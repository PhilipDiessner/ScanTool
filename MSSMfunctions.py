import datetime
import time
import os.path as osp
import SLHA_extract_values as SLHA
import sqlite3
import numpy as np
import Init
import Run
import LHCstudies as lhc
from functools import partial
from MRSSMroutines import run_base
from MRSSMfunctions import read_CM

# Global variables specifing scaning also needed for MPI
scanname = "pMSSMewinos"
scandir = osp.expanduser("~/raid2/MRSSMscans/")
dbdir = osp.expanduser("~/raid1/pointdbs/")
outdb = osp.join(dbdir,scanname+".db")
scanpath = osp.join(scandir,scanname)

Htemplate = "/home/diessner/raid2/Herwig++/Models/MSSM/mssm.template"
analyses = [ "atlas_conf_2013_049","atlas_1402_7029",
                 "atlas_conf_2013_035","atlas_conf_2013_036", "atlas_1403_5294"]
nofevents = 100000
print outdb

parameter = ["m1", "m2", "m3", "mq2", "mq332", "ml2", 
                 "ml332", "mu2", "mu332", "md2", "md332", 
                 "me2", "me332",  "mu", "ma2", "tanbeta","Ae","Ad","Au"]
para_types = ["real"]*len(parameter)

SPheno_MSSM = Run.SPheno_run("/home/diessner/raid2/SPheno-3.3.6/", "MSSM", 
                            "{0}.SLHA.in", "SPheno.spc.MSSM")

# def SPhenoMSSMwrapper(i,scandir):
#     """wrapper for SPhenorun in MSSM"""
#     sphenodir = "/home/diessner/raid2/SPheno/"
#    point = i + ".SLHA.in"
#     out = "SPheno.spc.MSSM" #i + ".SPheno.out"
#     cwd = osp.join(scandir,i)
#     print i 
#     out = Run.SPhenorun(sphenodir,"MSSM",point,out,cwd)

def createSLHAinMSSMfull(parameters,switches):
    """
    writing input spectrum of MSSM for SPheno
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
    2 1.166379E-05    # G_F,Fermi constant 
    3 1.188000E-01    # alpha_s(MZ) SM MSbar 
    4 9.118760E+01    # Z-boson pole mass 
    5 4.180000E+00    # m_b(mb) SM MSbar 
    6 1.730700E+02    # m_top(pole) 
    7 1.776690E+00    # m_tau(pole) 
Block MINPAR      # Input parameters
3   {0[15]:E}  # TanBeta
Block EXTPAR      # Input parameters 
1 {0[0]:E}     # M1input
2 {0[1]:E}     # M2input
3 {0[2]:E}     # M3input
8 {0[3]:E}     # mq2input
9 {0[4]:E}     # mq233input
10 {0[5]:E}     # ml2input
11 {0[6]:E}     # ml233input
12 {0[7]:E}     # mu2input
13 {0[8]:E}     # mu233input
14 {0[9]:E}     # md2input
15 {0[10]:E}     # md233input
16 {0[11]:E}     # me2input
17 {0[12]:E}     # me233input
18 {0[16]:E}     # Xeinput
19 {0[17]:E}     # Xdinput
20 {0[18]:E}     # Xuinput
23 {0[13]:E}     # Muinput
24 {0[14]:E}     # MA2input
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
 31 1000            # fixed GUT scale (-1: dynamical GUT scale) 
 32 0               # Strict unification 
 34 1.000E-04       # Precision of mass calculation 
 35 40              # Maximal number of iterations
 37 1               # Set Yukawa scheme  
 38 2               # 1- or 2-Loop RGEs 
 50 1               # Majorana phases: use only positive masses 
 51 0               # Write Output in CKM basis 
 52 1              # Write spectrum in case of tachyonic states 
 54 1              # stop if iteration doesn't converge
 55 {1[2]}             # Calculate one loop masses 
 57 {1[3]}               # Calculate low energy constraints 
 60 1               # Include possible, kinetic mixing 
 65 1               # Solution tadpole equation 
 75 0               # Write WHIZARD files 
 76 {1[4]}               # Write HiggsBounds file 
 86 0.              # Maximal width to be counted as invisible in Higgs decays; -1: only LSP 
510 0.              # Write tree level values for tadpole solutions 
515 0               # Write parameter values at GUT scale 
520 {1[4]}              # Write effective Higgs couplings (HiggsBounds blocks) 
525 {1[4]}              # Write loop contributions to diphoton decay of Higgs 
530 {1[5]}              # Write Blocks for Vevacious 
550 {1[6]}              # Calculate Fine-Tuning
""".format(parameters,switches)


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
    ['mah2','MASS',['36']],
    ['mhpm2','MASS',['37']],
    ['mz','MASS',['23']],
    ['mw','MASS',['24']],
    ['mglu','MASS',['1000021']],
    ['mchi1','MASS',['1000022']],
    ['mchi2','MASS',['1000023']],
    ['mchi3','MASS',['1000025']],
    ['mchi4','MASS',['1000035']],
    ['mcha1','MASS',['1000024']],
    ['mcha2','MASS',['1000037']],
]

masspar = [x[0] for x in masses]

write_masses = partial(Run.write_wrapper,
                       partial(Run.read_param, masses, "SPheno.spc.MSSM")
                       , "masses")

def MSSM_BM3():
    tanb = 40 # range(2,61,2)
    m1 = 250
    m2 = 500
    m3 = 1500
    mu = 400
    ma2 = 490000
    mq2 = 4000000
    ml2 = 1000000
    mu2 = 4000000
    md2 = 4000000
    me2 = 1000000
    mq332 = 1000000
    ml332 = 1000000
    mu332 = 1000000
    md332 = 1000000
    me332 = 1000000
    ae = 0
    ad = 0
    au = 1500
    mssm_value_arrays = [m1,m2,m3,
                          mq2,mq332,ml2,ml332,
                          mu2,mu332,md2,md332,me2,me332,
                          mu,ma2,tanb,ae,ad,au]
    return mssm_value_arrays

def MSSM_BM2():
    tanb = 6 # range(2,61,2)
    m1 = 100
    m2 = 500
    m3 = 2000
    mu = 500
    ma2 = 1000000
    mq2 = 4000000
    ml2 = 1000000
    mu2 = 4000000
    md2 = 4000000
    me2 = 90000
    mq332 = 1000000
    ml332 = 1000000
    mu332 = 1000000
    md332 = 1000000
    me332 = 90000
    ae = 0
    ad = 0
    au = 2000
    mssm_value_arrays = [m1,m2,m3,
                          mq2,mq332,ml2,ml332,
                          mu2,mu332,md2,md332,me2,me332,
                          mu,ma2,tanb,ae,ad,au]
    return mssm_value_arrays

def MSSM_BM1():
    tanb = 3 # range(2,61,2)
    m1 = 600
    m2 = 500
    m3 = 1500
    mu = 400
    ma2 = 490000
    mq2 = 4000000
    ml2 = 1000000
    mu2 = 4000000
    md2 = 4000000
    me2 = 1000000
    mq332 = 1000000
    ml332 = 1000000
    mu332 = 1000000
    md332 = 1000000
    me332 = 1000000
    ae = 0
    ad = 0
    au = 400/3.
    mssm_value_arrays = [m1,m2,m3,
                          mq2,mq332,ml2,ml332,
                          mu2,mu332,md2,md332,me2,me332,
                          mu,ma2,tanb,ae,ad,au]
    return mssm_value_arrays

def readHandW(i,scandir):
    masses = [['mh1','MASS',['25']],
              ['mh2','MASS',['35']],
              ['mw','MASS',['24']]]
    i = str(i)
    filename = osp.join(scandir,i,"SPheno.spc.MSSM")
    return SLHA.getvalues(filename, masses)

def wrapper(i,scandir):
    try:
        out = readHandW(i, scandir)
        #point = [i]+readHB(i,scandir)+readHS(i,scandir)
        print i
    except IOError:
        pass
    else: 
        point = [int(i)]+[float(x) for x in out]
        Init.register_point(outdb, 'mhmw', point)
  
def HBHSfullwrapper(i, scandir):
    SPhenoMSSMwrapper(i,scandir)
    wrapper(i,scandir)

def scaninit():
    point = MSSM_BM3()
    points = []
    # mu332 = 700*700
    # lamsu = 0.0
    # lamtu = -1.1
    #point[1:5] = [lamsu,lamsu,lamsu,lamtu] # lambdas 
    #point[9] =  mu332 # stops
    #point[13] =  mu332 # stops
    #point[-2] = 80*80 # mS2
    #point[-5] = 20 # MDB
    # for x in np.append(np.arange(-2,-0.6, 0.05),[0.5,0.4,0.3,0.2,0]): # lambda
    #     for y in range(0,50,1): # md1
    #         for z in [i*i for i in range(0,100,2)]: # mS2
    #             pointtmp = copy.deepcopy(point)
    #             pointtmp[4]= x
    #             pointtmp[-5] = y
    #             pointtmp[-2] = z
    #             points.append(pointtmp)
    # for x in range(100,1001,30): # mdw
    #     for y in range(100,501,30): # mu
    #         pointtmp = copy.deepcopy(point)
    #         pointtmp[-4] = x
    #         pointtmp[5] = y
    #         pointtmp[6] = y
    #         points.append(pointtmp)
    for x in range(100,501,50): # m2
        for y in range(150,451,50): # mu
            pointtmp = point[:]
            pointtmp[-4] = 20
            pointtmp[0] = 50
            pointtmp[1] = x
            pointtmp[11] = 450*450
            pointtmp[12] = y*y
            pointtmp[13] = 600
            points.append(pointtmp)
    print len(points)
    switches = [0,0,1,0,0,0,0]
    Init.init_struc(points, scanpath, zip(parameter,para_types), 
               switches, createSLHAinMSSMfull, dbdir,makedb=True)

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
    Hconfigtmp = osp.join(hevents,"herwigMSSM")
    hepmcpath = osp.join(hevents, name +  ".hepmc")
    Htemplate = '/home/diessner/raid1/ScanTool/MSSM.template'
    
    CMfile = osp.join(cmevents,"CM.dat")        
    slhafile = osp.join(cmevents, "SPheno.spc.MSSM")
    lhepath = None
    Hconfigbase = '/home/diessner/raid1/ScanTool/LHC-mssm.base'
    lhc.full_herwig(slhafile,name,hevents,Hcardname,Hconfigtmp,Hconfigbase,
                    Htemplate, hepmcpath, nofevents)
    if cm:
        lhc.CM_run(name,cmevents,analyses,hepmcpath,CMfile,nofevents,lhepath=lhepath)

lhc_out = partial(Run.write_more_wrapper, read_CM, 'lhc')
spheno_run = partial(run_base, SPheno_MSSM)
lhc_run = partial(run_base, lhc_study) # (lhc_study,
lhc_write = partial(run_base, lhc_out)
lhc_table = partial(Init.table_init, 'lhc', zip(['analysis','r','cl'],
                                                ['text','real','real']))

masses_table = partial(Init.table_init, 'masses', zip(masspar, ['real']*len(masspar)))
masses_write = partial(run_base, write_masses)

def adapt_stop_mass(val, value, param):
    # get correct combination, loop correction should be similar
    comb1 = [param[0]-val[0]**2, param[1]-val[1]**2]
    comb2 = [param[0]-val[1]**2, param[1]-val[0]**2]
    sbcontr = param[2]+value[2]**2-val[2]**2
    if abs(comb1[0]-comb1[1]) < abs(comb2[0]-comb2[1]):
        return[comb1[0]+value[0]**2,comb1[1]+value[1]**2,sbcontr]
    else:
        return[comb2[0]+value[1]**2,comb2[1]+value[0]**2,sbcontr]

def adapt_sleptons(val,value,param):
    comb2 = [param[0]-val[1]**2, param[1]-val[0]**2]    
    goal = ((val[-2]+val[-1])/2.)**2
    return [comb2[0]+goal,comb2[1]+goal]
    
def stop_mass(i, scandir):
    fit1 = Run.adaptive_scan([["mq2","EXTPAR",["13"]],
                              ["mu2","EXTPAR",["9"]],
                              ["md2","EXTPAR",["15"]]],
                             [["su1","MASS",["1000002"]],
                              ["su2","MASS",["1000004"]],
                              ["sd2","MASS",["1000003"]]],
                             [1000,1200,1200],adapt_stop_mass,
                             Init.changemultiparameter,
                             SPheno_MSSM,model="MSSM")
    fit1(i, scandir)
    wrapper(i,scandir)

def slepton_mass(i,scandir):
    fit1 = Run.adaptive_scan([["me2","EXTPAR",["16"]],
                              ["me332","EXTPAR",["17"]]],
                             [["se1","MASS",["1000011"]],
                              ["se3","MASS",["1000015"]],
                              ["ch1","MASS",["1000022"]],
                              ["ch2","MASS",["1000023"]]],
                             [1000,1200,1200,2000,2000],adapt_sleptons,
                             Init.changemultiparameter,
                             SPheno_MSSM,model="MSSM")
    fit1(i, scandir)


slepton_run = partial(run_base, slepton_mass)

if __name__ == "__main__":
    start = time.time()
    # scaninit()
    # spheno_run(scanpath, outdb, parallel=True)
    # lhc_table(outdb)
    masses_table(outdb)
    masses_write(scanpath, outdb)
    # slepton_run(scanpath,outdb,parallel=False)
    # lhc_run(scanpath, outdb, parallel=True)
    # lhc_write(scanpath, outdb)
    # fit1 = Run.adaptive_scan([["mq2","EXTPAR",["13"]],["mu2","EXTPAR",["9"]]], [["su1","MASS",["1000002"]], ["su2","MASS",["1000004"]]],
    #                   [1015,1015],adapt_stop_mass, changeparameter_in_SLHAin,
    #                   SPhenoMSSMwrapper)
    
    # fit1(10, "/amnt/remote/ZIH.fast/users/diessner/MRSSMscans/MSSMOS1l/")
    end = time.time()
    
    diff = end - start
    print datetime.timedelta(seconds=diff)
    m, s = divmod(diff, 60)
    h, m = divmod(m, 60)
    print "%d:%02d:%02d" % (h, m, s)
