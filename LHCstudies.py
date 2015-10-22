import os.path as osp
import subprocess as spr
import os
import gzip
from random import randint
import string
import numpy as np
from Run import runwrapper, partial_runwrapper

MGpath = "/home/diessner/raid2/MG5_aMC_v2_1_1/bin/mg5_aMC"
Herwigpath = "Herwig++"
CMpath = "/home/diessner/raid2/CheckMATE-1.2.0/bin/CheckMATE"
Herwigconffile = "/home/diessner/raid2/"


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
     runwrapper(["slha2herwig", pegmodel,slhafile, outfile],rundir)

# def Herwigparamcard(pegmodel, slhafile, outfile,runpath):
#     try:
#         spr.check_call(["slha2herwig", pegmodel,slhafile, outfile],cwd=runpath)
#     except spr.CalledProcessError:
#         print "herwigpar: s.t. wrong for " + slhafile
#         return "Error"

def CM_paramcard(runname,rundir,analyses,hepmcfile,xsect,cardname,n):
    xerr = xsect/np.sqrt(n)
    out ="""## General Options
[Mandatory Parameters]
Name: {0}_cm
##Analyses: atlas_1402_7029
Analyses: {1}

[Optional Parameters]
OutputDirectory: {2}
SkipDelphes: False
SkipParamCheck: True
OutputExists: overwrite
FullCL: True
## Process Information (Each new process 'X' must start with [X])
[cha]
XSect: {3}*NB
XSectErr: {5}*NB
Events: {4}
""".format(runname,",".join(analyses),rundir,xsect,hepmcfile,xerr)
    with open(cardname, 'w') as f:
        f.write(out)

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
    
    endstring = "set /Herwig/Analysis/HepMCFile:PrintEvent " + str(n) + \
        "\nset /Herwig/Generators/LHCGenerator:NumberOfEvents " + str(n) + \
        "\nset /Herwig/Generators/LHCGenerator:MaxErrors " + str(n/20) +  \
        "\nset /Herwig/Generators/LHCGenerator:RandomNumberGenerator:Seed " + \
        str(randint(1,31122001)) + \
        "\nrun " + osp.basename(filename) +" LHCGenerator\n"
    with open(tmpfile+".in",'w') as f:
        f.write(startstring+lines+endstring)
    runwrapper(["Herwig++", "read", tmpfile+".in"],runpath)

def herwig_run(filename, runpath,n):
    out = runwrapper(["Herwig++", "run", filename+".run", "-N"+str(n),"-d2"]
                     ,runpath)
    with open(osp.join(runpath,"Hlog.txt")) as f:
        f.write(out)
        
def herwig_cleanup(filename, runpath):
    # os.remove(osp.join(runpath,filename + ".log"))
    # os.remove(osp.join(runpath,filename + ".out"))
    os.remove(osp.join(runpath,filename + ".hepmc"))
    os.remove(osp.join(runpath,filename + ".tex"))


def lhe_hepmc(lhepath,filename,tmpfile,runpath,paramfile, configfile,n):
    with open(configfile,'r') as f:
        lines = f.read()
    # appending for each SLHA file this spectrum as input and declaring to run 
    # parton shower, hadronisation simulation creating
    # the hepmc-file
    startstring = "read "+ paramfile +"\n"
    
    endstring = "set /Herwig/Analysis/HepMCFile:PrintEvent " + str(n) + \
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
            if line[:55] == "Total (from   weighted events): including vetoed events":
                # LHE format defined so that second line has to contain x-sec
                out = line.split()[-1]
                break
    try:
        x = line
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

def HerwigCM(slhafile,name,events,Hcardname,Hconfigtmp,Hconfigbase,
             Htemplate,lhepath,hepmcpath, analyses,CMfile,nofevents):
    Herwig_paramcard(Htemplate, slhafile, Hcardname,events)
    lhe_hepmc(lhepath,name,Hconfigtmp,events,Hcardname,Hconfigbase,nofevents)
    xsect = read_xsec(lhepath)
    print xsect
    CM_paramcard(name,events,analyses,hepmcpath,xsect,CMfile,nofevents)
    run_CM(CMpath, CMfile)
    herwig_cleanup(name,events)

def mg_herwig(slhafile, name, events, Hcardname, Hconfigtmp,
              Hconfigbase, Htemplate, lhepath, nofevents):
    Herwig_paramcard(Htemplate, slhafile, Hcardname, events)
    lhe_hepmc(lhepath, name, Hconfigtmp, events, Hcardname, Hconfigbase, nofevents)
    # herwig_cleanup(name,events)
    
def full_herwig(slhafile, name, events, Hcardname, Hconfigtmp, Hconfigbase,
                Htemplate, hepmcfile,  nofevents):
    Herwig_paramcard(Htemplate, slhafile, Hcardname,events)
    herwig_read(name, Hconfigtmp,events,Hcardname, Hconfigbase, nofevents)
    
    # herwig_run(name, events, nofevents)
    # xsect = read_xsec_herw(osp.join(events,name + ".out"))
    # if hepmcfile[-3:] == ".gz":
    #     spr.check_call(['nice','-n','3','gunzip', hepmcfile],cwd=events)
    #     CMparamcard(name,events,analyses,hepmcfile[:-3],xsect,CMfile,nofevents)
    # else:
    #     CMparamcard(name,events,analyses,hepmcfile,xsect,CMfile,nofevents)
    # runCM(CMpath, CMfile)
    # if osp.exists(osp.join(events,name)):
    #     if hepmcfile[-3:] == ".gz":
    #         os.remove(hepmcfile[:-3])
    #     else:
    #         os.remove(hepmcfile)
    # herwig_cleanup(name,events)
    
def CM_run(name,events,analyses,hepmcfile,CMfile,nofevents,lhepath=None):
    if lhepath:
       xsect = read_xsec(lhepath)
    else:
        xsect = read_xsec_herwig(osp.join(osp.dirname(hepmcfile),name + ".out"))
    CM_paramcard(name,events,analyses,hepmcfile,xsect,CMfile,nofevents)
    print xsect, CMfile
    run_CM(CMpath, CMfile,events)
    herwig_cleanup(name,osp.dirname(hepmcfile))
    
def read_CMresult(path,analysis):
    try:
        with open(path) as f:
            lines = list(f)
    except IOError:
        return analysis, -1,-1
    else:
        r = 0.0
        cl = 1.0
        for line in lines[1:]:
            spline= line.split()
            if analysis == 'best':
                newr = float(spline[2])
                newcl = float(spline[4])
                if newcl < cl:
                    # decide only by cl what best region ist
                    cl = newcl
                    r = newr
            elif analysis == spline[0]:
                cl = float(spline[4])
                r = float(spline[2])
        return analysis,r,cl

# if __name__ == "__main__":
#     # slha = osp.expanduser("~/raid2/SPheno/SPheno.spc.MRSSM")
#     # process = osp.expanduser("~/raid2/MG5_aMC_v2_1_1/oddwino2/")
#     # nofevents = 1000
#     # name ="1"
#     # events = osp.join(process,"Events", name)
#     # cardname = osp.join(process, "MG"+name)
#     # Hcardname = osp.join(events ,"H.dat")
#     # Hruncardname = osp.join(events ,"Hrun.dat")
#     # Hconfigtmp = osp.join(process, "MRSSM.in")
#     # lhepath = osp.join(events, "unweighted_events.lhe.gz")
#     # hepmcpath = osp.join(events, name +  ".hepmc")
#     # analyses = ["atlas_conf_2013_035"]
#     # CMfile = osp.join(events, "CM.dat")
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

    
