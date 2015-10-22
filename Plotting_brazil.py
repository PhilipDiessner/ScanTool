import numpy as np
import sys
import os.path as osp
import sqlite3
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.colors as col
import matplotlib.cm as cm
from scipy.interpolate import griddata
from matplotlib.mlab import griddata as gridd
from matplotlib.backends.backend_pdf import PdfPages
from MRSSMfunctions import BM1, BM2, BM3, BM4
from Init import points

mpl.rcParams.update({'font.size': 20})


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

pointdb = "/home/diessner/raid1/pointdbs/bm32d2l.db"
command = "SELECT tanb, lamsd,lamtu,lamtd,lamsu,mud,muu,mbdrc,mwdrc,mt2,ms2,mrd2,mru2,mhmw.mw,mhmw.mh1 FROM points JOIN mhmw ON points.identifier=mhmw.identifier"
# command = "SELECT lamsu,muu,mbdrc,ms2, mhh1,zh12*zh12 FROM points JOIN masses ON points.identifier=masses.identifier JOIN hmix on masses.identifier=hmix.identifier"
#pp = PdfPages('/home/diessner/research/phd/rsymmetry/BM2.pdf')
bmlist= BM1, BM2, BM3, BM4,
bmnames= ["BM1","BM2","BM3","BM4"]
indlist = [0,1,4,3,2,5,6,-5,-4,-1,-2,-7,-8]

listing = list(points(pointdb, command)) 

names = ["tanb","lamsd","lamtu","lamtd","lamsu","mud","muu","mbdrc","mwdrc" ,"mt2","ms2","mrd2","mru2"]
param = [r"$\tan\beta$",r"$\lambda_d$",r"$\Lambda_u$",r"$\Lambda_d$",r"$\lambda_u$",
       r"$\mu_d$",r"$\mu_u$",r"$M_D^B$",r"$M_D^W$",r"$m_T^2$",r"$m_S^2$",r"$m_{Rd}^2$",r"$m_{Ru}^2$"]
limits = [(),(-2,2),(-2,2),(-2,2),(-2,2),(0,2000),(0,1500),(0,2100),(0,2100),(0,3000**2),(0,3000**2)
,(0,3000**2),(0,3000**2)]
ranges  = [[],[float(x)/10. for x in xrange(-20,21,1)],
           [float(x)/10. for x in xrange(-20,21,1)],
           [float(x)/10. for x in xrange(-20,21,1)],
           [float(x)/10. for x in xrange(-20,21,1)], range(100,2100,100),
           range(100,2100,100),range(50,2100,100),range(50,2100,100),
           range(100000,4020000,100000),range(100000,4020000,100000),
           range(100000,4020000,100000),range(100000,4020000,100000)]
levels1=[50,100,118,124,128,134,150,200]
levels2=[80.36,80.38,80.40,80.43,80.48]

# indlist = [2,6,21,24]
# names = ["lamsu","muu","mbdrc","ms2"]
# param = [r"$\lambda_u$",r"$\mu_u$",r"$M_D^B$",r"$m_S^2$"]
# ranges = [[float(x)/1000. for x in xrange(-50,51,1)],
#           range(100,2100,50),
#           range(1,61,2),
#           range(0,120,5)]
# # print listing
# listing = [(v,w,x,np.sqrt(y),a,b) for (v,w,x,y,a,b) in listing]
# levels1=range(0,130,10)
# levels2=[x/10. for x in xrange(0,11,1)]
for bm in [2]:
    stpoint = bmlist[bm]()
    stpoint = [float(stpoint[i]) for i in indlist]
    # stpoint[-1]=np.sqrt(stpoint[-1])
    w, h = plt.figaspect(1.)
    #fig = plt.Figure(figsize=(w,h))
    for i in range(0,len(names)-1):
        for j in range(i+1,len(names)):
            if (i,j) not in [(2,4),(2,6),(4,6)]:
            #if (i,j) not in [(1,2),(1,3),(2,4),(2,6),(2,7),(4,5),(4,6),(5,6),(6,8),(7,8)]:
                print i,j
                continue
            # if i != 3 or j != 5:
            #     continue
            fig = plt.figure()
            ax1 = plt.axes([0.17,0.15,0.80,0.80])
            ax2 = plt.axes([0.17,0.15,0.80,0.80])
            # fig = plt.figure(figsize=(1.5,7))
            # ax1 = plt.axes([0.15,0.15,0.22,0.80])
            xar=[]
            yar=[]
            z1=[]
            z2=[]
            start=[]
            for spec in listing:
                spec = [round(float(x),5) for x in spec]
                print spec[:len(stpoint)]
                print stpoint
                if (stpoint[:i]==spec[:i] and stpoint[i+1:j]==spec[i+1:j] 
                    and stpoint[j+1:]==spec[j+1:len(stpoint)]):
                    xar.append(spec[i])
                    yar.append(spec[j])
                    start.append(spec)
                    z1.append(spec[-2])
                    z2.append(spec[-1])
            
            # min1, max1 = min(z1), max(z1)
            # min2, max2 = min(z2), max(z2)
            # if max1-min1<10:
            #     levels1 = np.linspace(min1,max1,num=5)
            # if max1-min1<0.2:
            #     levels2 = np.linspace(min2,max2,num=5)
            xi = np.sort(np.unique(np.array(xar)))
            yi = np.sort(np.unique(np.array(yar)))
            print xi
            print yi
            xgrid,ygrid= np.meshgrid(xi,yi)
            zi1=nans((len(yi),len(xi)))
            zi2=nans((len(yi),len(xi)))
            start=[list(x) for x in set(tuple(x) for x in start)]
            # np.set_printoptions(threshold=10000)
            for spec in start:
                try:
                #print xi, spec[i]
                    xind = np.nonzero(xi == spec[i])[0][0]
                    yind = np.nonzero(yi == spec[j])[0][0]
                except IndexError:
                    continue
                else:
                    zi1[yind][xind]=spec[-2]
                    zi2[yind][xind]=spec[-1]
            # print zi2
            # ax1.set_xlim(limits[i])
            # ax1.set_ylim(limits[j])
            print zi2
            print zi1
            ax1.set_xlabel(param[i],fontsize='large')
            ax1.set_ylabel(param[j],fontsize='large')
            cs1=ax1.contour(xi,yi,zi1,levels2,colors='r',linestyles='dashed')
            cl1=ax1.clabel(cs1,fmt='%1.2f',use_clabeltext=True)
            # cs2=ax1.contour(xi,yi,zi2,levels2,colors='g',linestyles='-.', zorder=0)
            # cl2=ax1.clabel(cs2,fmt='%1.2f',use_clabeltext=True,zorder = 0)
            # cs2=ax1.contour(xi,yi,zi2,levels1,colors='b',linestyles='solid')
            # cl2=ax1.clabel(cs2,fmt='%1.2f',use_clabeltext=True)
            cpool = ["0.95","0.85","Gold","g","GoldenRod","0.65","0.55"]
            cmap = col.ListedColormap(cpool, 'higgsmass')
            norm = col.BoundaryNorm([50,100,118,124,128,134,150,200], cmap.N)
            # cs3=ax1.contourf(xi,yi,zi2,levels2, zorder=-1)
            cs2=ax1.contourf(xi,yi,zi2,levels1,cmap=cmap,norm=norm)
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
            # plt.savefig("/home/diessner/research/phd/rsymmetry/lightsinglet/"+bmnames[bm]+"_mh1zh12_"+names[i]+"_"+names[j]+".pdf")
            plt.savefig("/home/diessner/Documents/talks/SUSY2015/"+bmnames[bm]+"_mhmw_"+names[i]+"_"+names[j]+".pdf")
            plt.show()
            # plt.close()
#pp.close()

