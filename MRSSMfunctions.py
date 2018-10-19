import os.path as osp
import copy
import sqlite3
from functools import partial
import shutil
import Init
import Run
import LHCstudies as lhc
import SLHA_extract_values as SLHA
from HEPpaths import inprefix,outprefix,homeprefix,\
    analyses,nofevents,Hconf_process,SPhenodir,Htemplate,\
    mg_process,HBdir,HSdir,uncerfile,dmexecut,sfermionmix,mwos


def createSLHAinMRSSMfull(parameters,switches):
    """
    writing input spectrum of MRSSM for SPheno
    switches - flags for SPhenoInput, look for {0[i]} in string
    values - actual scan values, look for {1[j]:E} in string
    filename - name of file
    filedir - directory to put the file
    """
    return """Block MODSEL      #  
1 1              #  1/0: High/low scale input 
2 1              # Boundary Condition  
6 0              # Generation Mixing 
Block SMINPUTS    # Standard Model inputs 
    1 1.279500E+02   # alpha^-1 (MZ) SM MSbar
    2 1.166379E-05    # G_F,Fermi constant 
    3 1.185000E-01    # alpha_s(MZ) SM MSbar 
    4 9.118760E+01    # Z-boson pole mass 
    5 4.180000E+00    # m_b(mb) SM MSbar 
    6 1.732100E+02    # m_top(pole) 
    7 1.776860E+00    # m_tau(pole) 
Block MINPAR      # Input parameters 
3  {0[0]:E}     # TanBeta
Block EXTPAR      # Input parameters 
1 {0[1]:E}     # LSDinput
2 {0[2]:E}     # LSUinput
3 {0[3]:E}     # LTDinput
4 {0[4]:E}     # LTUinput
5 {0[5]:E}     # MuDinput
6 {0[6]:E}     # MuUinput
7 {0[7]:E}     # MA2input
8 {0[8]:E}     # mq2input
9 {0[9]:E}     # mq332input
10 {0[10]:E}     # ml2input
11 {0[11]:E}     # ml332input
12 {0[12]:E}     # mu2input
13 {0[13]:E}     # mu332input
14 {0[14]:E}     # md2input
15 {0[15]:E}     # md332input
16 {0[16]:E}     # me2input
17 {0[17]:E}     # me332input
18 {0[18]:E}     # mRu2input
19 {0[19]:E}     # mRd2input
20 {0[20]:E}     # mO2input
21 {0[21]:E}     # M1input
22 {0[22]:E}     # M2input
23 {0[23]:E}     # M3input
65 {0[24]:E}     # mS2Input
66 {0[25]:E}     # mT2Input
Block SPhenoInput   # SPheno specific input 
  1 -1              # error level 
  2 0               # SPA conventions  
  7 {1[0]}              # Skip 2-loop Higgs corrections
  8  3              # Method used for two-loop calculation
  9  1              # Gaugeless limit used at two-loop
 10  0              # safe-mode used at two-loop
 11 {1[1]}              # calculate branching ratios 
 13 {1[1]}              # include 3-Body decays 
 12 1.000E-04       # write only branching ratios larger than this value 
 16 0               # One-loop decays
 31 10000            # fixed GUT scale (-1: dynamical GUT scale) 
 32 0               # Strict unification 
 34 1.000E-04       # Precision of mass calculation 
 35 40              # Maximal number of iterations
 37 1               # Set Yukawa scheme  
 38 2               # 1- or 2-Loop RGEs 
 50 0               # Majorana phases: use only positive masses 
 51 0               # Write Output in CKM basis 
 52 1              # Write spectrum in case of tachyonic states 
 54 1              # stop if iteration doesn't converge
 55 {1[2]}             # Calculate one loop masses 
 57 {1[3]}               # Calculate low energy constraints 
 60 0               # Include possible, kinetic mixing 
 65 1               # Solution tadpole equation  
 66 0               # Two-Scale Matching
 67 0               # effective Higgs mass calculation
 75 0               # Write WHIZARD files 
 76 {1[4]}               # Write HiggsBounds file 
 77 0               # Output for MicrOmegas (running masses for light quarks; real mixing matrices) 
 78 1               # Output for MadGraph (writes also vanishing blocks)
 86 0.              # Maximal width to be counted as invisible in Higgs decays; -1: only LSP 
510 0.              # Write tree level values for tadpole solutions 
515 0               # Write parameter values at GUT scale 
520 0               # Write effective Higgs couplings (HiggsBounds blocks) 
521 0
525 {1[4]}              # Write loop contributions to diphoton decay of Higgs 
530 {1[5]}              # Write Blocks for Vevacious 
""".format(parameters,switches)

def createSLHAinMRSSMmix(parameters,switches):
    """
    writing input spectrum of MRSSM for SPheno
    switches - flags for SPhenoInput, look for {0[i]} in string
    values - actual scan values, look for {1[j]:E} in string
    filename - name of file
    filedir - directory to put the file
    """
    return """Block MODSEL      #  
1 1              #  1/0: High/low scale input 
2 1              # Boundary Condition  
6 0              # Generation Mixing 
Block SMINPUTS    # Standard Model inputs 
    1 1.279500E+02   # alpha^-1 (MZ) SM MSbar
    2 1.166379E-05    # G_F,Fermi constant 
    3 1.185000E-01    # alpha_s(MZ) SM MSbar 
    4 9.118760E+01    # Z-boson pole mass 
    5 4.180000E+00    # m_b(mb) SM MSbar 
    6 1.732100E+02    # m_top(pole) 
    7 1.776860E+00    # m_tau(pole) 
Block MINPAR      # Input parameters 
3  {0[0]:E}     # TanBeta
Block EXTPAR      # Input parameters 
1 {0[1]:E}     # LSDinput
2 {0[2]:E}     # LSUinput
3 {0[3]:E}     # LTDinput
4 {0[4]:E}     # LTUinput
5 {0[5]:E}     # MuDinput
6 {0[6]:E}     # MuUinput
7 {0[7]:E}     # MA2input
8 {0[8]:E}     # mq2input
9 {0[9]:E}     # mq332input
10 {0[10]:E}     # ml2input
11 {0[11]:E}     # ml332input
12 {0[12]:E}     # mu2input
13 {0[13]:E}     # mu332input
14 {0[14]:E}     # md2input
15 {0[15]:E}     # md332input
16 {0[16]:E}     # me2input
17 {0[17]:E}     # me332input
18 {0[18]:E}     # mRu2input
19 {0[19]:E}     # mRd2input
20 {0[20]:E}     # mO2input
21 {0[21]:E}     # M1input
22 {0[22]:E}     # M2input
23 {0[23]:E}     # M3input
65 {0[24]:E}     # mS2Input
66 {0[25]:E}     # mT2Input
112 {0[26]:E}     # mq212Input
113 {0[27]:E}     # mq213Input
123 {0[28]:E}     # mq223Input
212 {0[29]:E}     # mu212Input
213 {0[30]:E}     # mu213Input
223 {0[31]:E}     # mu223Input
312 {0[32]:E}     # md212Input
313 {0[33]:E}     # md213Input
323 {0[34]:E}     # md223Input
122 {0[35]:E}     # mq222Input
222 {0[36]:E}     # mu222Input
322 {0[37]:E}     # md222Input
Block SPhenoInput   # SPheno specific input 
  1 -1              # error level 
  2 1               # SPA conventions  
  7 {1[0]}              # Skip 2-loop Higgs corrections
  8  3              # Method used for two-loop calculation
  9  1              # Gaugeless limit used at two-loop
 10  0              # safe-mode used at two-loop
 11 {1[1]}              # calculate branching ratios 
 13 {1[1]}              # include 3-Body decays 
 12 1.000E-04       # write only branching ratios larger than this value 
 16 0               # One-loop decays
 31 10000            # fixed GUT scale (-1: dynamical GUT scale) 
 32 0               # Strict unification 
 34 1.000E-04       # Precision of mass calculation 
 35 40              # Maximal number of iterations
 37 1               # Set Yukawa scheme  
 38 2               # 1- or 2-Loop RGEs 
 50 0               # Majorana phases: use only positive masses 
 51 0               # Write Output in CKM basis 
 52 1              # Write spectrum in case of tachyonic states 
 54 1              # stop if iteration doesn't converge
 55 {1[2]}             # Calculate one loop masses 
 57 {1[3]}               # Calculate low energy constraints 
 60 0               # Include possible, kinetic mixing 
 65 1               # Solution tadpole equation  
 66 0               # Two-Scale Matching
 67 0               # effective Higgs mass calculation
 75 0               # Write WHIZARD files 
 76 {1[4]}               # Write HiggsBounds file 
 77 0               # Output for MicrOmegas (running masses for light quarks; real mixing matrices) 
 78 1               # Output for MadGraph (writes also vanishing blocks)
 86 0.              # Maximal width to be counted as invisible in Higgs decays; -1: only LSP 
510 0.              # Write tree level values for tadpole solutions 
515 0               # Write parameter values at GUT scale 
520 0               # Write effective Higgs couplings (HiggsBounds blocks) 
521 0
525 {1[4]}              # Write loop contributions to diphoton decay of Higgs 
530 {1[5]}              # Write Blocks for Vevacious 
""".format(parameters,switches)


def createSLHAinMRSSMmt(parameters,switches):
    """
    writing input spectrum of MRSSM for SPheno
    switches - flags for SPhenoInput, look for {0[i]} in string
    values - actual scan values, look for {1[j]:E} in string
    filename - name of file
    filedir - directory to put the file
    """
    return """Block MODSEL      #  
1 1              #  1/0: High/low scale input 
2 1              # Boundary Condition  
6 0              # Generation Mixing 
Block SMINPUTS    # Standard Model inputs 
    1 1.281339E+02   # alpha^-1 (MZ) SM MSbar
    2 1.1663787E-05    # G_F,Fermi constant 
    3 1.181000E-01    # alpha_s(MZ) SM MSbar 
    4 9.118760E+01    # Z-boson pole mass 
    5 4.80000E+00    # m_b(mb) SM MSbar 
    6 {0[26]:E}    # m_top(pole) 
    7 1.776860E+00    # m_tau(pole) 
Block MINPAR      # Input parameters 
3  {0[0]:E}     # TanBeta
Block EXTPAR      # Input parameters 
1 {0[1]:E}     # LSDinput
2 {0[2]:E}     # LSUinput
3 {0[3]:E}     # LTDinput
4 {0[4]:E}     # LTUinput
5 {0[5]:E}     # MuDinput
6 {0[6]:E}     # MuUinput
7 {0[7]:E}     # MA2input
8 {0[8]:E}     # mq2input
9 {0[9]:E}     # mq332input
10 {0[10]:E}     # ml2input
11 {0[11]:E}     # ml332input
12 {0[12]:E}     # mu2input
13 {0[13]:E}     # mu332input
14 {0[14]:E}     # md2input
15 {0[15]:E}     # md332input
16 {0[16]:E}     # me2input
17 {0[17]:E}     # me332input
18 {0[18]:E}     # mRu2input
19 {0[19]:E}     # mRd2input
20 {0[20]:E}     # mO2input
21 {0[21]:E}     # M1input
22 {0[22]:E}     # M2input
23 {0[23]:E}     # M3input
65 {0[24]:E}     # mS2Input
66 {0[25]:E}     # mT2Input
Block SPhenoInput   # SPheno specific input 
  1 -1              # error level 
  2 0               # SPA conventions  
  7 {1[0]}              # Skip 2-loop Higgs corrections
  8  3              # Method used for two-loop calculation
  9  1              # Gaugeless limit used at two-loop
 10  0              # safe-mode used at two-loop
 11 {1[1]}              # calculate branching ratios 
 13 {1[1]}              # include 3-Body decays 
 12 1.000E-04       # write only branching ratios larger than this value 
 16 0               # One-loop decays
 31 10000            # fixed GUT scale (-1: dynamical GUT scale) 
 32 0               # Strict unification 
 34 1.000E-04       # Precision of mass calculation 
 35 40              # Maximal number of iterations
 37 1               # Set Yukawa scheme  
 38 2               # 1- or 2-Loop RGEs 
 50 0               # Majorana phases: use only positive masses 
 51 0               # Write Output in CKM basis 
 52 1              # Write spectrum in case of tachyonic states 
 54 1              # stop if iteration doesn't converge
 55 {1[2]}             # Calculate one loop masses 
 57 {1[3]}               # Calculate low energy constraints 
 60 0               # Include possible, kinetic mixing 
 65 1               # Solution tadpole equation  
 66 0               # Two-Scale Matching
 67 0               # effective Higgs mass calculation
 75 0               # Write WHIZARD files 
 76 {1[4]}               # Write HiggsBounds file 
 77 0               # Output for MicrOmegas (running masses for light quarks; real mixing matrices) 
 78 1               # Output for MadGraph (writes also vanishing blocks)
 86 0.              # Maximal width to be counted as invisible in Higgs decays; -1: only LSP 
510 0.              # Write tree level values for tadpole solutions 
515 0               # Write parameter values at GUT scale 
520 0               # Write effective Higgs couplings (HiggsBounds blocks) 
521 0
525 {1[4]}              # Write loop contributions to diphoton decay of Higgs 
530 {1[5]}              # Write Blocks for Vevacious 
""".format(parameters,switches)



if sfermionmix:
    createSLHAinMRSSM = createSLHAinMRSSMmix
elif mwos:
    createSLHAinMRSSM = createSLHAinMRSSMmt
else:
    createSLHAinMRSSM = createSLHAinMRSSMfull

# pass arguments to partial_runwrapper derived functions, have i, scandir
# as usual argument
SPheno_MRSSM = Run.SPheno_run(SPhenodir, "MRSSM", 
                             "{0}.SLHA.in", "SPheno.spc.MRSSM")
HB_MRSSM = Run.HB_run(HBdir, 7, 3, "")
HS_MRSSM = Run.HS_run(HSdir, 7, 3, "")

def hbhs_uncertain_file(i,scandir):
    shutil.copy2(uncerfile, osp.join(scandir, Init.ident_to_path(i)))
    
def run_dm(i,scandir):
    directory = osp.join(scandir, Init.ident_to_path(i))
    Run.runwrapper([dmexecut], directory)

masses= [
    ['mse1','MASS',['1000011']],
    ['mse2','MASS',['1000013']],
    ['mse3','MASS',['1000015']],
    ['mse4','MASS',['2000011']],
    ['mse5','MASS',['2000013']],
    ['mse6','MASS',['2000015']],
    ['msv1','MASS',['1000012']],
    ['msv2','MASS',['1000014']],
    ['msv3','MASS',['1000016']],
    ['msu1','MASS',['1000002']],
    ['msu2','MASS',['1000004']],
    ['msu3','MASS',['1000005']],
    ['msu4','MASS',['2000002']],
    ['msu5','MASS',['2000004']],
    ['msu6','MASS',['2000006']],
    ['msd1','MASS',['1000001']],
    ['msd2','MASS',['1000003']],
    ['msd3','MASS',['1000005']],
    ['msd4','MASS',['2000001']],
    ['msd5','MASS',['2000003']],
    ['msd6','MASS',['2000005']],
    ['mhh1','MASS',['25']],
    ['mhh2','MASS',['35']],
    ['mhh3','MASS',['45']],
    ['mhh4','MASS',['55']],
    ['mah2','MASS',['36']],
    ['mah3','MASS',['46']],
    ['mah4','MASS',['56']],
    ['mhpm2','MASS',['37']],
    ['mhpm3','MASS',['47']],
    ['mhpm4','MASS',['57']],
    ['mz','MASS',['23']],
    ['mw','MASS',['24']],
    ['mglu','MASS',['1000021']],
    ['mphio','MASS',['3000021']],
    ['msigo','MASS',['3000022']],
    ['mchi1','MASS',['1000022']],
    ['mchi2','MASS',['1000023']],
    ['mchi3','MASS',['1000025']],
    ['mchi4','MASS',['1000035']],
    ['mcha11','MASS',['1000024']],
    ['mcha12','MASS',['1000037']],
    ['mcha21','MASS',['2000024']],
    ['mcha22','MASS',['2000037']],
    ['mrh1','MASS', ['401']],
    ['mrh2','MASS', ['402']],
    ['mrpm1','MASS', ['403']],
    ['mrpm2','MASS', ['404']],
    ['mt','MASS',['6']]
]

mixmatrix = [["zh11",'SCALARMIX',['1','1']],["zh12",'SCALARMIX',['1','2']],
             ["zh13",'SCALARMIX',['1','3']],["zh14",'SCALARMIX',['1','4']],
             ["zh21",'SCALARMIX',['2','1']],["zh22",'SCALARMIX',['2','2']],
             ["zh23",'SCALARMIX',['2','3']],["zh24",'SCALARMIX',['2','4']],
         ]

derived_par = [['vS','NMSSMRUN',['5']], ['vT','HMIX',['310']],
               ['mHd2','MSOFT',['21']],['mHu2','MSOFT',['22']],
               ['vd','HMIX',['102']],['vu','HMIX',['103']],
               ['g1','GAUGE',['1']],['g2','GAUGE',['2']],['g3','GAUGE',['3']]]

sulmix = [["ul11","ULSQMIX",["1","1"]],["ul12","ULSQMIX",["1","2"]],
          ["ul13","ULSQMIX",["1","3"]],["ul21","ULSQMIX",["2","1"]],
          ["ul22","ULSQMIX",["2","2"]],["ul23","ULSQMIX",["2","3"]],
          ["ul31","ULSQMIX",["3","1"]],["ul32","ULSQMIX",["3","2"]],
          ["ul33","ULSQMIX",["3","3"]]]

masspar = [x[0] for x in masses]
derivedpar = [x[0] for x in derived_par]
hmixpar = [x[0] for x in mixmatrix]
sulpar= [x[0] for x in sulmix]

def read_CM(i,scandir):
    """read all signal regions evaluated, first checks if result exists"""
    results = osp.join(scandir,Init.ident_to_path(i),'lhc_cm','result.txt')
    if not osp.exists(results):
        print "s.th. wrong with CheckMATE, no result for " + i
        raise IOError
            
    out = [lhc.read_CMresult(osp.join(scandir,Init.ident_to_path(i),'lhc_cm',
                                       "evaluation", "best_signal_regions.txt"),analysis)
            for analysis in analyses+['best']]
    print out
    return out

def read_CM2(i,scandir):
    """read all signal regions evaluated, first checks if result exists"""
    results = osp.join(scandir,Init.ident_to_path(i),'lhc_cm','result.txt')
    if not osp.exists(results):
        print "s.th. wrong with CheckMATE, no result for " + i
        raise IOError
    results = osp.join(scandir,Init.ident_to_path(i),'lhc_cm',
                       "evaluation", "best_signal_regions.txt")
    
    out = lhc.read_CMresults(results)
    print out
    return out

def read_relic_out(i, scandir):
    outfile = osp.join(scandir,Init.ident_to_path(i),"omg.out")
    with open(outfile) as f:
        output = f.readlines()
    ret = [-1]
    for line in output:
        line = line.split()
        if line[0] == "1":
            ret = line[1:2]
        if line[0] == "999" and ret != [-1]:
            ret.append(line[1])
        if line[0] == "998" and ret != [-1]:
            ret.append(line[1])
    print ret
    return ret

def read_twodm_relic_out(i, scandir):
    outfile = osp.join(scandir,Init.ident_to_path(i),"omg.out")
    with open(outfile) as f:
        output = f.readlines()
    ret = [-1]
    for line in output:
        line = line.split()
        if line[0] == "1":
            ret = line[1:2]
        if line[0] == "2" and ret != [-1]:
            ret.append(line[1])
        if line[0] == "3" and ret != [-1]:
            ret.append(line[1])
    print ret
    return ret
# derived functions to write to db
write_masses = partial(Run.write_wrapper,
                       partial(Run.read_param, masses, "SPheno.spc.MRSSM")
                       , "masses")
write_derived_par = partial(Run.write_wrapper,
                       partial(Run.read_param, derived_par,
                               "SPheno.spc.MRSSM"), "derivedpar")
write_sulmix = partial(Run.write_wrapper,
                       partial(Run.read_param, sulmix,
                               "SPheno.spc.MRSSM"), "sulmix")
zhmix = partial(Run.write_wrapper,
                partial(Run.read_param, mixmatrix, "SPheno.spc.MRSSM")
                ,"hmix")
write_omega = partial(Run.write_wrapper, read_relic_out, 'relic',)
HBHS_write_wrapper = partial(Run.write_wrapper,Run.read_hbhs , 'hbhs')
lhc_out = partial(Run.write_more_wrapper, read_CM2, 'lhc')



def swapflag(db,scanp ):
    # comm = ('SELECT C.identifier, C.lamsd, C.lamsu' 
    #         'FROM (SELECT points.identifier, IFNULL(mhmw.mh1,0)' 
    #         'AS fls,points.lamsd, points.lamsu FROM points' 
    #         'LEFT OUTER JOIN mhmw ON points.identifier=mhmw.identifier) C' 
    #         'WHERE C.fls==0')
    # pts = Init.points(db,comm)
    method = []
    # for i in range(len(pts)-1):
    #     # if pts[i-1][0] == pts[i][0]-1 and pts[i+1][0] == pts[i][0]+1:
    #     #     continue
    #     # else:
    #     method.append(pts[i][0])
    print len(method)
    runfunc = Run.run_on_dir(scanp)
    twolchange = Init.changeSLHAwrapper(Init.changeoneparameter,
                                        ['tachy','SPhenoInput',['52']],0)
    runfunc(twolchange, parallel=False)

def mg_run(i,scandir):
    name = 'lhc'
    events = osp.join(scandir, str(i))
    cardname = osp.join(events, "MGcard.dat") 
    slhafile = osp.join(events, "SPheno.spc.MRSSM")
    lhc.genlhe(slhafile, mg_process,name,events,cardname,nofevents)
    
def lhc_study_iktp(i,scandir, mg = False, cm = True):
    if type(scandir) in (tuple, list):
        cmdir, herwigdir = scandir
    else:
        herwigdir, cmdir = scandir, scandir
    name = 'lhc'
    hevents = osp.join(herwigdir,Init.ident_to_path(i))
    cmevents = osp.join(cmdir, Init.ident_to_path(i))
    
    cardname = osp.join(hevents, "MGcard.dat")
    Hcardname = osp.join(hevents, "H.dat")
    # Hruncardname = osp.join(events,"Hrun.dat")
    Hconfigtmp = osp.join(hevents,"herwigMRSSM")
    hepmcpath = osp.join(hevents, name +  ".hepmc")
    
    CMfile = osp.join(cmevents,"CM.dat")        
    slhafile = osp.join(cmevents, "SPheno.spc.MRSSM")
    lhepath = None
        
    # lhc.genlhe(slhafile,process,name,events,cardname,nofevents)
    # lhc.HerwigCM(slhafile,process,name,events,Hcardname,Hconfigtmp,Hconfigbase,
    #              Htemplate,lhepath,hepmcpath, analyses,CMfile,nofevents)
    if mg:
        mg_process = '/home/diessner/raid2/MG5_aMC_v2_1_1/ewino_speedtest/'
        lhepath = osp.join(hevents, name, "unweighted_events.lhe.gz")
        Hconfigbase = '/home/diessner/raid1/ScanTool/LHE-mrssm.base'
        lhc.mg_herwig(slhafile, name, hevents, Hcardname,
                      Hconfigtmp,Hconfigbase, Htemplate, lhepath, nofevents)
    else:
        Hconfigbase = Hconf_process
        lhc.full_herwig(slhafile,name,hevents,Hcardname,Hconfigtmp,Hconfigbase,
                        Htemplate, hepmcpath, nofevents)
    if cm:
        lhc.CM_run(name,cmevents,analyses,hepmcpath,CMfile,nofevents,lhepath=lhepath)

def MRSSM_get_Kfac(slha,path,process):
    """to be implemented"""
    msq,mgl = [float(a) for a in SLHA.get_sq_gl_masses(slha,path)]
    xsecs = [0.00981,  0.0010, 0.000177, 4.42e-05, 1.4159e-05,
             5.39e-06, 2.29e-06, 1.038e-06]
    sqval = range(400,1801,200)
    diff = [abs(x-msq) for x in sqval]
    min1,xsec = min(zip(diff,xsecs),key=lambda x: x[0])
    return xsec,1
    
def lhc_study(i,scandir, cm = True):
    if type(scandir) in (tuple, list):
        cmdir, herwigdir = scandir
    else:
        herwigdir, cmdir = scandir, scandir
    name = 'lhc'
    hevents = osp.join(herwigdir,Init.ident_to_path(i))
    cmevents = osp.join(cmdir, Init.ident_to_path(i))
    
    cardname = osp.join(hevents, "MGcard.dat")
    Hcardname = osp.join(hevents, "H.dat")
    # Hruncardname = osp.join(events,"Hrun.dat")
    Hconfigtmp = osp.join(hevents,"herwigMRSSM")
    hepmcpath = osp.join(hevents, name +  ".hepmc")
    
    CMfile = osp.join(cmevents,"CM.dat")        
    slhafile = osp.join(cmevents, "SPheno.spc.MRSSM")
    SLHA.flavor_order(slhafile,toRSSM=True)
    lhepath = None
        
    # lhc.genlhe(slhafile,process,name,events,cardname,nofevents)
    # lhc.HerwigCM(slhafile,process,name,events,Hcardname,Hconfigtmp,Hconfigbase,
    #              Htemplate,lhepath,hepmcpath, analyses,CMfile,nofevents)

    Hconfigbase = Hconf_process
    lhc.full_herwig(slhafile,name,hevents,Hcardname,Hconfigtmp,Hconfigbase,
                   Htemplate, hepmcpath, nofevents)
    if cm:
        lhc.CM_run(name,cmevents,analyses,hepmcpath,CMfile,
                   nofevents,cleanup=True)

def rerun_CM(i,scandir):
    if type(scandir) in (tuple, list):
        cmdir, herwigdir = scandir
    else:
        herwigdir, cmdir = scandir, scandir
    name = 'lhc'
    hevents = osp.join(herwigdir,Init.ident_to_path(i))
    cmevents = osp.join(cmdir, Init.ident_to_path(i))
    
    cardname = osp.join(hevents, "MGcard.dat")
    Hcardname = osp.join(hevents, "H.dat")
    # Hruncardname = osp.join(events,"Hrun.dat")
    Hconfigtmp = osp.join(hevents,"herwigMRSSM")
    hepmcpath = osp.join(hevents, name +  ".hepmc")
    
    CMfile = osp.join(cmevents,"CM.dat")        
    slhafile = osp.join(cmevents, "SPheno.spc.MRSSM")
    lhepath = None

    lhc.CM_run_no_delphes(name,cmevents,analyses,hepmcpath,CMfile,nofevents,lhepath=lhepath)
        
def lhc_wrapper(i,scandir):
    SPheno_MRSSM(i,scandir)
    lhc_study(i,scandir)

def adapt_stop_mass(val, value, param):
    # get correct combination, loop correction should be similar
    comb1 = [param[0]-val[0]**2, param[1]-val[1]**2]
    comb2 = [param[0]-val[1]**2, param[1]-val[0]**2]
    sbcontr = param[2]+value[2]**2-val[2]**2
    socontr = 5000*5000 #  param[3]+value[3]**2-val[3]**2
    if abs(comb1[0]-comb1[1]) < abs(comb2[0]-comb2[1]):
        return[comb1[0]+value[0]**2,comb1[1]+value[1]**2,sbcontr]
    else:
        return[comb2[0]+value[1]**2,comb2[1]+value[0]**2,sbcontr]

def stop_mass_wrapper(i, scandir):
    fit1 = Run.adaptive_scan([["mq2","EXTPAR",["13"]],
                              ["mu2","EXTPAR",["9"]],
                              ["md2","EXTPAR",["15"]],
                              #["mo2","EXTPAR",["20"]]
                          ],
                             [["su1","MASS",["1000002"]],
                              ["su2","MASS",["1000004"]],
                              ["sd2","MASS",["1000003"]],
                              # ["phiO","MASS",["3000021"]]
                          ],
                             [2000,3000,3000],adapt_stop_mass,
                             Init.changemultiparameter,
                             SPheno_MRSSM,eps=0.001)
    SPheno_MRSSM(i, scandir)
    fit1(i, scandir)
    wrapper(i,scandir)
    
if __name__ == "__main__":
    # lhc_study(14,
    #           '/amnt/remote/pkts08.raid2/users/diessner/MRSSMscans/bm5_lhc_mud_mdw',
    #           db='/home/diessner/raid1/pointdbs/bm5_lhc_mud_mdw.db')
    swapflag("nodbneeded","/home/diessner/raid2/MRSSMscans/conclusion/")
