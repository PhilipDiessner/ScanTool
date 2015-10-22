import os.path as osp
import sqlite3
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.colors as col
import matplotlib.cm as cm
from matplotlib.contour import ContourSet
from scipy.interpolate import griddata
# from matplotlib.mlab import griddata
from matplotlib.mlab import griddata as gridd
from matplotlib.backends.backend_pdf import PdfPages
from Init import points
# from MRSSMplotting import nans
# params = {'text.usetex' : True,
#           'font.size' : 11,
#           'font.family' : 'lmodern',
#           'text.latex.unicode': True,
#           }
# plt.rcParams.update(params) 

plt.rcParams.update({'font.size': 24})

def make_omega_plot(omega_points):
    N = 15j
    extent = (5,55,50,500)
    # extent = (200,1200,1000,3100)

    xs, ys = np.mgrid[extent[0]:extent[1]:50j, extent[2]:extent[3]:50j]
    x0 = [x[0] for x in omega_points]
    y0 = [x[1] for x in omega_points]
    print min(x0), max(x0)
    xy = [[x[0], x[1]] for x in omega_points ]
    z0 = [x[2] for x in omega_points
               ]
    resampled0 = griddata( xy,z0, (xs, ys),method='linear' )
    # resampled1 = griddata(xs1, ys1, zs1, (xs, ys))

    print resampled0
    omega_levels = [0.05,0.12,0.5,1]
    omega_levels0 = [0.10,0.14]

    plt.hot()
    fig = plt.figure(figsize=(7,9))
    ax1 = plt.axes([0.2,0.12,0.75,0.8])
    # plt.scatter(x0,y0,marker='o',c='b',s=5)
    cs1=ax1.contour(resampled0.T,omega_levels, colors='k',lw =2,extent=extent)
    cs2=ax1.contourf(resampled0.T,omega_levels0,extent=extent)
    #cs2=plt.imshow(resampled0.T,origin="lower",extent=extent)
    cl1=ax1.clabel(cs1,fmt='%1.2f',use_clabeltext=True,zorder = -1)
    ax1.set_title(r"$\Omega h^2$", size="large")
    ax1.set_xlabel(r"$M_D^B\mathrm{\,[GeV]}$", size="large")
    ax1.set_ylabel(r"$m_{\tilde{\tau}_R}\mathrm{\,[GeV]}$", size="large")
    # plt.savefig("/home/diessner/research/phd/rsymmetry/lightsinglet/omega_m1_mstau.pdf")
    #plt.xlim((0,50))
    #plt.ylim((70,210))

    plt.show()

def make_dd_plot(points):
    # extent = (100,55,50,500)
    extent = (400,1000,1000,3100)

    xs, ys = np.mgrid[extent[0]:extent[1]:50j, extent[2]:extent[3]:50j]
    x0 = [x[0] for x in points]
    y0 = [x[1] for x in points]
    print min(x0), max(x0)
    xy = [[x[0], x[1]] for x in points ]
    z0 = [x[3] for x in points   ]
    z1 = [10**x[4] for x in points   ]
    print z0
    resampled0 = griddata( xy,z0, (xs, ys),method='linear' )
    resampled1 = griddata( xy,z1, (xs, ys),method='linear' )
    # resampled1 = griddata(xs1, ys1, zs1, (xs, ys))

    print resampled0
    dd_levels = [1.5, 3, 5, 10, 50, 100, 500]
    p_levels = [0.01,  0.1,0.5]
    p_levels_1 = [ 0.05]
    fig = plt.figure(figsize=(8,9))
    ax1 = plt.axes([0.2,0.11,0.73,0.8])
    
    plt.hot()
    # plt.scatter(x0,y0,marker='o',c='b',s=5)
    cs1=ax1.contour(resampled1.T, levels=p_levels,colors='k',lw =8,extent=extent)
    cs2=ax1.contour(resampled1.T, levels=p_levels_1, colors='r',linewidths=[4],extent=extent)
    #cs2=plt.imshow(resampled0.T,origin="lower",extent=extent)
    cl1=ax1.clabel(cs1,fmt='%1.2f',use_clabeltext=True,zorder = -1)
    cl2=ax1.clabel(cs2,fmt='%1.2f',use_clabeltext=True,zorder = -1)
    ax1.set_title(r"$p$ value", size="large")
    ax1.set_xlabel(r"$\mu_u$ [GeV]", size="large")
    ax1.set_ylabel(r"$m_{sq_{1,2}}$ [GeV]", size="large")
    # plt.savefig("/home/diessner/research/phd/rsymmetry/lightsinglet/omega_m1_mstau.pdf")
    #plt.xlim((0,50))
    #plt.ylim((70,210))

    plt.show()


if __name__ == "__main__":
    
    db = "~/raid1/pointdbs/bm6_dm_mus_msq.db"
    points = points(db,
                    "select muu, msu3, omega, -loglike,pval from relic \
                    join points on points.identifier=relic.identifier \
                    join masses on points.identifier=masses.identifier")
    print points
    # make_omega_plot(points)
    make_dd_plot(points)
