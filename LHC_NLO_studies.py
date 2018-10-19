import os.path as osp
import subprocess as spr
import os
from math import log10, floor
from sqlite3 import OperationalError
import string
from collections import defaultdict
import cPickle as pickle
import xml.etree.ElementTree as et
import cProfile
import numpy as np

from Init import points, make_db,register_points
from Run import runwrapper, partial_runwrapper, touch#, replace_line_in_file
from lhc_nlo_cards import *
from HEPpaths import MGpath
from SLHA_extract_values import get_sq_gl_masses,SLHA
from matplotlib import gridspec
try:
    import numpy as np
    import matplotlib as mpl
    import matplotlib.pyplot as plt
    from scipy.interpolate import griddata
    from matplotlib.mlab import griddata as gridd
    params = {
        #'text.usetex' : True,
    'font.size' : 11,
    #'font.family' : 'lmodern',
    #'text.latex.unicode': True,
    'xtick.labelsize':9,
    'ytick.labelsize':9}

    plt.rcParams.update(params) 
except ImportError:
    import math as np
def round_to_1(x):
    return round(x, -int(floor(log10(abs(x)))))

def make_arrs(xy,z,extent,inter=70j,interpol='linear'):
    xs, ys = np.mgrid[extent[0]:extent[1]:inter, extent[2]:extent[3]:inter]
    resampled = griddata( xy,z, (xs, ys),method=interpol )
    return resampled.T

def mso_calc(mglu,mpo):
    return np.sqrt(mpo*mpo+4*mglu*mglu)

def do_MG_scan(scans,process,lo=True,mu=None,pdfset=None):
    """ scans - iterable of tuples
    process - string of processname
    lo - lo or nlo
    """
    processdir = osp.join(MGpath,process)
    paramcardpath = osp.join(processdir,"Cards/param_card.dat")
    runcardpath = osp.join(processdir,"Cards/run_card.dat")
    optionpath = osp.join(processdir,"launch.txt")
    executable = ["./bin/aMCatNLO", "launch.txt"] 
    
    if lo:
        if not pdfset:
            pdf = 25000
        else:
            pdf = pdfset
        order = "LO" 
        prec = 0.001
    else:
        if not pdfset:
            pdf = 25100
        else:
            pdf = pdfset
        order = "NLO"
        prec = 0.003
    if mu:
        renorm="True"
    else:
        renorm="False"
        mu=[500]
    for i, scan in enumerate(scans):
        print process, order
        print scan,mu[i],pdf
        if len(scan)==4:
            with open(paramcardpath, 'w') as f:
                f.write(paramcard_mrssm_wrapper(scan))
        elif len(scan)==3: # stop left and right different
            with open(paramcardpath, 'w') as f:
                f.write(paramcard_MSSM(scan))
        else:
            print "wrong number of parameters passed"
            return False
        with open(runcardpath, 'w') as f:
            if len(scans)==len(mu):
                f.write(runcard([i,pdf,prec,renorm,mu[i]]))
            elif len(mu)==1:
                f.write(runcard([i,pdf,prec,renorm,mu[0]]))                
            else: 
                print 'wrong len of mu'
                return False
        with open(optionpath, 'w') as f:
            f.write(optioncard(order))
        out = runwrapper(executable, processdir)
        with open('/theoc/theoc-fs01/data/diessner/logging_mg.log','a') as f:
            f.write(out)
        

param_dict = {"#run_name":"run",
              "mass#1000001":"mdl","mass#2000001":"mdr",
              "mass#1000002":"mul","mass#2000002":"mur",
              "mass#1000003":"msl","mass#2000003":"msr",
              "mass#1000004":"mcl","mass#2000004":"mcr",
              "mass#1000005":"mbl","mass#2000005":"mbr",
              "mass#1000006":"mtl","mass#2000006":"mtr",
              "mass#1000021":"mgl","mass#3000021":"mso",
              "mass#3000022":"mpo", "cross(pb)":"xsect"}

writeparam = ["run","xsect","mdl","mdr","mul","mur","msl","msr",
              "mcl","mcr","mbl","mbr","mtl","mtr","mgl","mso","mpo"]
paramtypes = ["text"]+ ["real"]*(len(writeparam)-1)

def readout_summary(infile,dbname,table):
    with open(infile, 'r') as f:
        lines = f.readlines()
    params = [param_dict.get(x, None) for x in lines[0].split()]
    notneeded = [i for i, j in enumerate(params) if j == None]
    params=[i for i in params if i != None]
    sortind = []
    for val in writeparam:
        try:
            sortind.append(params.index(val))
        except ValueError:
            print "I hope this is the MSSM as param "+ val+" not found"
            pass
    towrite=[]
    for i,line in enumerate(lines[1:]):
        line=line.split()
        line = [j for i, j in enumerate(line) if i not in notneeded] 
            
        newline = [line[x] for x in sortind]
        newline[1:] = [float(x) for x in newline[1:]]
        long_enough= len(writeparam)-len(newline)
        newline = newline + [-1]*long_enough # add octet masses if missing for mssm
        towrite.append([i+1]+newline)
    try:
        make_db(dbname,zip(writeparam,paramtypes),table,towrite)
    except OperationalError:
        register_points(dbname,table,towrite)

def plot(dbdir):
    db1 = osp.join(dbdir,"sulsur_mssm_0.001_fixedmur")
    db2 = osp.join(dbdir,"sulsur_mrssm_0.001_fixedmur")
    command ='SELECT mgl, xsect FROM NLO where mul=500'
    nlopoints = [list(x) for x in points(db1,command)]
    command ='SELECT mgl, xsect FROM LO where mul=500'
    lopoints = [list(x) for x in points(db1,command)]
    command ='SELECT mgl, xsect FROM NLO where mul=500 and mpo=3000 order by mgl asc'
    nlopoints1 = [list(x) for x in points(db2,command)]
    command ='SELECT mgl, xsect FROM LO where mul=500 and mpo=3000 order by mgl asc'
    lopoints1 = [list(x) for x in points(db2,command)]
    command ='SELECT mgl, xsect FROM NLO where mul=500 and mpo=10000 order by mgl asc'
    nlopoints2 = [list(x) for x in points(db2,command)]
    command ='SELECT mgl, xsect FROM LO where mul=500 and mpo=10000 order by mgl asc'
    lopoints2 = [list(x) for x in points(db2,command)]
    command ='SELECT mgl, xsect FROM NLO where mul=500 and mpo=30000 order by mgl asc'
    nlopoints3 = [list(x) for x in points(db2,command)]
    command ='SELECT mgl, xsect FROM LO where mul=500 and mpo=30000 order by mgl asc'
    lopoints3 = [list(x) for x in points(db2,command)]
    # point3 = points(db3,command)[0]
    # print sorted(point2)
    print nlopoints2
    # plotpoints1 = np.transpose(sorted(point2))
    # plotpoints2 = np.transpose(sorted(points2))
    x = []
    k = []
    for lo in lopoints:
        for nlo in nlopoints:
            if lo[0]==nlo[0]:
                x.append(lo[0])
                k.append(nlo[1]/lo[1])
                break
    x1 = []
    k1 = []
    for lo in lopoints1:
        for nlo in nlopoints1:
            if lo[0]==nlo[0]:
                x1.append(lo[0])
                k1.append(nlo[1]/lo[1])
                print nlo
                break
    x2 = []
    k2 = []
    for lo in lopoints2:
        for nlo in nlopoints2:
            if lo[0]==nlo[0]:
                x2.append(lo[0])
                k2.append(nlo[1]/lo[1])
                break
    x3 = []
    k3 = []
    for lo in lopoints3:
        for nlo in nlopoints3:
            if lo[0]==nlo[0]:
                x3.append(lo[0])
                k3.append(nlo[1]/lo[1])
                print nlo
                break
    #a=[]
    #for i in range(len(x)):
    #    a.append(k[i]-k1[i])
    # f=plt.Figure(figsize=(5.95/2,5.95/1.618))
    # f.set_tight_layout(True)
    f,(ax) = plt.subplots(figsize=(8.3/3.,9/1.618), ncols=1)
    f.set_tight_layout(True)
    #plt.plot(plotpoints1[0],plotpoints1[1],color='b',linestyle='-',label="varying CP-even mass only")
    #plt.plot(plotpoints3[0],plotpoints3[1],color='r',linestyle='--',label="cp-odd octet not zero mom subtraction")    
    #plt.plot(0.9,point3[1],marker='o',label=r'as before for $m_o=0$')
    ax.plot(x,k,color='b',ls='--',lw=3,label=r'MSSM')    
    ax.plot(x1,k1,color='r',ls='-',lw=3,label=r'MRSSM, $m_O=3$ TeV')
    ax.plot(x2,k2,color='g',ls='-.',lw=3,label=r'MRSSM, $m_O=10$ TeV')
    ax.plot(x3,k3,color='m',ls=':',lw=3,label=r'MRSSM, $m_O=30$ TeV')
    #plt.plot(0.9,point2[1],marker='*',label=r'as before for $m_o=0$')
    ax.set_xlim([1000,4800])
    xticks = ax.xaxis.get_major_ticks()
    for tick in xticks[::2]:
        tick.label1.set_visible(False)
    ax.legend(loc='best',prop={'size':10})
    # plt.xscale('log')
    ax.set_xlabel(r'$m_{\tilde{g}}$ [GeV]')
    ax.set_ylabel(r'K')
    ax.set_title(r'$pp\to \tilde u_L \tilde u_R$, $m_{\tilde q}=500$ GeV')
    #f.subplots_adjust(hspace=0.3)
    f.savefig("/home/diessner/research/rsymmetry/SQCD/ulur_mglu_K_msq=500_final.pdf")
    plt.show()

def muplot():
    from muarray import muscan,muscan2
    x,lo,nlo=zip(*muscan)
    lo = [a*1000. for a in lo] 
    nlo = [a*1000. for a in nlo]
    k = [nlo[i]/lov for i, lov in enumerate(lo)]
    
    f = plt.figure(figsize=(8/2,8/1.618)) 

    gs = gridspec.GridSpec(2, 1, height_ratios=[3, 1]) 
    ax1 = plt.subplot(gs[0])
    ax2 = plt.subplot(gs[1])
    #f,(ax1,ax2) = plt.subplots(2,figsize=(8/2,8/1.618),sharex=True)
    ax1.plot(x,lo,color='b',ls='--',lw=3,label=r'LO')   
    ax1.plot(x,nlo,color='g',ls='-',lw=3,label=r'NLO')
    ax2.plot(x,k,color='b',ls='-',lw=3)
    # plt.xscale('log')
    ax1.legend(loc='best',prop={'size':12})
    #plt.xscale('log')
    ax1.set_xlabel(r'$\mu_R=\mu_F$ [GeV]')
    ax1.set_ylabel(r'$\sigma$ [fb]' )
    ax2.set_ylabel(r'$K$' )
    ax1.set_title(r'$pp\to \tilde u_L \tilde u_R$, $m_{\tilde q}=1500$ GeV, $m_{\tilde g}=2000$ GeV')

    plt.tight_layout()
    f.savefig("/home/diessner/research/rsymmetry/SQCD/ulur_mu.pdf")
    plt.show()

def octetplot():
    db ="/afs/desy.de/user/d/diessner/theorie/pointdbs/sulsur_mrssm_final"
    locommand = "SELECT mpo, xsect FROM LO where mul=1500 and mgl=2000 order by mpo"
    nlocommand = "SELECT mpo, xsect FROM NLO where mul=1500 and mgl=2000 order by mpo"
    lopoints = [list(i) for i in points(db,locommand)]
    nlopoints = [list(i) for i in points(db,nlocommand)]
    x1 = []
    k1 = []
    for point in nlopoints:
        for lopoint in lopoints:
            if point[0]==lopoint[0]:
                x1.append(point[0])
                print point,lopoint
                k1.append(point[1]/lopoints[3][1])
    db = "/afs/desy.de/user/d/diessner/theorie/pointdbs/sulsulc_mrssm_final"
    locommand = "SELECT mpo, xsect FROM LO where mul=1500 and mgl=2000 order by mpo"
    nlocommand = "SELECT mpo, xsect FROM NLO where mul=1500 and mgl=2000 order by mpo"
    lopoints = [list(i) for i in points(db,locommand)]
    nlopoints = [list(i) for i in points(db,nlocommand)]
    x2=[]
    k2=[]
    for point in nlopoints:
        for lopoint in lopoints:
            if point[0]==lopoint[0]:
                x2.append(point[0])
                print point,lopoint
                k2.append(point[1]/lopoints[2][1])
    #k2=[4.842e-04/lopoints[0][1]]+k2
    #x2=[1000]+x2
    print k1,k2
    #f,(ax1) = plt.subplots(figsize=(8/1.618,8/2))
    f,(ax1) = plt.subplots(figsize=(8.3/3.,9/1.618), ncols=1)
    f.set_tight_layout(True)
    ax1.plot(x1,k1,color='b',ls='--',lw=3,label=r'$\tilde{u}_L\tilde{u}_R$')   
    ax1.plot(x2,k2,color='g',ls='-',lw=3,label=r'$\tilde{u}_L\tilde{u}_L^\dagger$')
    # plt.xscale('log')
    ax1.legend(loc='best',prop={'size':10})
    plt.xscale('log')
    ax1.set_xlabel(r'$m_O$ [GeV]')
    #ax1.set_ylabel(r'$\sigma$ [fb]' )
    ax1.set_ylabel(r'K' )
    ax1.set_xlim([1000,500000])
    #f.subplots_adjust(left=0.2)
    ax1.set_title(r'$m_{\tilde q}=1500$ GeV, $m_{\tilde g}=2000$ GeV',loc='right')
    f.savefig("/home/diessner/research/rsymmetry/SQCD/octetmass_dep_final.pdf")
    plt.show()

def plotpoints(db,db2=None):
    extent=[250,4000,1000,5000]
    locommand = "SELECT mul, mgl, xsect FROM LO where  mpo=3000"
    nlocommand= "SELECT mul, mgl, xsect FROM NLO where mpo=3000"
    mssmlocommand = "SELECT mul, mgl, xsect FROM LO where mpo=-1"
    mssmnlocommand= "SELECT mul, mgl, xsect FROM NLO where mpo=-1"
    command="select mpo, xsect from NLO where mul=1000 and mgl=1500"
    lopoints = [list(x) for x in points(db,locommand)]
    nlopoints = [list(x) for x in points(db,nlocommand)]
    if db2:
        lopoints2 = [list(x) for x in points(db2,mssmlocommand)]
        nlopoints2 = [list(x) for x in points(db2,mssmnlocommand)]
        print points
    xy, z, start = [], [], []
    lopoints=[[250,1000,0.9225658]]+ lopoints # sulsur3TeV
    scatter=False
    if scatter:
        xy = [x[:2] for x in lopoints]
    #z = [np.log10(x[2]) for x in lopoints]
    else:
        for point in nlopoints:
            for lopoint in lopoints:
                if point[:2]==lopoint[:2]:
                    if db2:
                        for point2 in nlopoints2:
                            if point[:2]==point2[:2]:
                                for lopoint2 in lopoints2:
                                    if point[:2]==lopoint2[:2]:
                                        xy.append(point[:2])
                                        z.append(lopoint2[2]*point[2]/point2[2]/lopoint[2])
                                        print lopoint[2], lopoint2[2]
                                        break
                    else:
                        xy.append(point[:2])
                        z.append(point[2]/lopoint[2])
                        print point[:2],point[2]/lopoint[2]
                        break
    print xy,z
    return [xy,z,extent]

def plotting(xy,zi,extent):
    #f=plt.figure(figsize=(2,2))
    # f.set_size_inches(2.07,3,forward=True)    
    #plt.scatter([x[0] for x in xy],[x[1] for x in xy])
    f,(ax1) = plt.subplots(figsize=(8/1.618,8/2))
    f.set_tight_layout(True)
    #ax1.scatter([x[0] for x in xy],[x[1] for x in xy])
    cs=ax1.contour(make_arrs(xy,zi,extent,inter=20j),extent=extent,cmap='winter',linewidths=2)
    ax1.clabel(cs,fmt='%1.2f',use_clabeltext=True)
    #plt.yscale('log')
    ax1.set_xlabel(r'$m_{\tilde{q}}$ [GeV]')
    ax1.set_ylabel(r'$m_{\tilde{g}}$ [GeV]')
    ax1.set_title(r'$K$(MRSSM)/K(MSSM), $pp\rightarrow \tilde{u}_L \tilde{u}_R$, $m_O=3$ TeV')
    f.savefig("/home/diessner/research/rsymmetry/SQCD/sulsur_final.pdf")
    plt.show()

def mssmscan():
    massesscanmssm = []
    msqscan = "scan1:range(3000,5000,500)"
    mglscan = "scan2:[200,300,400,500,750]"
    mtrscan = "scan1:[x+1 for x in range(3000,5000,500)]"
    massesscanmssm = massesscanmssm + [[msqscan, mglscan, mtrscan]]
    massesscanmssm = []
    #for msq in [300,400,500,750]+range(1000,4501,500):
   # msq=1500
    mus=[]
    for msq in range(250,4001,250):
        for mgl in range(1000,5001,250):
            msqscan =  "scan1:["+str(msq)+"]" 
            mtrscan = "scan1:["+str(msq*1.001)+"]" 
            # for mgl in range(1000,5001,200):
            mglscan =  "scan1:["+str(mgl)+"]"
            massesscanmssm += [[msqscan, mglscan, mtrscan]]
            mus.append(msq)
    process = "pp_susu_mssm" 
    # process = "ulbar_mssm"   

    do_MG_scan(massesscanmssm,process,lo=True,mu=mus)
    do_MG_scan(massesscanmssm,process,lo=False,mu=mus)
   
def mrssmscan():
    massesscan = []
    msqscan = "scan:[1500]"
    mglscan = "scan:[2000]"
    mposcan = "5000"
    msoscan = "5385"
    process = "pp_qlqr" #"pp_ululbar"
    mus=[]
    # massesscan = [[msqscan, mglscan, msoscan, mposcan]]
    # massesscan = [["1500", "1000", str(np.sqrt(5000**2+4*1000**2)), "5000"],
    #               ["1500", "2000", str(np.sqrt(5000**2+4*2000**2)), "5000"],
    #               ["500", "2000", str(np.sqrt(5000**2+4*2000**2)), "5000"]]
    #pdfs = [25100,25200,13100,260000]
    #mgl=2000 # *1000
    #msq=1500
    # for mo in 1,2,4,8,16,31,63,125,250,500,1000:
    #     msqscan = "scan1:["+str(msq)+"]"
    #     mglscan = "scan1:["+str(mgl)+"]"
    #     mposcan = "scan1:["+str(mo*1000)+"]"
    #     msoscan = "scan1:["+str(np.sqrt(mo**2+4*(mgl/1000.)**2)*1000)+"]"
    #     mus.append(msq)
    #     massesscan +=[[msqscan, mglscan, msoscan, mposcan]]
    mo=5
    mgl=2000
    for msq in range(500,2001,50):
        msqscan = "scan1:["+str(msq)+"]"
        mglscan = "scan1:["+str(mgl)+"]"
        mposcan = "scan1:["+str(mo*1000)+"]"
        msoscan = "scan1:["+str(np.sqrt(mo**2+4*(mgl/1000.)**2)*1000)+"]"
        mus.append(msq)
        massesscan +=[[msqscan, mglscan, msoscan, mposcan]]
    # msq=1500
    # for mgl in range(500,3001,50):
    #     msqscan = "scan1:["+str(msq)+"]"
    #     mglscan = "scan1:["+str(mgl)+"]"
    #     mposcan = "scan1:["+str(mo*1000)+"]"
    #     msoscan = "scan1:["+str(np.sqrt(mo**2+4*(mgl/1000.)**2)*1000)+"]"
    #     mus.append(msq)
    #     massesscan +=[[msqscan, mglscan, msoscan, mposcan]]
    # for msq in range(500,4001,250):
    #     for mgl in range(1000,5001,250):
    #         for mo in 300,:
    #             mo=mo*1000
    #             msqscan = "scan1:["+str(msq)+"]"
    #             mglscan = "scan1:["+str(mgl)+"]"
    #             mposcan = "scan1:["+str(mo)+"]"
    #             msoscan = "scan1:["+str(np.sqrt(mo**2+4*mgl**2))+"]"
    #             mus.append(msq)
    #             massesscan +=[[msqscan, mglscan, msoscan, mposcan]]
    #massesscan = [["1500", "2000", str(np.sqrt(5000**2+4*2000**2)), "5000"]]
    #mus = [1500,1500,500]
    #for i,point in enumerate(massesscan):
    #    for pdf in pdfs:
    #        do_MG_scan([point],process,lo=False,mu=mus[i],pdfset=pdf)
        
    # for muin in range(300,3000,75)+range(3000,6001,200):
    #     do_MG_scan(massesscan,process,lo=False,mu=muin)
    #     do_MG_scan(massesscan,process,lo=True,mu=muin)
    # for mun in range(300,750,75)+range(3000,6001,200):
    print len(massesscan),len(mus)
    do_MG_scan(massesscan,process,lo=True,mu=mus,pdfset=25000)
    #do_MG_scan(massesscan,process,lo=False,mu=mus,pdfset=25100)
    # print paramcard_mrssm_wrapper(massesscan[0])

def readout():
    nlofiles=[]
    lofiles=[]
    #for i in range(1975,2519):
    #    lofiles.append("scan_run_"+str(i)+"_LO[-]run_"+str(i)+"_LO.txt")
    for i in range(401,656):
        nlofiles.append("scan_run_"+str(i)+"[-]run_"+str(i)+".txt")
    #nw="3[68-82]","3[83-97]","[398-412]","4[13-27]","4[28-42]","4[43-57]","4[58-72]","4[73-80]",\
    #    "48[1-9]","[490-504]","5[05-19]","5[20-34]","5[35-49]","5[50-64]","5[65-79]","5[80-94]",\
    #    "[595-609]","6[10-24]","6[25-39]","6[40-54]","6[55-69]","6[70-84]","6[85-99]","7[00-14]"
    #for i in nw:
    #    nlofiles.append("scan_run_"+i+".txt")
    dbdir= "/afs/desy.de/user/d/diessner/theorie/pointdbs/"
    db = osp.join(dbdir,"sulsulc_mrssm_final")
    process = "pp_ululc_second"
    processdir = osp.join(MGpath,process)
    for fil in nlofiles:
        infile = osp.join(processdir,"Events",fil)
     #   print infile
        try:
            readout_summary(infile,db,"NLO")
        except IOError:
            pass
    for fil in lofiles:
        infile = osp.join(processdir,"Events",fil)
        try:
            pass
            readout_summary(infile,db,"LO")
        except IOError:
            pass

#def runcard_parser(filename):
    
def summary_parser(filename,withuncert=False):
    if withuncert:
        with open(filename) as f:
            for i,line in enumerate(f):
                if i==9:
                    scale=line
                if i==12:
                    pdf=line
        scale= scale.split()
        pdf= pdf.split()
        result=(float(scale[0])+float(pdf[0]))/2.
        up= np.sqrt(float(scale[2][:-1])**2+float(pdf[2][:-1])**2)
        down= np.sqrt(float(scale[3][:-1])**2+float(pdf[3][:-1])**2)
        return result, result*(100+up)/100.,result*(100-down)/100.
    else:
        with open(filename) as f:
            for i,line in enumerate(f):
                if i==5:
                    result = float(line.split()[3])
                    numunc = float(line.split()[5])
        return result, result+numunc,result-numunc


def get_summary(lo_range,nlo_range,mass_range,process):
    xy=[]
    for i,res in enumerate(lo_range):
        templo= str(res) if res>9  else  "0"+str(res)
        tempnlo= str(nlo_range[i]) if nlo_range[i]>9 else "0"+str(nlo_range[i])
        try:
            out=summary_parser(
                osp.expanduser("~/data/madgraph/"+process+"/Events/run_"+templo+"_LO/summary.txt"))
            nloout=summary_parser(
                osp.expanduser("~/data/madgraph/"+process+"/Events/run_"+tempnlo+"_LO/summary.txt"))
        except:
            continue
        xy.append([mass_range[i],out,nloout])
    return xy

def header_parser(ffile):
    with open(ffile, 'r') as f:
        text=f.readlines()
    text = filter(lambda x: x[0]!="#",text)
    root = et.fromstringlist(text)
    return SLHA(slhastr=root[0][2].text)

def get_msq_mgl_mo_header(ffile):
    slha = header_parser(ffile)
    variables = [
        ['mq','MASS',['1000001']],
        ['mg','MASS',['1000021']],
        ['mo','MASS',['3000022']]]
    res = map(slha.getvalue,variables)
    res[-1]=round_to_1(res[-1])
    return res


def loop_header():
    maindir = "/afs/desy.de/user/d/diessner/data/madgraph/pp_qlql_all/Events/"
    db = "/afs/desy.de/user/d/diessner/theorie/pointdbs/NLO_xsec_qlql.db"
    runrange= xrange(17,1297)
    lorange = xrange(1537,1793)
    result=[]
    parameters = zip(["msq","mglu","mo","xsec","xsecup","xsecdown"],['real']*6)
    # for x in runrange:
    #     if x <10:
    #         ffile = maindir+"run_0{0}/run_0{0}_grid_banner.txt".format(x)
    #         sfile = maindir+"run_0{0}/summary.txt".format(x)
    #     else:
    #         ffile = maindir+"run_{0}/run_{0}_grid_banner.txt".format(x)
    #         sfile = maindir+"run_{0}/summary.txt".format(x)
    #     result.append(get_msq_mgl_mo_header(ffile)+list(summary_parser(sfile,withuncert=False)))
    # #print np.asarray(result)[:,1].sum(),np.asarray(result)[:,0].sum()
    # for mo in 1000,3000,10000,30000,100000:
    #     res=filter(lambda z: z[2]==mo,result)
    #     res = [[i]+z for i,z in enumerate(res)]
    #     make_db(db,parameters,"t"+str(mo),res)
    # result=[]
    for x in lorange:
        if x <10:
            ffile = maindir+"run_0{0}_LO/run_0{0}_LO_grid_banner.txt".format(x)
            sfile = maindir+"run_0{0}_LO/summary.txt".format(x)
        else:
            ffile = maindir+"run_{0}_LO/run_{0}_LO_grid_banner.txt".format(x)
            sfile = maindir+"run_{0}_LO/summary.txt".format(x)
        result.append(get_msq_mgl_mo_header(ffile)+list(summary_parser(sfile,withuncert=False)))
    res = [[i]+z for i,z in enumerate(result)]
    make_db(db,parameters,"lo",res)

def result_data():
    # data
    lo_mglscan=range(1,32)
    nlo_mglscan=range(32,63)
    lo_msqscan=range(63,94)
    nlo_msqscan=range(1,32)
    mglu=range(500,3001,50)
    msq=range(500,2001,50)
    p1="pp_qlql_all"
    ulul=get_summary(lo_msqscan,nlo_msqscan,msq,p1)
    lo_mglscan=range(170,221)
    nlo_mglscan=range(221,272)
    lo_msqscan=range(66,97)
    nlo_msqscan=range(4,35)
    p2="pp_qlqr"
    ulur=get_summary(lo_msqscan,nlo_msqscan,msq,p2)
    pickle.dump(ulur, open( "ulur_tree.p", "wb" ) )
    pickle.dump(ulul, open( "ulul_tree.p", "wb" ) )

def result_plot():
    ulur = pickle.load( open( osp.expanduser("~/afs/ulur_tree.p"), "rb" ) )
    ulul = pickle.load( open( osp.expanduser("~/afs/ulul_tree.p"), "rb" ) )
    print ulul#,ulur

    f = plt.figure(figsize=(8/2,10/1.618)) 
    gs = gridspec.GridSpec(3, 1, height_ratios=[3, 1, 1]) 
    ax1 = plt.subplot(gs[0])
    ax2 = plt.subplot(gs[1], sharex=ax1)
    ax3 = plt.subplot(gs[2])
    ax1.set_yscale("log")
    ax1.set_xlim([500,2000])
    ax2.set_xlim([500,2000])
    ax3.set_xlim([500,2000])
    mass1=[x[0] for x in ulul]
    mass2=[x[0] for x in ulul]
    ax1.plot(mass1,[x[2][0]*1000 for x in ulur],'r',lw=2,ls="-",label=r"$\tilde{q} \tilde{q}$ NLO")
    ax1.plot(mass1,[x[1][0]*1000 for x in ulur],'g',lw=2,ls="--",label=r"$\tilde{q} \tilde{q}$ LO")
    ax1.plot(mass2,[x[2][0]*1000 for x in ulul],"b",lw=2,ls="-.",label=r"$\tilde{q} \tilde{q}^\dagger$ NLO")
    ax1.plot(mass2,[x[1][0]*1000 for x in ulul],"k",lw=2,ls=":",label=r"$\tilde{q} \tilde{q}^\dagger$ LO")
    ax1.set_title(r"$m_{\tilde{g}}=2000$ GeV, $m_{O}=5000$ GeV")
    ax1.legend(loc='best',prop={'size':11})
    ax2.plot(mass1,[x[2][0]/x[1][0] for x in ulur],'r',lw=2,ls="-")
    #ax2.plot(mass1,[x[2][1]/x[1][0] for x in ulur])
    #ax2.plot(mass1,[x[2][2]/x[1][0] for x in ulur])
    #ax2.plot(mass1,[x[1][1]/x[1][0] for x in ulur])
    #ax2.plot(mass1,[x[1][2]/x[1][0] for x in ulur])
    #ax2.plot(mass1,[1 for x in ulur],lw=2,ls="--")
    ax3.plot(mass2,[x[2][0]/x[1][0] for x in ulul],"b",lw=2,ls="-.")
    # ax3.plot(mass2,[x[2][1]/x[1][0] for x in ulul],"b",lw=1,ls="-.",alpha=0.5)
    # ax3.plot(mass2,[x[2][2]/x[1][0] for x in ulul],"b",lw=1,ls="-.",alpha=0.5)
    # ax3.plot(mass2,[x[1][1]/x[1][0] for x in ulul],"k",lw=1,ls=":",alpha=0.5)
    # ax3.plot(mass2,[x[1][2]/x[1][0] for x in ulul],"k",lw=1,ls=":",alpha=0.5)
    #ax2.plot(mass2,[1 for x in ulur],'g',lw=2,ls="--")
    #ax3.plot(mass2,[1 for x in ulur],'k',lw=2,ls=":")
    ax2.fill_between(mass1,[x[2][1]/x[1][0] for x in ulur],[x[2][2]/x[1][0] for x in ulur]
                     , facecolor='red', interpolate=True, alpha=0.3)
    # ax2.fill_between(mass1,[x[1][1]/x[1][0] for x in ulur],[x[1][2]/x[1][0] for x in ulur]
    #                  , facecolor='green', interpolate=True, alpha=0.3)
    ax1.fill_between(mass1,[x[2][1]*1000 for x in ulur],[x[2][2]*1000 for x in ulur]
                     , facecolor='red', interpolate=True, alpha=0.3)
    ax1.fill_between(mass1,[x[1][1]*1000 for x in ulur],[x[1][2]*1000 for x in ulur]
                     , facecolor='green', interpolate=True, alpha=0.3)    
    ax1.fill_between(mass2,[x[2][1]*1000 for x in ulul],[x[2][2]*1000 for x in ulul]
                      , facecolor='b', interpolate=True, alpha=0.3)
    ax1.fill_between(mass2,[x[1][1]*1000 for x in ulul],[x[1][2]*1000 for x in ulul]
                      , facecolor='k', interpolate=True, alpha=0.3)
    ax3.fill_between(mass2,[x[2][1]/x[1][0] for x in ulul],[x[2][2]/x[1][0] for x in ulul]
                     , facecolor='blue', interpolate=True, alpha=0.3)
    # ax3.fill_between(mass2,[x[1][1]/x[1][0] for x in ulul],[x[1][2]/x[1][0] for x in ulul]
    #                  , facecolor='black', interpolate=True, alpha=0.3)
    
    f.set_tight_layout(True)
    ax1.set_ylabel(r'$\sigma$ [fb]')
    ax2.set_ylabel(r'$K(pp\rightarrow \tilde{q} \tilde{q})$')
    ax3.set_ylabel(r'$K(pp\rightarrow \tilde{q} \tilde{q}^\dagger)$')
    ax3.set_xlabel(r'$m_{\tilde{q}}$ [GeV]')
    plt.setp(ax1.get_xticklabels(), visible=False)
    plt.setp(ax2.get_xticklabels(), visible=False)
    #plt.savefig("test.pdf")
    plt.savefig("/home/diessner/research/rsymmetry/SQCD/alternative_tree_msq.pdf")
    plt.show()

if __name__ == "__main__":
    #mssmscan()
    #mrssmscan()
    # readout()
    dbdir= "/afs/desy.de/user/d/diessner/theorie/pointdbs/"
    db = osp.join(dbdir,"sulsur_mrssm_final")
    db2 = osp.join(dbdir,"sulsur_mssm_final")
    #db = osp.join(dbdir,"ululbar_mrssm_0.001")
    #plotting(*plotpoints(db,db2))
    #plot(dbdir)
    #octetplot()
    #muplot()
    #result_data()
    #result_plot()
    loop_header()
# "pp_ulur_mssm" "pp_susu_mssm" "ulbar_mssm" done;
