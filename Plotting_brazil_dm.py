import numpy as np
import sys
import os.path as osp
import sqlite3
import os.path as osp
import matplotlib as mpl
mpl.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.colors as col
import matplotlib.cm as cm
from scipy.interpolate import griddata
from matplotlib.mlab import griddata as gridd
from matplotlib.backends.backend_pdf import PdfPages
from MRSSMfunctions import BM1, BM2, BM3, BM4 ,parameter
from Init import points
mpl.rcParams.update({'font.size': 10})


def nans(shape, dtype=float):
    a = np.empty(shape, dtype)
    a.fill(np.nan)
    return a

def discrete_cmap(N=8):
    """create a colormap with N (N<15) discrete colors and register it"""
    # define individual colors as hex values
    cpool = ["c","b" ,"y","g","y","c","b"]
    cmap3 = col.ListedColormap(cpool, 'higgsmass')
    cm.register_cmap(cmap=cmap3)

pointdb = "/home/diessner/raid1/pointdbs/bm4_2d_scan.db"
command = "SELECT tanb,lamtd,lamtu,mud,muu,bmu,mq2,ml2,mu2,me2,mbdrc,mwdrc,ms2,\
           masses.mhh2,masses.mw,relic.omega, - relic.loglike \
           FROM points \
           JOIN masses ON points.identifier=masses.identifier \
           JOIN relic ON points.identifier=relic.identifier"

# pp = PdfPages('/home/diessner/research/phd/rsymmetry/BM4_selecteder.pdf')
s = BM4()
indlist = [0,3,4,5,6,7,8,10,12,16,21,22,24]
s = [s[i] for i in indlist]
print [parameter[i] for i in indlist]
bmlist=  [round(float(x),5) for x in s[:5]+map(np.sqrt, s[5:10])+s[10:12]+[np.sqrt(s[12])]],
bmnames= ["BM4"]
# listing = list(points(pointdb, command))
points = [list(x) for x in points(pointdb,command)]
print len(points)
points = [tuple(x[:5]+map(np.sqrt,x[5:10])+x[10:12]+[np.sqrt(x[12])]+x[13:]) for x in points]
points = [list(x) for x in set(points)]
print len(points)
names = ["tanb","lamtd","lamtu","mud","muu", 'bmu','mq2','ml2','md2','me2',"mbdrc","mwdrc","ms2"]
param = [r"$\tan\beta$",r"$\Lambda_d$",r"$\Lambda_u$", r"$\mu_d$ [GeV]",r"$\mu_u$ [GeV]", r"$\sqrt{B_\mu}$ [GeV]",r"$m_{\tilde{q}_L}$ [GeV]",
         r"$m_{\tilde{l}_L}$ [GeV]",r"$m_{\tilde{q}_R}$ [GeV]",r"$m_{\tilde{l}_R}$ [GeV]",r"$M_D^B$ [GeV]",r"$M_D^W$ [GeV]",r"$m_S$ [GeV]"]
limits = [[1,55],[-2,2],[-2,1.1],[100,1600],[100,1500],[0,600],[900,2600],[0,1600],
          [900,2600],[70,260],[5,51],[0,2100],[0,110]]
# ranges  = [[],[float(x)/10. for x in xrange(-20,21,1)],
#            [float(x)/10. for x in xrange(-20,21,1)],
#            [float(x)/10. for x in xrange(-20,21,1)],
#            [float(x)/10. for x in xrange(-20,21,1)], range(100,2100,100),
#            range(100,2100,100),range(50,2100,100),range(50,2100,100),
#            range(100000,4020000,100000),range(100000,4020000,100000),
#            range(100000,4020000,100000),range(100000,4020000,100000)]
wanted = [(2,4),(2,8),(4,8),(6,8),(9,10)]
#wanted = [(0,5)] + [(i,j) for i in (2,3,4,6,7,8,9) for j in (2,3,4,6,7,8,9,10) if j>i]
for bm in [0]:
    stpoint = bmlist[bm]
    stpoint = [round(float(x),5) for x in stpoint]
    print stpoint
    # stpoint = [float(stpoint[i]) for i in indlist]
    w, h = plt.figaspect(1.)
    #fig = plt.Figure(figsize=(w,h))
    for i in range(0,len(names)-1):
        for j in range(i+1,len(names)):
            k,l = indlist[i],indlist[j]
            print i,j
            levels1=[50,100,118,123,127,132,150,200]
            levels2=[80.36,80.38,80.40,80.42,80.44,80.48]
            levels3=[0.05,0.08,0.10,0.13,0.2,0.5,2,10,50,100,1000]
            levels4= [1.5,5,10,50,200]

            # if (i,j) not in [(2,4),(2,6),(4,6)]:
            if (i,j) not in wanted:
            #     print i,j
            #     # print parameter[k],parameter[l]
                continue
            # if i != 3 or j != 5:
            #     continue
            f = plt.figure(figsize=(4,8))
            # f, (ax1, ax2) = plt.subplots(1, 2, sharex='col', sharey='row')
            ax1 = plt.axes([0.2,0.55,0.75,0.43])
            ax2 = plt.axes([0.2,0.05,0.75,0.43])
            # fig = plt.figure(figsize=(1.5,7))
            # ax1 = plt.axes([0.15,0.15,0.22,0.80])
            xar=[]
            yar=[]
            xyar = []
            z1=[]
            z2=[]
            z3=[]
            z4=[]
            start=[]
            m = 1
            for spec in points:
                spec = [round(float(x),5) for x in spec]
                if (stpoint[:i]==spec[:i] and stpoint[i+1:j]==spec[i+1:j] 
                    and stpoint[j+1:]==spec[j+1:len(stpoint)]):
                    xar.append(spec[i])
                    yar.append(spec[j])
                    xyar.append([spec[i],spec[j]])
                    start.append(spec)
                    z1.append(spec[-4])
                    z2.append(spec[-3])
                    z3.append(spec[-2])
                    z4.append(spec[-1])
            print len(z1)
            print np.shape(xyar)
            min3, max3 = min(z3), max(z3)
            min4, max4 = min(z4), max(z4)
            if max3-min3<1:
                levels3 = np.linspace(min3,max3,num=5)
            if max4-min4<2:
                levels4 = np.linspace(min4,max4,num=5)
            extent = limits[i]+limits[j]
            xs, ys = np.mgrid[extent[0]:extent[1]:50j, extent[2]:extent[3]:50j]
            resampled1 = griddata(xyar,z1,(xs,ys),method='cubic')
            resampled2 = griddata(xyar,z2,(xs,ys),method='cubic')
            resampled3 = griddata(xyar,z3,(xs,ys),method='cubic')
            resampled4 = griddata(xyar,z4,(xs,ys),method='cubic')
            start=[list(x) for x in set(tuple(x) for x in start)]
            # np.set_printoptions(threshold=10000)
            # for spec in start:
            #     try:
            #         xind = np.nonzero(xi == spec[i])[0][0]
            #         yind = np.nonzero(yi == spec[j])[0][0]
            #     except IndexError:
            #         continue
            #     else:
            #         zi1[yind][xind]=spec[-2]
            #         zi2[yind][xind]=spec[-1]
            # print zi2
            # ax1.set_xlim(limits[i])
            # ax1.set_ylim(limits[j])
            cpool = ["0.95","0.85","Gold","g","GoldenRod","0.65","0.55"]
            cmap = col.ListedColormap(cpool, 'higgsmass')
            norm = col.BoundaryNorm([50,100,118,124,128,134,150,200], cmap.N)
                
            ax1.set_xlabel(param[i],fontsize='large')
            ax1.set_ylabel(param[j],fontsize='large')
            # ax2.set_xlabel(param[i])#,fontsize='large')
            ax2.set_ylabel(param[j],fontsize='large')
            cs1=ax1.contourf(resampled1.T,levels1,cmap=cmap,norm=norm,extent=extent)
            cs2=ax1.contour(resampled2.T,levels2,colors='r',linestyles='dashed',extent=extent)
            cl2=ax1.clabel(cs2,fmt='%1.2f',use_clabeltext=True,zorder = -1)
            cs3=ax2.contour(resampled3.T,levels3,colors='b',ls='--',extent=extent)
            cl3=ax2.clabel(cs3,fmt='%1.2f',use_clabeltext=True,zorder = -1)
            cs4=ax2.contour(resampled4.T,levels4,colors='r',ls='--',extent=extent)
            cl4=ax2.clabel(cs4,fmt='%1.2f',use_clabeltext=True,zorder = -1)
            cs5=ax2.contourf(resampled3.T,levels1,cmap=cmap,norm=norm,extent=extent)
            
            # cs2=ax1.contour(xi,yi,zi2,levels1,colors='b',linestyles='solid')
            # cl2=ax1.clabel(cs2,fmt='%1.2f',use_clabeltext=True)
            # ax2.plot(stpoint[i],stpoint[j],"*",markersize=20,markerfacecolor='white',zorder=2)
            # if i == 4:
            #     if bm == 0:
            #         ax2.plot(-1.11,stpoint[j],"*",markersize=20,markerfacecolor='black',zorder=2)
            #     elif bm == 1:
            #         ax2.plot(-0.85,stpoint[j],"*",markersize=20,markerfacecolor='black',zorder=2)
            #     elif bm == 2:
            #         ax2.plot(-1.03,stpoint[j],"*",markersize=20,markerfacecolor='black',zorder=2)
                
            # if j == 4:
            #     if bm == 0:
            #         ax2.plot(stpoint[i],-1.11,"*",markersize=20,markerfacecolor='black',zorder=2)
            #     elif bm == 1:
            #         ax2.plot(stpoint[i],-0.85,"*",markersize=20,markerfacecolor='black',zorder=2)
            #     elif bm == 2:
            #         ax2.plot(stpoint[i],-1.03,"*",markersize=20,markerfacecolor='black',zorder=2)
            # fig.colorbar(cs2)
            # plt.yscale('log')
            # plt.legend()
            # pp.savefig()
            # if j ==4:
              #  ax1.plot(stpoint[i],-0.85,"*",markersize=20,markerfacecolor='black')
            # cb1 = mpl.colorbar.ColorbarBase(ax1, cmap=cmap,
            #                            norm=norm,
            #                            orientation='vertical')
            # plt.savefig("/home/diessner/research/phd/rsymmetry/papers/mrssm-higgs-w/img/mhmw_colorbar.pdf")
            plt.savefig("/home/diessner/research/phd/rsymmetry/papers/higgs-in-the-mrssm-with-light-singlet/img/bm4_"+names[i]+"_"+names[j]+".pdf")
            # plt.show()
            # plt.close()
            del f
# pp.close()

