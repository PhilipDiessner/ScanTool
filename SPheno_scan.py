import numpy as np
# import scipy as scp
import subprocess as spr 
import multiprocessing as mp
import itertools as itr
import os
import time
import parallel
import random
import copy

def randomspectra(boundsarray,npoints,randfunc):
    for i in xrange(npoints):
        randoms = [ x[0] if (len(x)==1 or x[0] == x[1])
                    else round(x[0]+x[2](*x[3]),4) if len(x)>2
                    else round(x[0]+randfunc()*(x[1]-x[0] ),4) 
                    for x in boundsarray]
        yield randoms

def generator_points_wrapper(npoints, function):
    for i in xrange(npoints):
        yield function()
    
def generate_points_MRSSM_SPheno():
    tanb = 40
    mud = random.uniform(0,1500)
    muu = random.uniform(0,1500)
    mbdrc = random.uniform(0,1500)
    mwdrc = random.uniform(0,1500)
    ms2 = random.uniform(500000,5000000)
    mt2 = random.uniform(10000000,100000000)
    lamsd = random.uniform(-1,1)
    lamtd = random.uniform(-1,1)
    muu2=muu**2
    mbdrc2=mbdrc**2
    mwdrc2=mwdrc**2
    tu_down = (-5* mwdrc * muu - np.sqrt(33* mwdrc2* muu2 + 8* mt2* muu2))/(8. * muu2)
    tu_up = (-5* mwdrc * muu + np.sqrt(33* mwdrc2* muu2 + 8* mt2* muu2))/(8. * muu2)
    su_down =(-3* mbdrc * muu - np.sqrt(13* mbdrc2* muu2 + 4* ms2* muu2))/(8.* muu2)
    su_up =(-3* mbdrc * muu + np.sqrt(13* mbdrc2* muu2 + 4* ms2* muu2))/(8.* muu2)
    lamtu = random.uniform(tu_down,tu_up)
    lamsu = random.uniform(su_down,su_up)
    bmu = 90000
    mq2 = 1000000
    ml2 = 1000000
    mu2 = 1000000
    md2 = 1000000
    me2 = 1000000
    mo2 = 1000000
    mru2 = 1000000
    mrd2 = 1000000
    modrc = 800
    mgut=1000

    mrssm_value_array = [tanb,lamsd,lamsu,lamtd,lamtu,mud,muu,bmu,
                          mq2,ml2,mu2,md2,me2,
                          mru2,mrd2,mo2,
                          mbdrc,mwdrc,modrc,ms2,mt2,mgut]
    return mrssm_value_array

def randtodigits(digits):
    def returnfunc():
        return float(random.randrange(digits))/digits
    return returnfunc

def MRSSM_BM1():
    tanb = [40] # range(2,61,2)
    vs = [2000**2]# [2]
    mbdrc = [250]
    modrc = [1500]
    mwdrc = [500]
    mo2 = [1000000]
    mru2 = [1000000]
    mrd2 = [490000]
    lamsd = [0.15]
    lamsu = [-0.15]
    lamtd = [-1.0]
    lamtu = [-1.15]
    muu = [400]
    mud = [400]
    vt = [3000**2]
    bmu = [40000]
    mq2 =[6250000]
    ml2 =[1000000]
    mu2 =[6250000]
    md2 =[6250000]
    me2 =[1000000]
    mq332 =[1000000]
    ml332 =[1000000]
    mu332 =[1000000]
    md332 =[1000000]
    me332 =[1000000]
    mgut = [1000] # map(lambda x: 10**x,range(3,20))
    mrssm_value_arrays = [tanb,lamsd,lamsu,lamtd,lamtu,mud,muu,bmu,
                          mq2,mq332,ml2,ml332,
                          mu2,mu332,md2,md332,me2,me332,
                          mru2,mrd2,mo2,
                          mbdrc,mwdrc,modrc,vs,vt,mgut]
    return mrssm_value_arrays

def MRSSM_BM3():
    tanb = [3] # range(2,61,2)
    vs = [2000**2]# [2]
    mbdrc = [600]
    modrc = [1500]
    mwdrc = [500]
    mo2 = [1000000]
    mru2 = [4000000]
    mrd2 = [490000]
    lamsd = [1.0]
    lamsu = [-0.8]
    lamtd = [-1.0]
    lamtu = [-1.2]
    muu = [400]
    mud = [400]
    vt = [3000**2]
    bmu = [500**2]
    mq2 =[6250000]
    ml2 =[1000000]
    mu2 =[6250000]
    md2 =[6250000]
    me2 =[1000000]
    mq332 =[1000000]
    ml332 =[1000000]
    mu332 =[1000000]
    md332 =[1000000]
    me332 =[1000000]
    mgut = [1000] # map(lambda x: 10**x,range(3,20))
    mrssm_value_arrays = [tanb,lamsd,lamsu,lamtd,lamtu,mud,muu,bmu,
                          mq2,mq332,ml2,ml332,
                          mu2,mu332,md2,md332,me2,me332,
                          mru2,mrd2,mo2,
                          mbdrc,mwdrc,modrc,vs,vt,mgut]
    return mrssm_value_arrays

def MRSSM_BM2():
    tanb = [10] # range(2,61,2)
    vs = [2000**2]# [2]
    mbdrc = [1000]
    modrc = [1500]
    mwdrc = [500]
    mo2 = [1000000]
    mru2 = [1000000]
    mrd2 = [490000]
    lamsd = [1.1]
    lamsu = [-1.1]
    lamtd = [-1.0]
    lamtu = [-1.0]
    muu = [400]
    mud = [400]
    vt = [3000**2]
    bmu = [300**2]
    mq2 =[6250000]
    ml2 =[1000000]
    mu2 =[6250000]
    md2 =[6250000]
    me2 =[1000000]
    mq332 =[1000000]
    ml332 =[1000000]
    mu332 =[1000000]
    md332 =[1000000]
    me332 =[1000000]
    mgut = [1000] # map(lambda x: 10**x,range(3,20))
    mrssm_value_arrays = [tanb,lamsd,lamsu,lamtd,lamtu,mud,muu,bmu,
                          mq2,mq332,ml2,ml332,
                          mu2,mu332,md2,md332,me2,me332,
                          mru2,mrd2,mo2,
                          mbdrc,mwdrc,modrc,vs,vt,mgut]
    return mrssm_value_arrays

def highscale_MRSSM():
    spheno_switches = [1,1,1000,0,0,0]
    model = "MRSSM"
    tanb = [50] # range(2,61,2)
    vs = [250000]# [2]
    mbdrc = [250]
    modrc = [1500]
    mwdrc = [500]
    mo2 = [1000000]
    mru2 = [1000000]
    mrd2 = [1000000]
    lamsd = [0.15]
    lamsu = [-0.15]
    lamtd = np.arange(-2,2.01,0.1)
    lamtu = [-1.15]
    muu = [400]
    mud = [400]
    vt = [2500**2]
    bmu = [1000]
    mq2 =[6250000]
    ml2 =[1000000]
    mu2 =[6250000]
    md2 =[6250000]
    me2 =[1000000]
    mq332 =[1000000]
    ml332 =[1000000]
    mu332 =[1000000]
    md332 =[1000000]
    me332 =[1000000]
    mgut = [1000] # map(lambda x: 10**x,range(3,20))
    mrssm_value_arrays = MRSSM_BM1()
    mrssm_value_arrays[4]=lamtd
    mrssm_value_arrays[-1]=[90]
    bounds = [[10],[1],[1],[1],[1],[100],[-200],[50000],
              [10000000],[10000000],[10000000],[10000000],[10000000],
              [500000],[500000],[10000000],
              [-150],[150],[400],[2],[1], map(lambda x: 10**x,range(3,17))]
    bounds = [[40,40],[-2,2],[-2,2],[-2,2],[-2,2],[0,1500],[0,1500],[50000,5000000],
                [10000000,10000000],[10000000,10000000],[10000000,10000000],[10000000,10000000],[10000000,10000000],
               [500000,500000],[500000,500000],[10000000,10000000],
               [0,1500],[0,1500],[800,800],[500000,40000000],[40000000,40000000],[1000,1000]]
    npoints = 50000
    cond=[[19,19],[[0,[2,2,6,6],16],[0,[2,6,16],8]]]
    
    # npoints = reduce(lambda x,y: x*y,map(len,mrssm_value_arrays))
    # mrssm_scan_array = generator_points_wrapper(npoints, generate_points_MRSSM_SPheno) 
    # goodspectrafile= "/home/diessner/research/phd/rsymmetry/mrssm_n2_tree_randscan.txt"
    # mrssm_scan_array = goodspectra(goodspectrafile)
    mrssm_scan_array = itr.product(*mrssm_value_arrays)
    sphenodir = "/home/diessner/raid2/SPheno/"
    indir =  "/home/diessner/zihfast/MRSSMmstscan/"
    # # indir = sphenodir
    outdir = "/home/diessner/zihfast/MRSSMmsmtspc/"
    working_points = "/home/diessner/research/phd/rsymmetry/MRSSMv0workingpts.txt"
    log =indir + "tachyon_tree_log" 
    # points = 0 #len(mrssm_scan_array)
    SPheno_scan_seq(sphenodir,SPheno_point, model, indir, outdir, spheno_switches,mrssm_scan_array,log,
                     SPheno_create_infile_MRSSM_highenergy,working_points,points=npoints)


def lowscale_MRSSM_Flex():
    spheno_switches = [1,1]
    model = "MRSSM"
    tanb = [2,10,30,50]
    vs = [1,200]
    mbdrc = [200]
    modrc = [400]
    mwdrc = [200]
    mo2 = [10000000]
    mru2 = [100000]
    mrd2 = [100000]
    mr12= map(lambda x: 9*10**x,[4,5,6,7,8])
    mr22= map(lambda x: 9*10**x,[4,5,6,7,8])
    lamsd = [0.5,1,1.5]
    lamsu = [-0.5,-1,-1.5]
    lamtd = [0.5, 1,1.5]
    lamtu = [0.5,1,1.5]
    lamda = map(lambda x: x/10.,range(-25,26))
    muu = [250]
    mud = [250]
    vt = [1]
    bmu = [50000]
    mstop2 = [250000,4000000]
    bounds = [[1,50],[1,1],[100,100],[400,400],[100,100],[1000000,1000000],[50000,50000],
              [50000,50000],[-1,1],[-1,1],[-1,1],[-1,1],[250,250],[250,250],[1,1],[10000,10000],[100000,100000],[1000,1000]]
    mrssm_scan_array=[]
    # for lam in lamda:
    #     for tan in tanb:
    #         mrssm_scan_array.append([tan,1,200,2000,200,10000000,5000000,5000000,lam,-lam,-lam,lam,-250,-250,2,5000,1000000,1000000])
    #     for v in vs:
    #         mrssm_scan_array.append([15,v,200,2000,200,10000000,5000000,5000000,lam,-lam,-lam,lam,-250,-250,2,5000,1000000,1000000])
    #     for mdrc in mbdrc:
    #         mrssm_scan_array.append([15,1,mdrc,2000,200,10000000,5000000,5000000,lam,-lam,-lam,lam,-250,-250,2,5000,1000000,1000000])
    #     for mdrc in mbdrc:
    #         mrssm_scan_array.append([15,1,200,2000,mdrc,10000000,5000000,5000000,lam,-lam,-lam,lam,-250,-250,2,5000,1000000,1000000])
    #     for mu in muu:
    #         mrssm_scan_array.append([15,1,200,2000,200,10000000,5000000,5000000,lam,-lam,-lam,lam,mu,-250,2,5000,1000000,1000000])   
    #     for mu in muu:
    #         mrssm_scan_array.append([15,1,200,2000,200,10000000,5000000,5000000,lam,-lam,-lam,lam,-250,mu,2,5000,1000000,1000000])
    #     for bm in bmu:
    #         mrssm_scan_array.append([15,1,200,2000,200,10000000,5000000,5000000,lam,-lam,-lam,lam,-250,-250,2,bm,1000000,1000000])   
    #     for mst2 in mstop2:
    #         mrssm_scan_array.append([15,1,200,2000,200,10000000,5000000,5000000,lam,-lam,-lam,lam,-250,-250,2,5000,mst2,mst2])
    #randfunc = randtodigits(10000)
    #print randfunc()
    #randompoints = randomspectra(bounds,100,random.random)
    #for x in randompoints:
    #    print x
    mrssm_value_arrays = [tanb,vs,mbdrc,modrc,mwdrc,mo2,mr12,mr22,lamsd,lamsu,lamtd,lamtu,muu,mud,
                           vt,bmu]
    npoints = 200*3**4 # 00000
    # for x in mrssm_value_arrays:
    #     npoints =npoints*len(x)
    mrssm_scan_array = itr.product(*mrssm_value_arrays)
    # goodspectrafile= "/home/diessner/research/phd/rsymmetry/mrssm_scan_tree_allowed_main.txt"
    # mrssm_scan_array = goodspectra(goodspectrafile)
    # mrssm_scan_array = randomspectra(bounds,npoints,random.random)
    flexdir = "/home/diessner/raid1/FlexibleSUSY/"
    indir =  "/home/diessner/zihfast/MRSSMmrhscan/"
    # # indir = sphenodir
    outdir = "/home/diessner/zihfast/MRSSMmrhloopspc/"
    log =indir+"tachyon_tree_log" 
    # points = 0 #len(mrssm_scan_array)
    # npoints = len(mrssm_scan_array)
    SPheno_scan_par(flexdir, Flex_point,model, indir, outdir, spheno_switches,mrssm_scan_array,
                    log, FlexSUSY_create_infile_MRSSM_low,points=npoints)

def scan_2D(point,ar1,ar2,ind1,ind2):
    out = []
    temp=point[:]
    for i in ar1:
        temp[ind1]=i
        for j in ar2:
            temp[ind2]=j
            if temp != point:
                out.append(temp[:])
    return out

def highscale_MRSSM_onepoint():
    spheno_switches = [1,1,1000,0,0,0]
    model = "MRSSM"
    tanb = [0.5,1.1,2,3,4,5,10,15,20,30,50] # range(2,61,2)
    vs = [1]# [2]
    mbdrc = range(50,2100,100)
    modrc = [500]
    mwdrc = range(50,2100,100)
    mo2 = [1000000]
    mru2 = range(100000,4020000,100000)
    mrd2 = range(100000,4020000,100000)
    lamsd = np.arange(-2,2.1,0.1)
    lamsu = np.arange(-2.05,2.1,0.1)
    lamtd = np.arange(-2,2.1,0.1)
    lamtu = np.arange(-2.0,2.1,0.1)
    muu = range(100,2100,100)
    mud = range(50,2100,100)
    vt = map(lambda x: x/10.,range(2,10))+range(2,10)
    bmu = [50000]
    mq2 =[10000000]
    ml2 =[10000000]
    mu2 =[10000000]
    md2 =[10000000]
    me2 =[10000000]
    ms2 = range(100000,5010000,100000)
    mt2 = range(100000,10200000,250000)
    mgut = [1000] # map(lambda x: 10**x,range(3,20))
    point = [item for sublist in MRSSM_BM1() for item in sublist]
    print len(point)
    inds=range(0,7)+[-9,-8,-6,-5,-3,-2]
    mrssm_value_arrays = [tanb,lamsd,lamsu,lamtd,lamtu,mud,muu,mrd2,mru2,mbdrc,mwdrc,ms2,mt2]
    inds= range(1,7)+[-6,-5]
    mrssm_value_arrays = [lamsd,lamsu,lamtd,lamtu,mud,muu,mbdrc,mwdrc]    
    inds= [4,6]
    mrssm_value_arrays = [lamtu,muu]
    points=[point]
    i=0
    for x in range(len(mrssm_value_arrays)-1):
        for y in range(x+1,len(mrssm_value_arrays)):
            i+=1
            points.extend(scan_2D(point,mrssm_value_arrays[x],mrssm_value_arrays[y],inds[x],inds[y]))
    print i
    sphenodir = "/home/diessner/raid2/SPheno/"
    indir =  "/home/diessner/zihfast/MRSSMmsmtscan/"
    # # indir = sphenodir
    outdir = "/home/diessner/zihfast/MRSSMchfit/"
    working_points = "/home/diessner/research/phd/rsymmetry/MRSSMmsmtworkingpts.txt"
    log =indir+"tachyon_tree_log" 
    npoints= len(points)
    # points = 0 #len(mrssm_scan_array)
    SPheno_scan_seq(sphenodir,SPheno_point, model, indir, outdir, spheno_switches,points,log,SPheno_create_infile_MRSSM_highenergy,working_points,points=npoints)
# par_pool

if __name__ == "__main__":
    # highscale_MRSSM_onepoint()
    # lowscale_MRSSM_Flex()
    highscale_MRSSM()
