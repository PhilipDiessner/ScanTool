import os.path as osp
import copy
import sqlite3
import numpy as np
from functools import partial
import shutil
import Init
import Run
import LHCstudies as lhc
import SLHA_extract_values as SLHA

analyses = [ "atlas_conf_2013_049","atlas_1402_7029",
                 "atlas_conf_2013_035","atlas_conf_2013_036", "atlas_1403_5294"]
nofevents = 100000
Hconf_process = '/home/diessner/raid1/ScanTool/LHC-mrssm.base.ewinos'

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
    2 1.166379E-05    # G_F,Fermi constant 
    3 1.188000E-01    # alpha_s(MZ) SM MSbar 
    4 9.118760E+01    # Z-boson pole mass 
    5 4.180000E+00    # m_b(mb) SM MSbar 
    6 1.730700E+02    # m_top(pole) 
    7 1.776690E+00    # m_tau(pole) 
Block MINPAR      # Input parameters 
3  {0[0]:E}     # TanBeta
Block EXTPAR      # Input parameters 
1 {0[1]:E}     # LSDinput
2 {0[2]:E}     # LSUinput
3 {0[3]:E}     # LTDinput
4 {0[4]:E}     # LTUinput
5 {0[5]:E}     # MuDinput
6 {0[6]:E}     # MuUinput
7 {0[7]:E}     # BMuinput
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
 52 0              # Write spectrum in case of tachyonic states 
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
520 0               # Write effective Higgs couplings (HiggsBounds blocks) 
525 {1[4]}              # Write loop contributions to diphoton decay of Higgs 
530 {1[5]}              # Write Blocks for Vevacious 
550 {1[6]}              # Calculate Fine-Tuning
1101 1             # Include Glu in 1.loop corrections
1102 1             # Include Fv in 1.loop corrections
1103 1             # Include Chi in 1.loop corrections
1104 1             # Include Cha1 in 1.loop corrections
1105 1             # Include Cha2 in 1.loop corrections
1106 1             # Include Fe in 1.loop corrections
1107 1             # Include Fd in 1.loop corrections
1108 1             # Include Fu in 1.loop corrections
1201 1             # Include SOc in 1.loop corrections
1202 1             # Include Sd in 1.loop corrections
1203 1             # Include Sv in 1.loop corrections
1204 1             # Include Su in 1.loop corrections
1205 1             # Include Se in 1.loop corrections
1206 1             # Include hh in 1.loop corrections
1207 1             # Include Ah in 1.loop corrections
1208 1             # Include Rh in 1.loop corrections
1209 1             # Include Hpm in 1.loop corrections
1210 1             # Include Rpm in 1.loop corrections
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
""".format(parameters,switches)

def BM1():
    tanb = 3 # range(2,61,2)
    ms2 = 2000**2 # [2]
    mbdrc = 600
    modrc = 1500
    mwdrc = 500
    mo2 = 1000000
    mru2 = 4000000
    mrd2 = 490000
    lamsd = 1.0
    lamsu = -0.8
    lamtd = -1.0
    lamtu = -1.2
    muu = 400
    mud = 400
    mt2 = 3000**2
    bmu = 500**2
    mq2 = 6250000
    ml2 = 1000000
    mu2 = 6250000
    md2 = 6250000
    me2 = 1000000
    mq332 = 1000000
    ml332 = 1000000
    mu332 = 1000000
    md332 = 1000000
    me332 = 1000000
    mrssm_value_arrays = [tanb,lamsd,lamsu,lamtd,lamtu,mud,muu,bmu,
                          mq2,mq332,ml2,ml332,
                          mu2,mu332,md2,md332,me2,me332,
                          mru2,mrd2,mo2,
                          mbdrc,mwdrc,modrc,ms2,mt2]
    return mrssm_value_arrays

def BM2():
    tanb = 10 # range(2,61,2)
    ms2 = 2000**2 # [2]
    mbdrc = 1000
    modrc = 1500
    mwdrc = 500
    mo2 = 1000000
    mru2 = 1000000
    mrd2 = 490000
    lamsd = 1.1
    lamsu = -1.1
    lamtd = -1.0
    lamtu = -1.0
    muu = 400
    mud = 400
    mt2 = 3000**2
    bmu = 300**2
    mq2 = 6250000
    ml2 = 1000000
    mu2 = 6250000
    md2 = 6250000
    me2 = 1000000
    mq332 = 1000000
    ml332 = 1000000
    mu332 = 1000000
    md332 = 1000000
    me332 = 1000000
    mrssm_value_arrays = [tanb,lamsd,lamsu,lamtd,lamtu,mud,muu,bmu,
                          mq2,mq332,ml2,ml332,
                          mu2,mu332,md2,md332,me2,me332,
                          mru2,mrd2,mo2,
                          mbdrc,mwdrc,modrc,ms2,mt2]
    return mrssm_value_arrays

def BM3():
    tanb = 40 # range(2,61,2)
    ms2 = 2000**2 # [2]
    mbdrc = 250
    modrc = 1500
    mwdrc = 500
    mo2 = 1000000
    mru2 = 1000000
    mrd2 = 490000
    lamsd = 0.15
    lamsu = -0.15
    lamtd = -1.0
    lamtu = -1.15
    muu = 400
    mud = 400
    mt2 = 3000**2
    bmu = 40000
    mq2 = 6250000
    ml2 = 1000000
    mu2 = 6250000
    md2 = 6250000
    me2 = 1000000
    mq332 = 1000000
    ml332 = 1000000
    mu332 = 1000000
    md332 = 1000000
    me332 = 1000000
    mrssm_value_arrays = [tanb,lamsd,lamsu,lamtd,lamtu,mud,muu,bmu,
                          mq2,mq332,ml2,ml332,
                          mu2,mu332,md2,md332,me2,me332,
                          mru2,mrd2,mo2,
                          mbdrc,mwdrc,modrc,ms2,mt2]
    return mrssm_value_arrays

def BM4():
    tanb = 40 # range(2,61,2)
    ms2 = 30**2# [2]
    mbdrc = 50
    modrc = 1500
    mwdrc = 600
    mo2 = 1000000
    mru2 = 1000000
    mrd2 = 490000
    lamsd = 0.01
    lamsu = -0.01
    lamtd = -1.0
    lamtu = -1.2
    muu = 600
    mud = 400
    mt2 = 3000**2
    bmu = 40000
    mq2 = 1500*1500
    ml2 = 800*800
    mu2 = 1500*1500
    md2 = 1500*1500
    me2 = 800*800
    mq332 = 700*700
    ml332 = 800*800
    mu332 = 700*700
    md332 = 1000*1000
    me332 = 130*130
    mrssm_value_arrays = [tanb,lamsd,lamsu,lamtd,lamtu,mud,muu,bmu,
                          mq2,mq332,ml2,ml332,
                          mu2,mu332,md2,md332,me2,me332,
                          mru2,mrd2,mo2,
                          mbdrc,mwdrc,modrc,ms2,mt2]
    return mrssm_value_arrays

def BM5():
    tanb = 20 # range(2,61,2)
    ms2 = 40**2# [2]
    mbdrc = 44
    modrc = 1500
    mwdrc = 500
    mo2 = 1000000
    mru2 = 1000000
    mrd2 = 490000
    lamsd = 0
    lamsu = -0.01
    lamtd = -1.0
    lamtu = -1.15
    muu = 550
    mud = 400
    mt2 = 3000**2
    bmu = 40000
    mq2 = 1300*1300
    ml2 = 1000000
    mu2 = 1300*1300
    md2 = 1300*1300
    me2 = 1000*1000
    mq332 = 700*700
    ml332 = 1000000
    mu332 = 700*700
    md332 = 1000*1000
    me332 = 1000*1000
    mrssm_value_arrays = [tanb,lamsd,lamsu,lamtd,lamtu,mud,muu,bmu,
                          mq2,mq332,ml2,ml332,
                          mu2,mu332,md2,md332,me2,me332,
                          mru2,mrd2,mo2,
                          mbdrc,mwdrc,modrc,ms2,mt2]
    return mrssm_value_arrays

def BM6(): 
    tanb = 6 # range(2,61,2)
    ms2 = 80**2# [2]
    mbdrc = 30
    modrc = 1500
    mwdrc = 400
    mo2 = 1000000
    mru2 = 1000000
    mrd2 = 490000
    lamsd = 0
    lamsu = -0.0
    lamtd = -1.0
    lamtu = -1.2
    muu = 550
    mud = 550
    mt2 = 3000**2
    bmu = 500*500
    mq2 = 1400*1400
    ml2 = 500*500
    mu2 = 1400*1400
    md2 = 1400*1400
    me2 = 350*350
    mq332 = 700*700
    ml332 = 700*700
    mu332 = 700*700
    md332 = 1000*1000
    me332 = 95*95
    mrssm_value_arrays = [tanb,lamsd,lamsu,lamtd,lamtu,mud,muu,bmu,
                          mq2,mq332,ml2,ml332,
                          mu2,mu332,md2,md332,me2,me332,
                          mru2,mrd2,mo2,
                          mbdrc,mwdrc,modrc,ms2,mt2]
    return mrssm_value_arrays

# pass arguments to partial_runwrapper derived functions, have i, scandir
# as usual argument
SPheno_MRSSM = Run.SPheno_run("/home/diessner/raid2/SPheno-3.3.6/", "MRSSM", 
                             "{0}.SLHA.in", "SPheno.spc.MRSSM")
HB_MRSSM = Run.HB_run("/home/diessner/raid2/HiggsBounds-4.2.0/", 7, 3, "")
HS_MRSSM = Run.HS_run("/home/diessner/raid2/HiggsSignals-1.3.1/", 7, 3, "")

def hbhs_uncertain_file(i,scandir):
    uncerfile = osp.expanduser("~/raid1/ScanTool/MHall_uncertainties.dat")
    shutil.copy2(uncerfile, osp.join(scandir, Init.ident_to_path(i)))
    
def run_dm(i,scandir):
    execut= "/home/diessner/raid2/micromegas_4.1.8/MRSSM/CalcOmega_with_DDetection"
    directory = osp.join(scandir, Init.ident_to_path(i))
    Run.runwrapper([execut], directory)

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
]

masspar = [x[0] for x in masses]

mixmatrix = [["zh11",'SCALARMIX',['1','1']],["zh12",'SCALARMIX',['1','2']],
             ["zh13",'SCALARMIX',['1','3']],["zh14",'SCALARMIX',['1','4']],
             ["zh21",'SCALARMIX',['2','1']],["zh22",'SCALARMIX',['2','2']],
             ["zh23",'SCALARMIX',['2','3']],["zh24",'SCALARMIX',['2','4']],
         ]

hmixpar = [x[0] for x in mixmatrix]

def read_CM(i,scandir):
    out = [lhc.read_CMresult(osp.join(scandir,Init.ident_to_path(i),'lhc_cm',
                                       "evaluation", "best_signal_regions.txt"),analysis)
            for analysis in analyses+['best']]
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

# derived functions to write to db
write_masses = partial(Run.write_wrapper,
                       partial(Run.read_param, masses, "SPheno.spc.MRSSM")
                       , "masses")
zhmix = partial(Run.write_wrapper,
                partial(Run.read_param, mixmatrix, "SPheno.spc.MRSSM")
                ,"hmix")
write_omega = partial(Run.write_wrapper, read_relic_out, 'relic',)
HBHS_write_wrapper = partial(Run.write_wrapper,Run.read_hbhs , 'hbhs')
lhc_out = partial(Run.write_more_wrapper, read_CM, 'lhc')

def scan_2D(point,ar1,ar2,ind1,ind2):
    out = []
    temp=point[:]
    for i in ar1:
        temp[ind1]=i
        for j in ar2:
            temp[ind2]=j
            out.append(temp[:])
    return out

def swapflag(db,scanp):
    comm = ('SELECT C.identifier, C.lamsd, C.lamsu' 
            'FROM (SELECT points.identifier, IFNULL(mhmw.mh1,0)' 
            'AS fls,points.lamsd, points.lamsu FROM points' 
            'LEFT OUTER JOIN mhmw ON points.identifier=mhmw.identifier) C' 
            'WHERE C.fls==0')
    pts = Init.points(db,comm)
    method = []
    for i in range(len(pts)-1):
        # if pts[i-1][0] == pts[i][0]-1 and pts[i+1][0] == pts[i][0]+1:
        #     continue
        # else:
        method.append(pts[i][0])
    print len(method)
    runfunc = Run.run_on_dir(scanp)
    twolchange = Init.changeSLHAwrapper(Init.changeoneparameter,
                                        ['2lmethod','SPhenoInput',['8']],1)
    runfunc(twolchange,method=method, parallel=False)

def mg_run(i,scandir):
    name = 'lhc'
    events = osp.join(scandir, str(i))
    cardname = osp.join(events, "MGcard.dat") 
    slhafile = osp.join(events, "SPheno.spc.MRSSM")
    mg_process = '/home/diessner/raid2/MG5_aMC_v2_1_1/ewino_speedtest/'
    lhc.genlhe(slhafile, mg_process,name,events,cardname,nofevents)
    
def lhc_study(i,scandir, mg = False, cm = True):
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
    Htemplate = '/home/diessner/raid1/ScanTool/MRSSM.template'
    
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
    lhc_study(14,
              '/amnt/remote/pkts08.raid2/users/diessner/MRSSMscans/bm5_lhc_mud_mdw',
              db='/home/diessner/raid1/pointdbs/bm5_lhc_mud_mdw.db')
