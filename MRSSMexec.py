import datetime
import time
import os.path as osp
import numpy as np
from functools import partial
import MRSSMroutines as mrr 
import MRSSMfunctions as mrf
import Init
from Run import adaptive_scan

scanname = "bm4paper_lhc_mud_muu_light_staus"
# "bm5paper_higgs_mdw+ms2"
# "bm4paper_lhc_mud_muu_light_staus"
# "bm4paper_lhc_mud_muu_light_sleptons"


# lhc_mus_mdw_mdb50_light_rsleptons
# "lhc_rsleptons200_300_excl" # "light_singlet_offdiag" # "bm4_2d_mixing""bm6_lhc_mud_mdw"
#"2d2lnew" # "lightsingletlhcm1m2" #"bm4_lhc_mud_mdw" # "light_singlet_large_mus"
#lhc_mud_mstau_mdb50_heavy_sleptons
scandir1 = osp.expanduser("~/zihfast/MRSSMscans/")
scandir2 = osp.expanduser("~/raid2/MRSSMscans/")
dbdir = osp.expanduser("~/raid1/pointdbs/")
outdb = osp.join(dbdir,scanname+".db")
newscanpath = (osp.join(scandir2,scanname), osp.join(scandir2,scanname))
scanpath = newscanpath[1]
switches = [0,1,1,0,1,0,0]
parameter = ["tanb", "lamsd", "lamsu", "lamtd", "lamtu", "mud",
             "muu", "bmu", "mq2", "mq332", "ml2", 
             "ml332", "mu2", "mu332", "md2", "md332", 
             "me2", "me332", "mru2", "mrd2", "mo2", 
             "mbdrc", "mwdrc", "modrc", "ms2", "mt2"]
para_types = ["real"]*len(parameter) 
print outdb

def scan2Dinit(scanpath,makedb=True):
    points = []
    mbdrc = range(1,61,2)
    mwdrc = range(200,2100,50)
    muu = range(100,2100,50)
    mud = range(200,2100,50)
    mru2 = range(100000,4020000,100000)
    mrd2 = range(100000,4020000,100000)
    lamtd = [float(x)/10. for x in xrange(-20,21,1)]
    lamtu = [float(x)/10. for x in xrange(-20,21,1)]
    lamsu = [float(x)/1000. for x in xrange(-50,51,1)]

    tanb = [2,3,6]+range(10,51,5)
    ms2 = [x*x for x in range(0,120,5)]
    bmu = [x*x for x in range(100,1600,50)]
    me2 = [x*x for x in range(80,260,10)]
    ml2 = [x*x for x in range(100,1600,100)]
    mq2 = [x*x for x in range(1000,2600,100)]
    inds= [0,3,4,5,6,7,8,10,12,16,21,22,24]
    mrssm_value_arrays = [tanb,lamtd,lamtu,mud,muu,bmu,mq2,ml2,
                          mq2,me2,mbdrc,mwdrc,ms2]
    inds= [2,6,21,24]
    mrssm_value_arrays = [mud,muu,mbdrc]
    print reduce(lambda x,y: x+y, [len(x) for x in mrssm_value_arrays])
    for bm in BM4,BM5,BM6:
        point = bm()
        for x in range(len(mrssm_value_arrays)-1):
            for y in range(x+1,len(mrssm_value_arrays)):
                points.extend(scan_2D(point,mrssm_value_arrays[x],
                                      mrssm_value_arrays[y],inds[x],inds[y]))
    print len(points)
    Init.init_struc(points, scanpath, zip(parameter,para_types), 
              switches, createSLHAinMRSSMfull, dbdir,makedb=True)
    
def scan_init(scanpath,makedb=True):
    point = mrf.BM5()
    points = []
    # mu332 = 2500*2500
    
    lamsu = -0.01
    # lamtu = -1.1
    # point[1:5] = [lamsu,lamsu,lamsu,lamsu] # lambdas 
    #point[9] =  mu332 # stops
    #point[13] =  mu332 # squark
    #point[15] =  mu332 # sbottom
    #point[-2] = 80*80 # mS2
    #point[-5] = 20 # MDB
    # for x in [float(i)/20. for i in xrange(-30,1,1)]: # Lambda
    #     for y in range(0,50,1): # md1
    #         for z in [i*i for i in range(0,100,2)]: # mS2
    #             for a in [0,-100,-400,-2500,-6400,100,400,2500,6400]:
    #             #[float(i)/1000. for i in xrange(-60,40,2)]: # off diag
    #                 pointtmp = point[:]
    #                 pointtmp[4]= x
    #                 pointtmp[-5] = y
    #                 pointtmp[-2] = z
    #                 pointtmp[2]= (a/246.-0.362*y)/(np.sqrt(2)*700)
    #                 points.append(pointtmp)
    # for x in range(200,1501,50): # muu mud
    #     for y in range(1000,3001,200): # msq12
    #         pointtmp = point[:]
    #         pointtmp[5] = x
    #         pointtmp[6] = x
    #         pointtmp[8] = y*y
    #         pointtmp[12] = y*y
    #         pointtmp[14] = y*y
    #         points.append(pointtmp)
    # point[-4] = 500 # mdw
    # # point[5] = 300 # mud
    # # point[6] = 300 # muu
    # point[16] = 800*800 # me2
    # point[17] = 100*100 # me332
    # for x in range(100,600,50): # mud
    #     for y in range(100,600,50): # muu
    #         pointtmp = point[:]
    #         pointtmp[5] = x
    #         # pointtmp[16] = y*y
    #         pointtmp[6] = y
    #         points.append(pointtmp)
    # for x in range(175,426,50): # mud
    #     y=x-50
    #     # for y in range(50,451,50): # me3 mwdrc
    #     pointtmp = point[:]
    #         # pointtmp[16] = y*y
    #     pointtmp[17] = y*y
    #     # pointtmp[21] = x
    #     pointtmp[5] = x 
    #         # pointtmp[6] = 600
    #         # pointtmp[-4] = 600
    #         # pointtmp[-5] = 50
    #         # pointtmp[16] = 400 * 400
    #         #  pointtmp[17] = y * y
    #     points.append(pointtmp)
    for x in range(0,161,1):
        pointtmp = point[:]
        pointtmp[-5] = x
        points.append(pointtmp)
    for x in range(0,161,1):
        pointtmp = point[:]
        pointtmp[-2] = x*x
        points.append(pointtmp)
        
    # for x in xrange(100,5001,100): # m3
    #     for y in [2000,10000]:  # mo2
    #         pointtmp = copy.deepcopy(point)
    #         pointtmp[-3] = x
    #         pointtmp[-6] = y*y
    #         points.append(pointtmp)
    # points = [mrf.BM4(),mrf.BM5(), mrf.BM6()]
    print len(points)
    if type(scanpath) in (list,tuple):
        Init.init_struc(points, scanpath[0], zip(parameter, para_types), 
                        switches, mrf.createSLHAinMRSSMfull, dbdir,makedb=makedb)
        
        Init.init_struc(points, scanpath[1], zip(parameter, para_types), 
                        switches, mrf.createSLHAinMRSSMfull, dbdir,makedb=False)     
    else:
        Init.init_struc(points, scanpath, zip(parameter, para_types), 
                        switches, mrf.createSLHAinMRSSMfull, dbdir,makedb=makedb)

def scan2l_init(scanpath):
    points = []
    params = [1,2,4]
    ranges=[[float(x)/10. for x in xrange(-20,21,1)],
            [float(x)/10. for x in xrange(-20,21,1)],
            [float(x)/10. for x in xrange(-20,21,1)]]
    for point in [BM1(),BM2(),BM3(),BM4()]:
        print len(points)
        for i in xrange(len(params)):
            for value in ranges[i]:
                pointtmp = point[:]
                pointtmp[params[i]] = value
                points.append(pointtmp)
    Init.init_struc(points, scanpath, zip(parameter, para_types),
                    switches, createSLHAinMRSSMfull, dbdir,makedb=True)


def adapt_sleptons(val,value,param):
    comb1 = param[0]-val[0]**2
    return [comb1+value[0]]
    # comb1 = [param[0]-val[0]**2, param[1]-val[1]**2]
    # comb2 = [param[0]-val[1]**2, param[1]-val[0]**2]
    # print comb1, comb2
    # goal = value[:2]#((val[-2]+val[-1])/2.)**2
    # if abs(comb1[0])+abs(comb1[1]) < abs(comb2[0])+abs(comb2[1]):
    #     return [comb1[0]+goal[0]**2,comb1[1]+goal[1]**2]
    # else:
    #     return [comb2[0]+goal[0]**2,comb2[1]+goal[1]**2]

def slepton_mass(i,scandir):
    # fit1 = adaptive_scan([["me332","EXTPAR",["17"]],["me2","EXTPAR",["16"]]],
    #                      [["se1","MASS",["1000011"]],["se3","MASS",["1000015"]]],
    #                      [100,100], adapt_sleptons,
    #                          Init.changemultiparameter,
    #                   mrf.SPheno_MRSSM)
    fit1 = adaptive_scan([["me332","EXTPAR",["17"]]],
                         [["se1","MASS",["1000011"]]],
                         [10000], adapt_sleptons,
                             Init.changemultiparameter,
                      mrf.SPheno_MRSSM)
    fit1(i, scandir)

slepton_run = partial(mrr.run_base, slepton_mass)

if __name__ == "__main__":
    start = time.time()
    # scan_init(scanpath,makedb=True)
    # scan2l_init(scanpath)
    # scan2Dinit(scanpath)
    # mrr.spheno_run(scanpath, outdb, parallel=True)
    # slepton_run(scanpath,outdb,parallel=False)

    # mrr.mass_table(outdb)
    # mrr.zhmix_table(outdb)
    # mrr.masses_write(scanpath, outdb)
    # mrr.zhmix_write(scanpath, outdb)
    # mrr.hbhs_table(outdb)
    # mrr.hbhs_run(scanpath, outdb, parallel=True)
    # mrr.run_mg()
    mrr.lhc_table(outdb)
    mrr.lhc_run(scanpath, outdb, parallel=True)
    # mrr.lhc_write(scanpath,outdb)
    # mrr.dm_table(outdb)
    # mrr.dm_run(scanpath, outdb,parallel=True)
    end = time.time()
    
    diff = end - start
    print datetime.timedelta(seconds=diff)
    m, s = divmod(diff, 60)
    h, m = divmod(m, 60)
    print "%d:%02d:%02d" % (h, m, s)
