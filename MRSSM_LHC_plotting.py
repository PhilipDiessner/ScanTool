import os.path as osp
import sqlite3
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.colors as col
import matplotlib.cm as cm
from scipy.interpolate import griddata
# from matplotlib.mlab import griddata
from matplotlib.backends.backend_pdf import PdfPages
from MRSSMfunctions import BM1, BM2,BM3,BM4
from Init import points
from MRSSMplotting import nans

mpl.rcParams.update({'font.size': 20})


# db = "~/raid1/pointdbs/ lhc_mus_mdw_heavy_rsleptons_m1_10.db"
# db = "~/raid1/pointdbs/bm4_lhc_mus_mdw_heavy_rsleptons.db"
db2 = "~/raid1/pointdbs/lhc_mud_mstau_mdb50_heavy_sleptons_add.db"
db = "~/raid1/pointdbs/lhc_mud_muu_mdb50_light_rstau.db"
# db = "~/raid1/pointdbs/pMSSMewinos.db"
# bm4_lhc_mud_mdw.db bm6_lhc_mud_mdw2.db
lhc_points = points(db,
                      "select  mud, muu, cl from lhc \
                      join points on points.identifier=lhc.identifier \
                      join masses on points.identifier=masses.identifier \
                      where analysis='best' and cl != -1")
# lhc_points += points(db2,
#                       "select  mchi2, mse1, cl from lhc \
#                       join points on points.identifier=lhc.identifier \
#                       join masses on points.identifier=masses.identifier \
#                       where analysis='best' and cl != -1 ")
                      # where analysis='atlas_1403_5294'")
# lhc_points = points(db,
#                       "select mu, m2, cl from lhc \
#                       join points on points.identifier=lhc.identifier \
#                       where analysis='best' and cl > 0")
# "atlas_1402_7029" "atlas_1403_5294" "best"
print lhc_points
if db == "~/raid1/pointdbs/bm4_lhc_mdb_mstau.db":
    del lhc_points[10]
N = 15j
if db == "~/raid1/pointdbs/lhc_mus_mdw_mdb50_light_rstau.db":
    del lhc_points[24]
if db == "~/raid1/pointdbs/lhc_mud_mstau_mdb50_heavy_sleptons.db":
    del lhc_points[28]
# extent= (70,220,5,60)
extent = (100,600,100,600)
# extent = (200,1200,1000,3100)
#del lhc_points[5]
# del lhc_points[9]
xs, ys = np.mgrid[extent[0]:extent[1]:100j, extent[2]:extent[3]:100j]
high = [[x[0],x[1],x[2]] for x in lhc_points
           ]# if x[2] > 0.12]
xy = [[x[0],x[1]] for x in lhc_points
           ]
x0 = [x[0] for x in lhc_points
           ]
y0 = [x[1] for x in lhc_points
           ]
z0 = [x[2] for x in lhc_points
           ]
print z0
# xs0, ys0, zs0 = np.transpose(high)
resampled0 = griddata( xy, z0, (xs, ys), method='cubic' )
# resampled0 = griddata(x0, y0, z0, xs, ys)
# xi = np.linspace(90,210,100)
# yi = np.linspace(0,60,60)
# zi = griddata(x0, y0, z0, xi, yi)
# print resampled0,zi
lhc_levels = [0.01,0.1]
lhc_levels2 = [0.05]
# cs1 = plt.contour(xi,yi,zi,15,lw=2,colors='b')
fig = plt.figure(figsize=(8,8))
ax1 = plt.axes([0.15,0.15,0.75,0.75])
cs1=plt.contour(resampled0.T,lhc_levels, colors='b',lw =2,extent=extent)
#cs2=plt.imshow(resampled0.T,origin="lower",extent=extent)
cs2=plt.contour(resampled0.T,lhc_levels2, colors='r',lw =4,extent=extent)
cl1=plt.clabel(cs1,fmt='%1.2f',use_clabeltext=True,zorder = -1)
cl2=plt.clabel(cs2,fmt='%1.2f',use_clabeltext=True,zorder = -1)
# plt.title(r"$CL_S$ value ($CL_S<0.05$ is excluded )")

# plt.ylabel(r"$M_W^D$ [GeV]", size="large")
plt.xlabel(r"$\mu_d$ [GeV]", size="large")
plt.ylabel(r"$\mu_u$ [GeV]", size="large")
# plt.ylabel(r"$m_{\tilde{\tau}_R}$ [GeV]", size="large")
# plt.xlabel(r"$m_{\chi_2^0,\chi_1^\pm}$ [GeV]", size="large")
# plt.scatter(x0,y0,marker='o',c='b',s=5)
plt.title(r"$m_{\chi_1^0}=50$ GeV, $m_{\tilde{\tau}_R}=100$ GeV, $M_W^D=600$ GeV",
          y=1.02, size="large")
plt.plot((200,600),(200,400),'k--,')
plt.plot((200,200),(100,600),'k--,')
# plt.xlabel(r"$M_B^D$ [GeV]")
# plt.ylabel(r"$m_{\tilde{\tau}_R}\approx m_{\tilde{\mu}_R}\approx m_{\tilde{e}_R}$ [GeV]")
#plt.xlim((0,50))
#plt.ylim((70,210))
# these are matplotlib.patch.Patch properties
props = dict(boxstyle='round', facecolor='wheat', alpha=0.8)
plt.text(120,330, "Soft 3-body\ndecays", bbox=props)
plt.text(220,530, "Down-Higgsino-like production,\nmainly decay with stau", bbox=props)
plt.text(270,150, "Up-Higgsino-like production,\ncompeting decays to\nZ/W, Higgs", bbox=props)
plt.savefig("/home/diessner/research/phd/rsymmetry/lhcstudy/mrssm_talk_mud_muu_light_stau.pdf")
# plt.savefig("/home/diessner/research/phd/rsymmetry/lhcstudy/mssm_mchi2_mstau.pdf")
plt.show()
