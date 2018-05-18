import os.path as osp
import subprocess as spr
import os
import gzip
from random import randint
import string
import numpy as np
from Run import runwrapper, partial_runwrapper, touch#, replace_line_in_file
from SLHA_extract_values import get_sq_gl_masses
from HEPpaths import CMpath,nllpath,NLL

def MG_paramcard(slhafile,name,cardname,n,seed=0):
    out = """generate_events {0}
set nevents={1}
set iseed={2}
set cut_decays=F
set ebeam1=4000
set ebeam2=4000
{3}
""".format(name, n, seed,slhafile)
    with open(cardname, 'w') as f:
        f.write(out)

def Herwig_paramcard(pegmodel, slhafile, outfile,rundir):
     runwrapper(["slha2herwig", pegmodel,slhafile,"-o", outfile],rundir)

# def Herwigparamcard(pegmodel, slhafile, outfile,runpath):
#     try:
#         spr.check_call(["slha2herwig", pegmodel,slhafile, outfile],cwd=runpath)
#     except spr.CalledProcessError:
#         print "herwigpar: s.t. wrong for " + slhafile
#         return "Error"

def CM_paramcard(runname,rundir,analyses,hepmcfile,xsect,cardname,n,
                 Kfac="1",xsecunit="NB"):
    xerr = xsect/np.sqrt(n)
    out ="""## General Options
[Parameters]
Name: {0}_cm
##Analyses: atlas_1402_7029
Analyses: {1}
#
OutputDirectory: {2}
#SkipDelphes: False
SkipParamCheck: True
OutputExists: overwrite
FullCLs: False
WriteDelphesEvents: False
## Process Information (Each new process 'X' must start with [X])
[sq]
XSect: {3}*{7}
Kfac: {6}
XSectErr: {5}*{7}
Events: {4}
""".format(runname,",".join(analyses),rundir,xsect,hepmcfile,xerr,Kfac,xsecunit)
    with open(cardname, 'w') as f:
        f.write(out)

def CM_paramcard_rerun_noDelphes(runname,rundir,analyses,hepmcfile,xsect,cardname,n):
    # xerr = xsect/np.sqrt(n)
    touch(hepmcfile)
    replace_line_in_file("SkipDelphes: False","SkipDelphes: True", cardname)
        
def MG_run(execut,paramcard,directory):
    print execut,paramcard,directory
    runwrapper([execut, paramcard], directory)

def herwig_read(filename,tmpfile,runpath,paramfile, configfile, n):
    with open(configfile,'r') as f:
        lines = f.read()
    # appending for each SLHA file this spectrum as input and declaring to run 
    # full MC simulation creating
    # the hepmc-file
    startstring = "read "+ paramfile +"\n"
    
    endstring = "set /Herwig/Analysis/HepMC:PrintEvent " + str(n) + \
        "\nset /Herwig/Generators/LHCGenerator:NumberOfEvents " + str(n) + \
        "\nset /Herwig/Generators/LHCGenerator:MaxErrors " + str(n/20) +  \
        "\nset /Herwig/Generators/LHCGenerator:RandomNumberGenerator:Seed " + \
        str(randint(1,31122001)) + \
        "\nrun " + osp.basename(filename) +" LHCGenerator\n"
    with open(tmpfile+".in",'w') as f:
        f.write(startstring+lines+endstring)
    runwrapper(["Herwig++", "read", tmpfile+".in"],runpath)

def herwig7_read(filename,tmpfile,runpath,paramfile, configfile, n):
    with open(configfile,'r') as f:
        lines = f.read()
    # appending for each SLHA file this spectrum as input and declaring to run 
    # full MC simulation creating
    # the hepmc-file
    startstring = "read snippets/PPCollider.in"+"\n"+"read "+ paramfile +"\n"
    
    endstring = "set /Herwig/Analysis/HepMC:PrintEvent " + str(n) + \
        "\nset /Herwig/Generators/EventGenerator:NumberOfEvents " + str(n) + \
        "\nset /Herwig/Generators/EventGenerator:MaxErrors " + str(n/20) +  \
        "\nset /Herwig/Generators/EventGenerator:PrintEvent " + str(n) + \
        "\nset /Herwig/Generators/EventGenerator:RandomNumberGenerator:Seed " + \
        str(randint(1,31122001)) + \
        "\nrun " + osp.basename(filename) +" EventGenerator\n"
    with open(tmpfile+".in",'w') as f:
        f.write(startstring+lines+endstring)
    
    runwrapper(["Herwig", "read", tmpfile+".in"],runpath)


def herwig_run(filename, runpath,n):
    out = runwrapper(["Herwig++", "run", filename+".run", "-N"+str(n),"-d2"]
                     ,runpath)
    with open(osp.join(runpath,"Hlog.txt")) as f:
        f.write(out)
        
def herwig_cleanup(filename, runpath):
    try:
        os.remove(osp.join(runpath,filename + ".log"))
        # os.remove(osp.join(runpath,filename + ".out"))
        os.remove(osp.join(runpath,filename + ".hepmc"))
        os.remove(osp.join(runpath,filename + ".tex"))
    except:
	pass

def lhe_hepmc(lhepath,filename,tmpfile,runpath,paramfile, configfile,n):
    with open(configfile,'r') as f:
        lines = f.read()
    # appending for each SLHA file this spectrum as input and declaring to run 
    # parton shower, hadronisation simulation creating
    # the hepmc-file
    startstring = "read snippets/PPCollider.in"+"\n"+"read "+ paramfile +"\n"
    
    endstring = "set /Herwig/Analysis/HepMC:PrintEvent " + str(n) + \
        "\nset /Herwig/Generators/myLesHouchesGenerator:NumberOfEvents " + str(n) + \
        "\nset /Herwig/Generators/myLesHouchesGenerator:MaxErrors " + str(n/20) +  \
        "\nset /Herwig/EventHandlers/myReader:FileName " + lhepath + \
        "\nrun " + osp.basename(filename) +" myLesHouchesGenerator\n"
    with open(tmpfile,'w') as f:
        f.write(startstring+lines+endstring)
    runwrapper(["Herwig++", "read", tmpfile],runpath)

def read_xsec(lhefile):
    try:
        with gzip.open(lhefile) as f:
            while True:
                x=f.readline()
                if x == "<init>\n":
                    # LHE format defined so that second line has to contain x-sec
                    f.readline()
                    out = f.readline()
                    break
    except: 
        print "can't read xsec from: ", lhefile
        raise OSError
    return float(out.split()[0])/1000. # to nb

def read_xsec_herwig(herwigfile):
    with open(herwigfile) as f:
        for line in f:
            #line = line.split()
            if "Total" in line and "generated" in line:
                # LHE format defined so that second line has to contain x-sec
                out = line.split()[-1]
                break
    try:
        x = out
    except: 
        print "can't read xsec from: ", herwigfile
        raise OSError
    else:
        xs = out.split("(")
        rest = xs[1].split(")")
        return float(xs[0])*10**+int(rest[1][1:])

def run_CM(CMpath, paramfile,path): 
    runwrapper([CMpath, paramfile],path)

# def runCM(CMpath, paramfile):
#     try:
#         spr.check_call(['nice','-n','3',CMpath, paramfile])
#     except spr.CalledProcessError:
#         print "CM error for: "+ paramfile +"\n"

def genlhe(slhafile, process,name,events,cardname,nofevents):
    MG_paramcard(slhafile, osp.join(events,name), cardname, nofevents)
    MG_run(osp.join('.',"bin","madevent"), cardname, process)

def mg_herwig(slhafile, name, events, Hcardname, Hconfigtmp,
              Hconfigbase, Htemplate, lhepath, nofevents):
    Herwig_paramcard(Htemplate, slhafile, Hcardname, events)
    lhe_hepmc(lhepath, name, Hconfigtmp, events, Hcardname, Hconfigbase, nofevents)
    # herwig_cleanup(name,events)
    
def full_herwig(slhafile, name, runpath, Hcardname, Hconfigtmp, Hconfigbase,
                Htemplate, hepmcfile,  nofevents):
    Herwig_paramcard(Htemplate, slhafile, Hcardname,runpath)
    herwig7_read(name, Hconfigtmp,runpath,Hcardname, Hconfigbase, nofevents)
    
def CM_run(name,events,analyses,hepmcfile,CMfile,nofevents,
           sigma=None,Kfac=None,lhepath=None,cleanup=True):
    """
    Should only provide one of sigma,Kfac or lhepath, not checking if true
    Assuming sigma is in PB, else readin from Herwig in NB
    """
    CMpath = path.CMpath
    if sigma:
        xsect = sigma
    elif lhepath:
       xsect = read_xsec(lhepath)
    else:
        xsect = read_xsec_herwig(osp.join(osp.dirname(hepmcfile),name + ".out"))
    if not (Kfac and sigma):
        CM_paramcard(name,events,analyses,hepmcfile,xsect,CMfile,nofevents)
    elif sigma:
        if sigma<0:
            raise Exception("negative xsec for "+hepmcfile)
        else:
            CM_paramcard(name,events,analyses,hepmcfile,xsect,CMfile,nofevents,xsecunit="PB")
    elif Kfac:
        CM_paramcard(name,events,analyses,hepmcfile,xsect,CMfile,nofevents,Kfac=Kfac)
        
    print xsect,Kfac, CMfile,CMpath,events
    run_CM(CMpath, CMfile,events)
    if cleanup:
        herwig_cleanup(name,osp.dirname(hepmcfile))
    
def CM_run_no_delphes(name,events,analyses,hepmcfile,CMfile,nofevents,lhepath=None):
    xsect = -1 # rerunning
    CM_paramcard_rerun_noDelphes(name,events,analyses,hepmcfile,xsect,CMfile,nofevents)
    print xsect, CMfile
    run_CM(CMpath, CMfile,events)
    herwig_cleanup(name,osp.dirname(hepmcfile))

def get_Kfac(slha,pathtoslha,process):
    """
    returns the NLL K factor for a given process from NLLfast
    extracts squark and gluino masses from slha required as NLLfast input for process
    """
    msq,mgl = [str(float(a)) for a in get_sq_gl_masses(slha,pathtoslha)]
    nlloutput2 = None
    print NLL, process,msq,mgl
    if process=="st":
        print "stop pair not wrapped yet"
        nlloutput=""
    elif process=="gdcpl":
        nlloutput=runwrapper([NLL, process,mgl],path)
    elif process=="sdcpl":
        nlloutput=runwrapper([NLL, process,msq],path)
    elif process=="sqsum":
        nlloutput=runwrapper([NLL, "ss",msq,mgl],path)
        nlloutput2=runwrapper([NLL, "sb",msq,mgl],path)
    else:
        nlloutput=runwrapper([NLL, process,msq,mgl],path)
    line= nlloutput.split()
    if not line[0]=="TOO":
        sigma = float(line[-6])/1000. # in nb
        K = float(line[-1])
        if nlloutput2:
            line= nlloutput2.split()
            sigma += float(line[-6])/1000.
            print "K factor no reliable"
    else:
        K = 1.
        sigma = -1.
    return sigma,K
    
def read_CMresult(path,analysis):
    """
    reads results from the best_signal_regions.txt looking for analysis, reads
    only last block
    """
    try:
        with open(path) as f:
            lines = list(f)
    except IOError:
        return analysis, -1,-1
    else:
        r = 0.0
        cl = 1.0
        #lines.reverse() # get last block first
        for line in lines:
            spline= line.split()
            if spline[0] == "analysis":
                if len(spline)==11:
                    withcl = False
                    cl = -1
                elif len(spline)==13:
                    withcl =True
                else:
                    raise Exception("wrong format in readCMresult")
                continue
            elif analysis == 'best':
                newr = float(spline[10])
                if withcl:
                    newcl = float(spline[12])
                if withcl and newcl < cl:
                    newcl = float(spline[12])
                    # decide by cl what best region ist r is alternative
                    cl = newcl
                    r = newr
                elif newr>r:
                    r = newr
            elif analysis == spline[0]:
                if withcl:
                    cl = float(spline[12])
                r = float(spline[10])
        return analysis,r,cl

def read_CMresults(path):
    try:
        with open(path) as f:
            lines = list(f)
    except IOError:
        return []
    else:
        testr = 0.0
        testcl = 1.0
        out = []
        for line in lines:
            spline= line.split()
            if spline[0] == "analysis":
                if len(spline)==11:
                    withcl = False
                    testcl = -1
                    cl = -1
                elif len(spline)==13:
                    withcl =True
                else:
                    raise Exception("wrong format in readCMresult")
                continue
            else:
                analysis = spline[0]
                if withcl:
                    cl = float(spline[12])
                else:
                    cl = float(spline[9])
                    # take obs r value instead
                r = float(spline[10])
                out.append((analysis,r,cl))
                newr = float(spline[10])
                if withcl:
                    newcl = float(spline[12])
                else:
                    newcl = float(spline[9])
                if withcl and newcl < cl:
                    # decide by cl what best region ist r is alternative
                    testcl = newcl
                    testr = newr
                elif newr>testr:
                    testr = newr
                    testcl = newcl
        out.append(("best",testr,testcl))
        return out

if __name__ == "__main__":
    prefix = "/nfs/theoc/data/diessner/"
    homeprefix = '/afs/desy.de/user/d/diessner/'
    runpath = osp.join(prefix,"scantest")
    slha = osp.join(prefix,"SPheno-4.0.3/SPheno.spc.MRSSM")
    CMfile = osp.join(runpath,"CM.dat")        
    analyses = [ "atlas13TeV"]
    nofevents = 1000
    name ="MRSSM"
    Hcardname = osp.join(runpath ,"MRSSMH.dat")
    Hconfigtmp = osp.join(runpath, "MRSSMtest")
    # lhepath = osp.join(events, "unweighted_events.lhe.gz")
    hepmcfile = osp.join(runpath, name +  ".hepmc")
    Hconfigbase = osp.join(homeprefix,'data/ScanTool/LHC-mrssm.base.strong')
    Htemplate = osp.join(homeprefix,'data/ScanTool/MRSSM.template')
    #full_herwig(slha, name, runpath, Hcardname, Hconfigtmp, Hconfigbase,
    #             Htemplate, hepmcfile,  nofevents)
    #CM_run(name,runpath,analyses,hepmcfile,CMfile,nofevents,lhepath=None)
    # for i in xrange(1,320):
    #     try:
    #         lhefile = str(i) + ".lhe.gz"
    #         cardname = "MGrun_" + str(i)
    #         seed = i
    #         n = 25000
    #         name = i
    #         MGparamcard(slhafile,name,cardname, n, seed)
    # name = "4"
    # events = osp.expanduser("~/zihfast/MRSSMscans/lightsingletlhcm1m2/4/")
    # xsect = read_xsec_herw(osp.join(events,name + ".out"))
    # print xsect
    # CMparamcard(name,events, ['atlas_conf_2013_049', 'atlas_conf_2013_089', 'atlas_1402_7029', 'atlas_1403_5294'],osp.join(events,name + ".hepmc"),xsect,osp.join(events,name + "CM.dat"),100000)
    print get_Kfac("SPheno.spc.MSSM","/nfs/theoc/data/diessner/SPheno-4.0.3/","sdcpl")
    #print read_CMresults("/nfs/theoc/data2/diessner/MRSSMscans/MSSM_sq_lsp/1/lhc_cm/evaluation/best_signal_regions.txt")
