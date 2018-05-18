import os.path as osp 
import scans

## exec
scanfunc = scans.scan_init

scanname = "implem_test"
scandir1 = osp.expanduser("/nfs/theoc/data2/diessner/MRSSMscans")
scandir2 = osp.expanduser("/nfs/theoc/data2/diessner/MRSSMscans")
# Herwig scanning allows two paths
dbdir = osp.expanduser("~/theorie/pointdbs/")
switches = [0,1,1,0,0,0,0] # 2l(0 is yes),calc BR, 1L, low energy,HB files, vevac, finetuning
parameter = ["tanb", "lamsd", "lamsu", "lamtd", "lamtu", "mud",
             "muu", "bmu", "mq2", "mq332", "ml2", 
             "ml332", "mu2", "mu332", "md2", "md332", 
             "me2", "me332", "mru2", "mrd2", "mo2", 
             "mbdrc", "mwdrc", "modrc", "ms2", "mt2"]
             #,"mq212","mq213","mq223"
             #,"mu212","mu213","mu223","md212","md213","md223","mq222","mu222","md222"]
para_types = ["real"]*len(parameter) 

## functions
inprefix = '/nfs/theoc/data/diessner/'
outprefix = '/nfs/theoc/data2/diessner/'
homeprefix = '/afs/desy.de/user/d/diessner/'
analyses = [ "atlas13TeV"]
nofevents = 150000
strongLHCstudy= False
if strongLHCstudy:
    Hconf_process = osp.join(inprefix,'ScanTool/LHC-mrssm.base.strong')
    SPhenodir = osp.join(inprefix,"SPheno-4.0.3/")
else:
    Hconf_process = osp.join(inprefix,'ScanTool/LHC-mrssm.base.ewinos')
    SPhenodir = osp.join(inprefix,"SPheno-4.0.3.alt/")
Htemplate = osp.join(inprefix,'ScanTool/MRSSM.template')
mg_process = '/home/diessner/raid2/MG5_aMC_v2_1_1/ewino_speedtest/'
HBdir = "/home/diessner/raid2/HiggsBounds-4.3.1/"
HSdir = "/home/diessner/raid2/HiggsSignals-1.4.0/"
uncerfile = osp.join(inprefix,"ScanTool/MHall_uncertainties.dat")
dmexecut= osp.join(inprefix,"micromegas_5.0.2/MRSSM/CalcOmega_with_DDetection")
# only SPheno, micromegas functional

## LHC studies
CMpath = "/nfs/theoc/data/diessner/CheckMATEbeta-2.0.23/bin/CheckMATE"
nllpath = "/nfs/theoc/data/diessner/nnllfast-1.1"
NLL="/nfs/theoc/data/diessner/nnllfast-1.1/nnllfast"
# for Herwig the activate script has to be used and no local path are required

## LHC NLO studies
MGpath = "/theoc/theoc-fs01/data/diessner/madgraph/"

## Herwigoutputparser
fi = "/nfs/theoc/data2/MRSSMscans/lhc_bmtest/3/lhc.out"

