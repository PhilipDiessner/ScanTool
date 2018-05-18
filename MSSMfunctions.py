import datetime
import time
import os.path as osp
import sqlite3
import numpy as np
import Init
import Run
import SLHA_extract_values as SLHA
import LHCstudies as lhc
from functools import partial
from MRSSMfunctions import read_CM,read_CM2

# Global variables specifing scaning also needed for MPI
scanname = "MSSM_msqmst"
homeprefix = '/afs/desy.de/user/d/diessner/'
inprefix = '/nfs/theoc/data/diessner/'
outprefix = '/nfs/theoc/data2/diessner/'
scandir = osp.expanduser("/nfs/theoc/data2/diessner/MRSSMscans/")
dbdir = osp.join(homeprefix,"theorie/pointdbs/")
outdb = osp.join(dbdir,scanname+".db")
scanpath = osp.join(scandir,scanname)
Htemplate = osp.join(inprefix,'ScanTool/MSSM.template')
Hconf_process = osp.join(inprefix,'ScanTool/LHC-mssm.base')
SPhenodir = osp.join(inprefix,"SPheno-4.0.3/")

nofevents = 75000
analyses = [ "atlas13TeV"]
print outdb

parameter = ["m1", "m2", "m3", "mq2", "mq332", "ml2", 
                 "ml332", "mu2", "mu332", "md2", "md332", 
                 "me2", "me332",  "mu", "bmu", "tanbeta","Xe","Xd","Xu"]
para_types = ["real"]*len(parameter)

SPheno_MSSM = Run.SPheno_run(SPhenodir, "MSSM", 
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
    2 1.166370E-05    # G_F,Fermi constant 
    3 1.188000E-01    # alpha_s(MZ) SM MSbar 
    4 9.118760E+01    # Z-boson pole mass 
    5 4.180000E+00    # m_b(mb) SM MSbar 
    6 1.730700E+02    # m_top(pole) 
    7 1.776690E+00    # m_tau(pole) 
Block MINPAR      # Input parameters
3   {0[15]:E}  # TanBeta
Block EXTPAR      # Input parameters 
1 {0[13]:E}    # MuInput
7 {0[14]:E}   # BMuInput
8 {0[3]:E}    # mq2Input
9 {0[4]:E}    # mq233Input
10 {0[5]:E}    # ml2Input
11 {0[6]:E}    # ml233Input
12 {0[7]:E}   # mu2Input
13 {0[8]:E}    # mu233Input
14 {0[9]:E}    # md2Input
15 {0[10]:E}    # md233Input
16 {0[11]:E}    # me2Input
17 {0[12]:E}    # me233Input
21 {0[0]:E}    # M1Input
22 {0[1]:E}    # M2Input
23 {0[2]:E}    # M3Input
Block SPhenoInput   # SPheno specific input 
  1 -1              # error level 
  2  1              # SPA conventions 
  7  0              # Skip 2-loop Higgs corrections 
  8  3              # Method used for two-loop calculation 
  9  1              # Gaugeless limit used at two-loop 
 10  0              # safe-mode used at two-loop 
 11 1               # calculate branching ratios 
 13 1               # 3-Body decays: none (0), fermion (1), scalar (2), both (3) 
 14 0               # Run couplings to scale of decaying particle 
 12 1.000E-04       # write only branching ratios larger than this value 
 15 1.000E-30       # write only decay if width larger than this value 
 16 0              # One-loop decays 
 31 0              # fixed GUT scale (-1: dynamical GUT scale) 
 32 0               # Strict unification 
 34 1.000E-04       # Precision of mass calculation 
 35 40              # Maximal number of iterations
 36 5               # Minimal number of iterations before discarding points
 37 1               # Set Yukawa scheme  
 38 2               # 1- or 2-Loop RGEs 
 50 1               # Majorana phases: use only positive masses (put 0 to use file with CalcHep/Micromegas!) 
 51 0               # Write Output in CKM basis 
 52 1               # Write spectrum in case of tachyonic states 
 55 0               # Calculate loop corrected masses 
 57 0               # Calculate low energy constraints 
 65 1               # Solution tadpole equation 
 66 1               # Two-Scale Matching 
 67 1               # effective Higgs mass calculation 
 75 0               # Write WHIZARD files 
 76 0               # Write HiggsBounds file   
 77 0               # Output for MicrOmegas (running masses for light quarks; real mixing matrices)   
 78 0               # Output for MadGraph (writes also vanishing blocks)   
 86 0.              # Maximal width to be counted as invisible in Higgs decays; -1: only LSP 
510 0.              # Write tree level values for tadpole solutions 
515 0               # Write parameter values at GUT scale 
520 0.              # Write effective Higgs couplings (HiggsBounds blocks): put 0 to use file with MadGraph! 
521 0.              # Diphoton/Digluon widths including higher order 
525 0.              # Write loop contributions to diphoton decay of Higgs 
530 0.              # Write Blocks for Vevacious 
1101 1             # Include Glu in 1.loop corrections 
1102 1             # Include Fv in 1.loop corrections 
1103 1             # Include Chi in 1.loop corrections 
1104 1             # Include Cha in 1.loop corrections 
1105 1             # Include Fe in 1.loop corrections 
1106 1             # Include Fd in 1.loop corrections 
1107 1             # Include Fu in 1.loop corrections 
1201 1             # Include Sd in 1.loop corrections 
1202 1             # Include Sv in 1.loop corrections 
1203 1             # Include Su in 1.loop corrections 
1204 1             # Include Se in 1.loop corrections 
1205 1             # Include hh in 1.loop corrections 
1206 1             # Include Ah in 1.loop corrections 
1207 1             # Include Hpm in 1.loop corrections 
1301 1             # Include VG in 1.loop corrections 
1302 1             # Include VP in 1.loop corrections 
1303 1             # Include VZ in 1.loop corrections 
1304 1             # Include VWm in 1.loop corrections 
1401 1             # Include gG in 1.loop corrections 
1402 1             # Include gA in 1.loop corrections 
1403 1             # Include gZ in 1.loop corrections 
1404 1             # Include gWm in 1.loop corrections 
1405 1             # Include gWpC in 1.loop corrections 
1500 1               # Include Wave diagrams 1.loop corrections 
1501 1               # Include Penguin diagrams 1.loop corrections 
1502 1               # Include Box diagrams 1.loop corrections 
Block DECAYOPTIONS   # Options to turn on/off specific decays 
1    1     # Calc 3-Body decays of Glu 
2    1     # Calc 3-Body decays of Chi 
3    1     # Calc 3-Body decays of Cha 
4    1     # Calc 3-Body decays of Sd 
5    1     # Calc 3-Body decays of Su 
6    1     # Calc 3-Body decays of Se 
7    1     # Calc 3-Body decays of Sv 
1001 0     # Loop Decay of Sd 
1002 0     # Loop Decay of Su 
1003 0     # Loop Decay of Se 
1004 0     # Loop Decay of Sv 
1005 0     # Loop Decay of hh 
1006 0     # Loop Decay of Ah 
1007 0     # Loop Decay of Hpm 
1008 0     # Loop Decay of Glu 
1009 0     # Loop Decay of Chi 
1010 0     # Loop Decay of Cha 
1011 0     # Loop Decay of Fu 
1114 0.     # U-factors (0: off, 1:p2_i=m2_i, 2:p2=0, p3:p2_i=m2_1) 
1115 0.     # Use loop-corrected masses for external states 
1116 0.     # OS values for W,Z and fermions (0: off, 1:g1,g2,v 2:g1,g2,v,Y_i) 
1117 0.     # Use defined counter-terms 
1118 0.     # Use everywhere loop-corrected masses for loop-induced decays
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

def MSSM_LHC():
    tanb = 3 # range(2,61,2)
    m1 = 1
    m2 = 10000
    m3 = 5000
    mu = 10000
    ma2 = 100000000
    mq2 = 1000000
    ml2 = 100000000
    mu2 = 1000000
    md2 = 1000000
    me2 = 100000000
    mq332 = 100000000
    ml332 = 100000000
    mu332 = 100000000
    md332 = 100000000
    me332 = 100000000
    ae = 0
    ad = 0
    au = 0
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
    point = MSSM_LHC()
    points = []

    for x in range(1000,5001,400): # m1
        for y in range(400,2001,200): # msq
            pointtmp = point[:]
            pointtmp[0] = 0
            #pointtmp[13] = x
            #pointtmp[1] = y
            pointtmp[2] = 5000
            pointtmp[3] = x*x
            pointtmp[4] = y*y
            pointtmp[7] = x*x
            pointtmp[8] = y*y
            pointtmp[9] = x*x
            pointtmp[10] = y*y
            points.append(pointtmp)
    print len(points)
    switches = [0,0,1,0,0,0,0]
    print scanpath,dbdir
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
    
    CMfile = osp.join(cmevents,"CM.dat")        
    slhafile = osp.join(cmevents, "SPheno.spc.MSSM")
    SLHA.flavor_order(slhafile)
    lhepath = None
    Hconfigbase = Hconf_process
    lhc.full_herwig(slhafile,name,hevents,Hcardname,Hconfigtmp,Hconfigbase,
                    Htemplate, hepmcpath, nofevents)
    if cm:
        #sigma,Kfac = lhc.get_Kfac("SPheno.spc.MSSM", cmevents, "sqsum")
        #if sigma>0:
        #    lhc.CM_run(name,cmevents,analyses,hepmcpath,CMfile,
        #               nofevents,sigma=sigma,cleanup=False)
        #else: 
       	lhc.CM_run(name,cmevents,analyses,hepmcpath,CMfile,
                      nofevents,cleanup=True)

lhc_out = partial(Run.write_more_wrapper, read_CM2, 'lhc')
spheno_run = partial(Run.run_base, SPheno_MSSM)
lhc_run = partial(Run.run_base, lhc_study) # (lhc_study,
lhc_write = partial(Run.run_base, lhc_out)
lhc_table = partial(Init.table_init, 'lhc', zip(['analysis','r','cl'],
                                                ['text','real','real']))

masses_table = partial(Init.table_init, 'masses', zip(masspar, ['real']*len(masspar)))
masses_write = partial(Run.run_base, write_masses)

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


slepton_run = partial(Run.run_base, slepton_mass)

if __name__ == "__main__":
    start = time.time()
    #scaninit()
    #spheno_run(scanpath, outdb, parallel=True,ncores=10)
    
    # slepton_run(scanpath,outdb,parallel=False)
    #lhc_run(scanpath, outdb, parallel=True,ncores=15)
    
    #lhc_table(outdb)
    masses_table(outdb)
    masses_write(scanpath, outdb)
    #lhc_write(scanpath, outdb)
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
