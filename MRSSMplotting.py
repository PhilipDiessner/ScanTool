import os.path as osp
import sqlite3
import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
import matplotlib.colors as col
import matplotlib.cm as cm
from scipy.interpolate import griddata
from matplotlib.mlab import griddata as gridd
from matplotlib.backends.backend_pdf import PdfPages
from MRSSMfunctions import BM1, BM2,BM3,BM4
from Init import points

plt.rcParams.update({'font.size': 24})

def nans(shape, dtype=float):
    """grid of shape full nan"""
    a = np.empty(shape, dtype)
    a.fill(np.nan)
    return a

def points_with_correct_mh_mw1(infile):
    result_db = osp.expanduser(infile)
    conn = sqlite3.connect(result_db)
    c = conn.cursor()
    c.arraysize = 100
    out = []
    c.execute('''SELECT points.mbdrc, points.ms2, points.lamtu, mhmw.mh1, mhmw.mh2, hbhs.hbexcl, hbhs.p 
              FROM points
              JOIN mhmw ON mhmw.identifier = points.identifier
              JOIN hbhs ON hbhs.identifier = points.identifier''')
    for i in c:
        out.append(i)
    print len(out)
    print out[-1]
    conn.close()
    return tuple(out)

def correct_points(infile,BMfunc,index):
    parameters = ["tanb", "lamsd", "lamsu", "lamtd", "lamtu", 
                 "mud", "muu", "bmu", "mq2", "mq332", "ml2", 
                 "ml332", "mu2", "mu332", "md2", "md332", 
                 "me2", "me332", "mru2", "mrd2", "mo2", 
                 "mbdrc", "mwdrc", "modrc", "ms2", "mt2"]
    values = BMfunc()
    print len(values)
    values.pop(index)
    parameter = parameters.pop(index)
    listing = []
    for i in range(len(values)):
        listing.append(parameters[i])
        listing.append(values[i])
    func = ('SELECT points.{}, mhmw.mh1, mhmw.mh2, points.identifier ' 
            'FROM points JOIN mhmw ON mhmw.identifier = points.identifier ' 
            'WHERE ').format(parameter) + \
            ((len(values)-1) * 'points.{} = {} AND '
             + 'points.{} = {}').format(*listing)
    result_db = osp.expanduser(infile)
    conn = sqlite3.connect(result_db)
    c = conn.cursor()
    c.arraysize = 100
    out = []
    c.execute(func)
    for i in c:
        out.append(i)
    #print len(out)
    #print out[-1]
    conn.close()
    return out

def points_two_tables(infile1,infile2):
    attach = 'ATTACH \"'+ osp.expanduser(infile2)+ '\" AS AM' 
    func = ('SELECT points.mwdrc,points.muu, AM.lhc3.r,points.identifier ' 
            'FROM points JOIN AM.lhc3 '
            'ON AM.lhc3.identifier = points.identifier')
    print func
    result_db = osp.expanduser(infile1)
    conn = sqlite3.connect(result_db)
    c = conn.cursor()
    c.arraysize = 100
    out = []
    c.execute(attach)
    c.execute(func)
    for i in c:
        out.append(i)
    #print len(out)
    #print out[-1]
    conn.close()
    return out

def plotting(intuple,outfile):
    def nans(shape, dtype=float):
        a = np.empty(shape, dtype)
        a.fill(np.nan)
        return a
    intuple =  sorted(intuple, key=lambda x: (x[0],x[1]))
    print intuple[0]
    x,y,z,a,b,hb,hs,mix = intuple[0]
    singlet = []
    mixing = []
    hbhs = []
    setbefore = False
    for row in intuple:
        if row[0] == 30 and row[1] == 30*30:
            print row
        if row[0] == x and row[1] == y:
            if row[-3] == 1 and hb != 1:
                hb = 1
                hs = row[-2]
            elif row[-3] == hb and row[-2] > hs:
                hs = row[-2]

            if row[4]>122 or row[4]<128:
                if setbefore and abs(b-125)< abs(row[4]-125):
                    pass
                else:
                    b = row[4]
                    mix = row[-1]
                    a = row[3]
                    setbefore = True
        else:
            if hs > 0.05:
                permit = hb + 2
            else:
                permit = hb
            hbhs.append([x,np.sqrt(y),permit])
            singlet.append([x,np.sqrt(y),a])
            mixing.append([x,np.sqrt(y),mix])
            x,y,z,a,b,hb,hs,mix = row
            setbefore = False
    if hs > 0.05:
        permit = hb + 2
    else:
        permit = hb
    hbhs.append([x,np.sqrt(y),permit])
    singlet.append([x,np.sqrt(y),a])
    mixing.append([x,np.sqrt(y),mix])
    converted1 = np.asarray(singlet)
    converted3 = np.asarray(mixing)
    trconverted1 = np.transpose(converted1)
    converted2 = np.asarray(hbhs)
    xi = np.sort(np.unique(trconverted1[0]))
    yi = np.sort(np.unique(trconverted1[1]))
    print xi,yi
    xgrid,ygrid = np.meshgrid(xi,yi)
    zi1 = nans((len(yi),len(xi)))
    zi2 = nans((len(yi),len(xi)))
    zi3 = nans((len(yi),len(xi)))
    for z in converted1:
        xind=np.nonzero(xi == float(z[0]))[0][0]
        yind=np.nonzero(yi == float(z[1]))[0][0]
        zi1[yind][xind] = z[-1]
    for z in converted2:
        xind =np.nonzero(xi == float(z[0]))[0][0]
        yind=np.nonzero(yi == float(z[1]))[0][0]
        zi2[yind][xind] = z[-1]
    for z in converted3:
        xind =np.nonzero(xi == float(z[0]))[0][0]
        yind=np.nonzero(yi == float(z[1]))[0][0]
        zi3[yind][xind] = z[-1]
    #pp = PdfPages('/home/diessner/research/phd/rsymmetry/lightsinglettest.pdf')
    fig = plt.figure(figsize=(7,7))
    ax1 = plt.axes([0.15,0.15,0.8,0.8])
    ax1.grid(True)
    print zi2
    cpool = ["m","g","DeepSkyBlue","Gold"]
    cmap = col.ListedColormap(cpool, 'higgsmass')
    ax1.contourf(xi,yi,zi2,[-0.5,0.5,1.5,2.5,3.5],cmap=cmap)
    print zi1# np.arange(0,150,10)
    #cs1 = ax1.contour(xi,yi,zi1,np.arange(0,150,10),colors='r')
    #cl1 = ax1.clabel(cs1,fmt='%1.f',use_clabeltext=True)
    #cs2 = ax1.contour(xi,yi,zi3,[0.05,0.1,0.15,0.2,0.3,0.4,0.5,0.75],colors='b')
    # cl2 = ax1.clabel(cs2,fmt='%1.2f',use_clabeltext=True)
    ax1.set_xlabel(r"$M_B^D$",fontsize='large')
    ax1.set_ylabel(r"$m_S$",fontsize='large')
    ax1.text(0, 80, "allowed (yellow)",size='small')
    ax1.text(25, 90, "excluded HB&HS (red)",size='small')
    ax1.text(25, 35, "excluded HB (blue)",size='small')
    ax1.text(25, 70, "excluded HS (green)",size='small')
    plt.savefig(outfile)
    #pp.savefig()  
    #pp.close()
    
    plt.show()

def higgsmassplot(tree, onel,twol):
    tree = np.transpose(np.asarray(tree))
    onel = np.transpose(np.asarray(onel))
    twol = np.transpose(np.asarray(twol))
    print len(tree[1])
    ind = 2
    higgs = 4
    diffx = []
    diffy = []
    for i in xrange(len(onel[ind])):
        for j in xrange(len(twol[ind])):
            if onel[ind][i] == twol[ind][j]:
                diffx.append(onel[ind][i])
                diffy.append(twol[higgs][j]**2-onel[higgs][i]**2)
    fig = plt.figure(figsize=(5,7))
    ax1 = plt.axes([0.15,0.4,0.8,0.55])
    ax2 = plt.axes([0.15,0.05,0.8,0.25])
    ax1.plot(tree[ind],tree[higgs],'o',label='tree')
    ax1.plot(onel[ind],onel[higgs],'o',label=r'1L')
    ax1.plot(twol[ind],twol[higgs],'o',label=r'2L')
    ax2.plot(diffx, diffy, 'o')
    ax1.set_xlabel(r"$\Lambda_u$",fontsize='large')
    ax1.set_ylabel(r"$m_{h,SMlike}$",fontsize='large')
    ax1.legend(loc='best')
    ax2.set_ylabel(r"$m^2_{2L}-m^2_{1L}$",fontsize='large')
    #plt.show()
    plt.savefig("/home/diessner/research/phd/rsymmetry/lightsinglet/higgscomparison/lightsinglet_h2_lamtu.pdf")

def bm2lplots():
    # pp = PdfPages('/home/diessner/research/phd/rsymmetry/BM12l.pdf')
    bm = BM1
    
    mpl.rcParams.update({'font.size': 14})


    params = [1,2,4]
    labels = [r"$\lambda_d$",r"$\lambda_u$",r"$\Lambda_u$",r"$\mu_u\mathrm{\,[GeV]}$",r"$M_D^B$ [GeV]",
              r"$M_D^W$ [GeV]",r"$m_S$ [GeV]",r"$m_T$ [GeV]"]
    saving = ["lamsd","lamsu","lamtu","muu"]
    for a in range(len(params)):
        tree=  [x for x in correct_points("~/raid1/pointdbs/scantree.db", bm, params[a]) 
                if x[0]<3000]
        onel=  [x for x in correct_points("~/raid1/pointdbs/scan1l.db", bm, params[a]) 
                if x[0]<3000]
        twol=  [x for x in correct_points("~/raid1/pointdbs/scan2l.db", bm, params[a]) 
                if x[0]<3000]
        # exception points to be taken care of seperatly
        if a == 6:
            twol =  [x for x in twol if x[1]>50]  
        # for x in tree:
        #     if x[0]<3000:
        print onel
        tree = np.transpose(np.asarray(sorted(tree)))
        onel = np.transpose(np.asarray(sorted(onel)))
        twol = np.transpose(np.asarray(sorted(twol))) 
        diffx = [[],[]]
        diffy = [[],[]]
        for ind in [1,2]:
            for i in xrange(len(onel[ind])):
                for j in xrange(len(twol[ind])):
                    if onel[0][i] == twol[0][j]:
                        diffx[ind-1].append(onel[0][i])
                        diffy[ind-1].append((twol[ind][j]-onel[ind][i]))
        fig = plt.figure(figsize=(7,7))
        ax1 = plt.axes([0.17,0.35,0.80,0.60])
        # ax1 = plt.axes([0.2,0.4,0.75,0.55])
        ax2 = plt.axes([0.17,0.1,0.80,0.25])
        # ax2.plot(diffx[1], diffy[1], 'o')
        if bm == BM4:
            # ax1.set_ylim([0,200])
            ax1.plot(tree[0],tree[1],color='g',linestyle='--',label=r'tree', lw=2)
            ax1.plot(onel[0],onel[1],color='b',linestyle='--',label=r'1L', lw=2)
            ax1.plot(twol[0],twol[1],color='r',linestyle='--',label=r'loop', lw=2)
            
            ax1.plot(tree[0],tree[2],color='g',label=r'tree, second', lw=2)
            ax1.plot(onel[0],onel[2], color='b',label=r'1L, lightest', lw=2)
            ax1.plot(twol[0],twol[2],color='r',label=r'2L, higgs', lw=2)
            ax1.set_ylabel(r"$m_{H_1,H_2}\mathrm{\,[GeV]}$", size="x-large")
            ax2.plot(diffx[1], diffy[1], color='b', lw=2)
            ax2.plot(diffx[0], diffy[0], color='b', linestyle='--', lw=2)
        else:
            ax1.plot(tree[0],tree[1],color='g',label=r'tree', lw=2)
            ax1.plot(onel[0],onel[1], color='b',label=r'1L', lw=2)
            ax1.plot(twol[0],twol[1],color='r',label=r'2L', lw=2)
            ax1.set_ylabel(r"$m_{H_1}\mathrm{\,[GeV]}$", size="x-large")
            ax1.set_ylim([50,170]) 
            ax2.plot(diffx[0], diffy[0], color='b', lw=2)
            if bm == BM3 and params[a] ==1:
                ax2.set_ylim([4.7,4.8])
        ax2.set_xlabel(labels[a],fontsize='x-large')
        ax1.legend(loc='best',prop={'size':12})
        plt.setp(ax1.get_xticklabels(), visible=False)
        # ax1.text(-1.7, 75, r"$\tan\beta=50$",size="large")
        ax2.set_ylabel(r"$m_{2L}-m_{1L} \mathrm{\,[GeV]}$", size="x-large")
        ax2.get_yaxis().get_major_formatter().set_useOffset(False)
        # removes the subtraction of constant offset for small changes in large values
        ax1.set_ylim([55,170])
        # plt.show()
        plt.savefig("/home/diessner/research/phd/rsymmetry/papers/forflorian/img/" +
                   saving[a] + "bm1.pdf")
        # pp.savefig()
    # pp.close()

def plot_of_massdiff(points1,points2,points3=None,points4=None,
                     points5=None,points6=None,points7=None,points8=None):
    ## filter points that have grid spacing using mod. here 50
    # new1 = [[x[0],np.sqrt(x[1]),x[2]] for x in points1 if x[0] % 50 == 0 and x[1] % (100*100) ==0]
    # new2 = [[x[0],np.sqrt(x[1]),x[2]] for x in points2 if x[0] % 50 == 0 and x[1] % (100*100) ==0]
    # print [x[1] for x in points1]
    new1 = [[x[0],np.sqrt(x[1]),x[2]] for x in points1
            if x[1] == 2000*2000 and x[0] not in [1000]]
    new2 = [[x[0],np.sqrt(x[1]),x[2]] for x in points2
            if x[1] == 2000*2000 and x[0] not in [1000]]
    new5 = [[x[0],np.sqrt(x[1]),x[2]] for x in points1
            if x[1] == 10000*10000 and x[0] not in [2400,2500]]
    new6 = [[x[0],np.sqrt(x[1]),x[2]] for x in points2
            if x[1] == 10000*10000 and x[0] not in [2400,2500]]
    new9 = [[x[0],np.sqrt(x[1]),x[2]] for x in points7
            if x[1] == 2000*2000 and x[0] not in [2400,2500]]
    new10 = [[x[0],np.sqrt(x[1]),x[2]] for x in points8
             if x[1] == 2000*2000 and x[0] not in [2400,2500]]
    new3 = [[x[0],np.sqrt(x[1]),x[2]] for x in points3]
    new4 = [[x[0],np.sqrt(x[1]),x[2]] for x in points4]
    new7 = [[x[0],np.sqrt(x[1]),x[2]] for x in points5] # if x[0]<3100]
    new8 = [[x[0],np.sqrt(x[1]),x[2]] for x in points6] # if x[0]<3100]
    # add sort
    onel = np.transpose(np.asarray(new1))
    twol = np.transpose(np.asarray(new2))        
    onel2 = np.transpose(np.asarray(new3))
    twol2 = np.transpose(np.asarray(new4))       
    onel3 = np.transpose(np.asarray(new5))
    twol3 = np.transpose(np.asarray(new6))       
    onel4 = np.transpose(np.asarray(new7))
    twol4 = np.transpose(np.asarray(new8))   
    onel5 = np.transpose(np.asarray(new9))
    twol5 = np.transpose(np.asarray(new10))
    print twol
    print onel
    # xi=np.sort(np.unique(onel[0]))
    # yi=np.sort(np.unique(onel[1]))     
    # xi2=np.sort(np.unique(onel2[0]))
    # yi2=np.sort(np.unique(onel2[1]))
    diff =  twol[2]-onel[2]
    diff2 =  twol2[2]-onel2[2]
    diff3 =  twol3[2]-onel3[2]
    diff4 =  twol4[2]-onel4[2]
    diff5 =  twol5[2]-onel5[2]
    print diff
    # zi1=nans((len(yi),len(xi)))
    # zi2=nans((len(yi),len(xi)))
    # for i in xrange(len(new1)):
    #     xind=np.nonzero(xi == new1[i][0])[0][0]
    #     yind=np.nonzero(yi == new1[i][1])[0][0]
    #     zi1[yind][xind]=diff[i]
    # for i in xrange(len(new3)):
    #     xind=np.nonzero(xi2 == new3[i][0])[0][0]
    #     yind=np.nonzero(yi2 == new3[i][1])[0][0]
    #     zi2[yind][xind]=onel2[2][i]
    fig = plt.figure(figsize=(6,6))
    ax1 = plt.axes([0.12,0.1,0.83,0.85])

    # plt.grey()
    ax1.plot(onel[0], diff, color='b', ls='-', lw=4, label=r'MRSSM, $m_O=2$ TeV')
    ax1.plot(onel3[0],diff3,color='g', ls='--', lw=4,label=r'MRSSM, $m_O=10$ TeV')
    ax1.plot(onel5[0],diff5,color='r', ls='-',lw=2,label='MRSSM, no sgluon contrb.')
    ax1.plot(onel2[0],diff2,color='c', ls='--',lw=2,label='MSSM, no tree-level stop mixing')
    ax1.plot(onel4[0],diff4,color='m', ls='-.',lw=2,label='MSSM, strong stop mixing')
    #ax1.plot(twol3[0],twol3[2],label='2-loop')
    #ax1.plot(onel3[0],onel3[2],label='1-loop')
    # cs1=ax1.contour(xi,yi,zi1,np.arange(0,1500,100),colors='r',linestyles='dashed')
    # cl1=ax1.clabel(cs1,fmt='%1.1f',use_clabeltext=True)
    # cs2=ax1.contour(xi,yi,zi2,np.arange(0,13000,500),colors='b',linestyles='dashed')
    # cl2=ax1.clabel(cs2,fmt='%1.0f',use_clabeltext=True)
    # ax1.set_xlabel(r"$M_D^G$",fontsize='large')
    ax1.legend(loc='best')
    ax1.set_xlabel(r"$M^D_O\,\mathrm{[GeV]}$",fontsize='x-large')
    ax1.set_ylabel(r"$m_{2L}-m_{1L}\,\mathrm{[GeV]}$",fontsize='x-large')
    ax1.set_xlim([100,3000])
    ax1.set_ylim([-5,15])
    # ax1.set_ylim([-5,15])
    # ax1.text(1000, 127, r"$m_O=10000$ GeV",size="large")
    # ax1.text(200, 1000, r"$m_{h,2L}-m_{h,1L}$",size="x-large")
    # plt.show()
    plt.savefig("/home/diessner/research/phd/rsymmetry/higgstwoloop/higgs_mgl_mssm_bm3.pdf")

def plot_of_massdiff2(points1,points2,points3=None,points4=None,
                     points5=None,points6=None,points7=None,points8=None,points9=None,points10=None):
    ## filter points that have grid spacing using mod. here 50
    # new1 = [[x[0],np.sqrt(x[1]),x[2]] for x in points1 if x[0] % 50 == 0 and x[1] % (100*100) ==0]
    # new2 = [[x[0],np.sqrt(x[1]),x[2]] for x in points2 if x[0] % 50 == 0 and x[1] % (100*100) ==0]
    # print [x[1] for x in points1]
    new1 = [[x[0],np.sqrt(x[1]),x[2]] for x in points1
            if x[1] == 2000*2000 and x[0] not in [1000]]
    new2 = [[x[0],np.sqrt(x[1]),x[2]] for x in points2
            if x[1] == 2000*2000 and x[0] not in []]
    new3 = [[x[0],np.sqrt(x[1]),x[2]] for x in points3
            if x[1] == 2000*2000 and x[0] not in []]
    new4 = [[x[0],np.sqrt(x[1]),x[2]] for x in points4
            if x[1] == 2000*2000 and x[0] not in []]
    new5 = [[x[0],np.sqrt(x[1]),x[2]] for x in points5
            if x[1] == 2000*2000 and x[0] not in []]
    new6 = [[x[0],np.sqrt(x[1]),x[2]] for x in points6
            if x[1] == 2000*2000 and x[0] not in []]
    new7 = [[x[0],np.sqrt(x[1]),x[2]] for x in points7
            if x[1] == 2000*2000 and x[0] not in []]
    new8 = [[x[0],np.sqrt(x[1]),x[2]] for x in points8
            if x[1] == 2000*2000 and x[0] not in []]
    new9 = [[x[0],np.sqrt(x[1]),x[2]] for x in points9
             if x[1] == 2000*2000 and x[0] not in []]
    new10 = [[x[0],np.sqrt(x[1]),x[2]] for x in points10
             if x[1] == 2000*2000 and x[0] not in []]
    # add sort
    onel = np.transpose(np.asarray(new1))
    twol = np.transpose(np.asarray(new2))        
    onel2 = np.transpose(np.asarray(new3))
    twol2 = np.transpose(np.asarray(new4))       
    onel3 = np.transpose(np.asarray(new5))
    twol3 = np.transpose(np.asarray(new6))       
    onel4 = np.transpose(np.asarray(new7))
    twol4 = np.transpose(np.asarray(new8))   
    onel5 = np.transpose(np.asarray(new9))
    twol5 = np.transpose(np.asarray(new10))
    print twol
    print onel
    diff =  twol[2]-onel[2]
    diff2 =  twol2[2]-onel2[2]
    diff3 =  twol3[2]-onel3[2]
    diff4 =  twol4[2]-onel4[2]
    diff5 =  twol5[2]-onel5[2]
    print diff
    # zi1=nans((len(yi),len(xi)))
    # zi2=nans((len(yi),len(xi)))
    # for i in xrange(len(new1)):
    #     xind=np.nonzero(xi == new1[i][0])[0][0]
    #     yind=np.nonzero(yi == new1[i][1])[0][0]
    #     zi1[yind][xind]=diff[i]
    # for i in xrange(len(new3)):
    #     xind=np.nonzero(xi2 == new3[i][0])[0][0]
    #     yind=np.nonzero(yi2 == new3[i][1])[0][0]
    #     zi2[yind][xind]=onel2[2][i]
    fig = plt.figure(figsize=(6,6))
    ax1 = plt.axes([0.12,0.1,0.83,0.85])

    # plt.grey()
    ax1.plot(onel[0], diff, color='b', ls='-', lw=4, label=r'all contributions')
    ax1.plot(onel2[0],diff2,color='g', ls='--', lw=4,label=r'no sgluon')
    ax1.plot(onel3[0],diff3,color='r', ls=':',lw=4,label='and no gluino')
    ax1.plot(onel4[0],diff4,color='c', ls='-.',lw=4,label='and no gluon')
    ax1.plot(onel5[0],diff5,color='m', ls=':',lw=2,label=r'and no $\alpha_t^2$, $\alpha_t\alpha_b$')
    #ax1.plot(twol3[0],twol3[2],label='2-loop')
    #ax1.plot(onel3[0],onel3[2],label='1-loop')
    # cs1=ax1.contour(xi,yi,zi1,np.arange(0,1500,100),colors='r',linestyles='dashed')
    # cl1=ax1.clabel(cs1,fmt='%1.1f',use_clabeltext=True)
    # cs2=ax1.contour(xi,yi,zi2,np.arange(0,13000,500),colors='b',linestyles='dashed')
    # cl2=ax1.clabel(cs2,fmt='%1.0f',use_clabeltext=True)
    # ax1.set_xlabel(r"$M_D^G$",fontsize='large')
    ax1.legend(loc='best')
    ax1.set_xlabel(r"$M^D_O\,\mathrm{[GeV]}$",fontsize='x-large')
    ax1.set_ylabel(r"$m_{2L}-m_{1L}\,\mathrm{[GeV]}$",fontsize='x-large')
    ax1.set_xlim([100,3000])
    ax1.set_ylim([-2,9])
    # ax1.set_ylim([-5,15])
    # ax1.text(1000, 127, r"$m_O=10000$ GeV",size="large")
    # ax1.text(200, 1000, r"$m_{h,2L}-m_{h,1L}$",size="x-large")
    # plt.show()
    plt.savefig("/home/diessner/research/phd/rsymmetry/higgstwoloop/higgs_color_contrb.pdf")
    
def plot_mo_massdiff(points1,points2):
    new1 = [[x[0],np.sqrt(x[1]),x[2]] for x in points1 if x[0] == 1000]
    new2 = [[x[0],np.sqrt(x[1]),x[2]] for x in points2 if x[0] == 1000]
    new3 = [[x[0],np.sqrt(x[1]),x[2]] for x in points1 if x[0] == 5000]
    new4 = [[x[0],np.sqrt(x[1]),x[2]] for x in points2 if x[0] == 5000]
    onel = np.transpose(np.asarray(new1))
    twol = np.transpose(np.asarray(new2))        
    onel2 = np.transpose(np.asarray(new3))
    twol2 = np.transpose(np.asarray(new4))   
    diff =  twol[2]-onel[2]
    diff2 =  twol2[2]-onel2[2]
    fig = plt.figure(figsize=(7,7))
    ax1 = plt.axes([0.15,0.1,0.8,0.8])
    print diff
    print diff2
    ax1.plot(twol[1],diff,color='b',label=r"$M^D_O=1\,\mathrm{TeV}$")
    ax1.plot(twol2[1],diff2,color='g',label=r"$M^D_O=5\,\mathrm{TeV}$")
    ax1.set_xlabel(r"$m_O\,\mathrm{[GeV]}$",fontsize='x-large')
    #ax1.set_ylabel(r"$m_{h}\,\mathrm{[GeV]}$",fontsize='large')
    ax1.set_ylabel(r"$m_{2L}-m_{1L}\,\mathrm{[GeV]}$",fontsize='x-large')
    ax1.legend(loc='best')
    plt.show()
    plt.savefig("/home/diessner/research/phd/rsymmetry/higgstwoloop/dmh_mso.pdf")

def simpleplot(points1):
    new1 = [[x[0],np.sqrt(x[1]),abs(x[2]),abs(x[3]),abs(x[4]),abs(x[5])] for x in points1 if x[1] == 1000*1000]
    onel = np.transpose(np.asarray(new1))
    fig = plt.figure(figsize=(7,7))
    ax1 = plt.axes([0.15,0.1,0.8,0.8])
    print onel[3]
    ax1.plot(onel[0],onel[2],label=r"$Z^h_{1,1}$")
    ax1.plot(onel[0],onel[3],label=r"$Z^h_{1,2}$")
    ax1.plot(onel[0],onel[4],label=r"$Z^h_{1,3}$")
    ax1.plot(onel[0],onel[5],label=r"$Z^h_{1,4}$")
    ax1.set_xlabel(r"$m_O\,\mathrm{[GeV]}$",fontsize='x-large')
    ax1.legend(loc='best')
    ax1.set_ylim([0,0.2])
    plt.show()

def bm4plots(treep,onelp,twolp):
    tree = np.transpose(np.asarray(treep))
    onel = np.transpose(np.asarray(onelp))
    twol = np.transpose(np.asarray(twolp))
    print treep
    diffx = [[],[]]
    diffy = [[],[]]
    for ind in [1,2]:
        for i in xrange(len(onel[ind])):
            for j in xrange(len(twol[ind])):
                if onel[0][i] == twol[0][j]:
                    diffx[ind-1].append(onel[0][i])
                    diffy[ind-1].append((twol[ind][j]-onel[ind][i]))
                
    fig = plt.figure(figsize=(5,6))
    ax1 = plt.axes([0.14,0.35,0.82,0.60]) 
    ax2 = plt.axes([0.14,0.1,0.82,0.25])          
    ax1.plot(tree[0],tree[1],color='g',linestyle='--',label=r'tree', lw=2)
    ax1.plot(onel[0],onel[1],color='b',linestyle='--',label=r'1L', lw=2)
    ax1.plot(twol[0],twol[1],color='r',linestyle='--',label=r'loop', lw=2)
    
    ax1.plot(tree[0],tree[2],color='g',label=r'tree, second', lw=2)
    ax1.plot(onel[0],onel[2], color='b',label=r'1L, lightest', lw=2)
    ax1.plot(twol[0],twol[2],color='r',label=r'2L, higgs', lw=2)
    ax1.set_ylabel(r"$m_{H_1,H_2}\mathrm{\,[GeV]}$", size="x-large")
    ax2.plot(diffx[1], diffy[1], color='b', lw=2)
    ax2.plot(diffx[0], diffy[0], color='b', linestyle='--', lw=2)
    ax2.set_xlabel(r'$\Lambda_u$',fontsize='x-large')
    ax1.legend(loc='best',prop={'size':12})
    plt.setp(ax1.get_xticklabels(), visible=False)
    # ax1.text(-1.7, 75, r"$\tan\beta=50$",size="large")
    ax2.set_ylabel(r"$m_{2L}-m_{1L} \mathrm{\,[GeV]}$", size="x-large")
    ax2.get_yaxis().get_major_formatter().set_useOffset(False)
    # removes the subtraction of constant offset for small changes in large values
    ax1.set_ylim([55,170])
    # plt.show()
    plt.savefig("/home/diessner/research/phd/rsymmetry/lightsinglet/higgscomparison/bm4_lamtu_levels.pdf")

    fig.clear()
    ax1 = plt.axes([0.13,0.1,0.82,0.85]) 
    ax1.plot(tree[0],abs(tree[4]**2),color='g',linestyle='--',label=r'tree, $H_1$', lw=2)
    ax1.plot(onel[0],abs(onel[4]**2),color='b',linestyle='--',label=r'1L, $\phi_S$ -', lw=2)
    ax1.plot(twol[0],abs(twol[4]**2),color='r',linestyle='--',label=r'2L, content', lw=2)
    ax1.plot(tree[0],abs(tree[3]**2),color='g',label=r'tree, $H_1$', lw=2)
    ax1.plot(onel[0],abs(onel[3]**2), color='b',label=r'1L, $\phi_u$ -', lw=2)
    ax1.plot(twol[0],abs(twol[3]**2),color='r',label=r'2L, content', lw=2)
    ax1.legend(loc='best',prop={'size':12})
    ax1.set_xlabel(r'$\Lambda_u$',fontsize='x-large')
    plt.savefig("/home/diessner/research/phd/rsymmetry/lightsinglet/higgscomparison/bm4_lamtu_h1_content.pdf")

    fig.clear()
    ax1 = plt.axes([0.13,0.1,0.82,0.85]) 
    ax1.plot(tree[0],abs(tree[6]**2),color='g',linestyle='--',label=r'tree, $H_2$', lw=2)
    ax1.plot(onel[0],abs(onel[6]**2),color='b',linestyle='--',label=r'1L, $\phi_S$ -', lw=2)
    ax1.plot(twol[0],abs(twol[6]**2),color='r',linestyle='--',label=r'2L, content', lw=2)
    ax1.plot(tree[0],abs(tree[5]**2),color='g',label=r'tree, $H_2$', lw=2)
    ax1.plot(onel[0],abs(onel[5]**2), color='b',label=r'1L, $\phi_u$ -', lw=2)
    ax1.plot(twol[0],abs(twol[5]**2),color='r',label=r'2L, content', lw=2)
    ax1.legend(loc='best',prop={'size':12})
    ax1.set_xlabel(r'$\Lambda_u$',fontsize='x-large')
    # plt.show()
    plt.savefig("/home/diessner/research/phd/rsymmetry/lightsinglet/higgscomparison/bm4_lamtu_h2_content.pdf")

def mass_mixing_plot(intuple,outfile):
    good = []
    bothbad = []
    hbbad = []
    hsbad = []
    for entry in intuple:
        if entry[-2] == 1:
            if entry[-1]>0.1:
                good.append(entry[:2])
            else:
                hsbad.append(entry[:2])
        else:
            if entry[-1]>0.1:
                hbbad.append(entry[:2])
            else:
                bothbad.append(entry[:2])
    fig = plt.figure(figsize=(6,6))
    ax1 = plt.axes([0.14,0.15,0.8,0.8])
    print len(good)
    ax1.plot([p[0] for p in good],[p[1] for p in good],'dy',label="good points")
    ax1.plot([p[0] for p in hbbad],[p[1] for p in hbbad],'db',label="HB excluded")
    ax1.plot([p[0] for p in hsbad],[p[1] for p in hsbad],'dg',label="HS excluded")
    ax1.plot([p[0] for p in bothbad],[p[1] for p in bothbad],'dm',label="both excluded")
    ax1.legend(loc='best',prop={'size':12})
    ax1.set_ylabel(r"$Z^2_{H,12}$ (doublet content)", size="x-large")
    ax1.set_xlabel(r"$m_{H_1}\mathrm{\,[GeV]}$", size="x-large")
    plt.show()
    # plt.savefig(outfile)

def higgses_masses(intuple):
    plt.rcParams.update({'font.size': 24})
    print len(zip(*intuple[:10]))
    [x,y1,y2,y3,y4,z1,z2,z3,z4] = zip(*intuple)
    x = [np.sqrt(q) for q in x] # for ms2
    fig = plt.figure(figsize=(6,9))
    ax1 = plt.axes([0.22,0.12,0.7,0.8])
    # ax1.plot(x,z1)
    # ax1.plot(x,z2)
    # ax1.plot(x,z3)
    # ax1.plot(x,z4)
    b1 = []
    b2 = []
    xi1=[]
    xi2=[]
    yi11=[]
    yi12=[]
    yi21=[]
    yi22=[]
    for i in range(len(x)):
        if z1[i]>0.5:
            b1.append(y1[i]-120.)
            xi1.append(x[i])
            yi11.append(y1[i])
            yi22.append(y2[i])
        else:
            b2.append(y2[i]-120.)
            xi2.append(x[i])
            yi12.append(y1[i])
            yi21.append(y2[i])

    # ax1.plot(xi1,yi11,lw=3,c='g')
    # ax1.plot(xi2,yi12,lw=3,c='b')
    # ax1.plot(xi2,yi21,lw=3, c='g')
    # ax1.plot(xi1,yi22,lw=3, c='b')
    # ax1.plot((0, 200), (125, 125), 'k--')
    # ax1.set_ylabel(r"$M_{H_i}\mathrm{\,[GeV]}$", size="large")
    # ax1.set_ylim([10,150])
    
    ax1.plot(xi1, b1,lw=3, c='g')
    ax1.plot(xi2, b2,lw=3, c='g')
    ax1.set_ylabel(r"$m_{H,SM}-m_{H,ref}\mathrm{\,[GeV]}$", size="large")
    ax1.set_ylim([-10,15])
    
    # ax1.plot(x, z1,lw=3, c='g')
    # ax1.plot(x, z2,lw=3, c='b')
    # ax1.set_ylabel(r"$(Z^H_{1j})^2$", size="large")
    # ax1.set_ylim([0,1])

    ax1.set_xlim([0,125])
    ax1.set_xlabel(r"$m_S\mathrm{\,[GeV]}$", size="large")
        
    plt.savefig("/home/diessner/research/phd/rsymmetry/bm6_higgs_mass_splitting_massdiff_ms2.pdf")
    plt.show()
    
if __name__ == "__main__":
    command = 'SELECT points.mbdrc, points.ms2, points.lamtu,mhh1, masses.mhh2,\
    hbhs.hbexcl, hbhs.p, zh12*zh12\
    FROM points \
    JOIN masses ON masses.identifier = points.identifier \
    JOIN hbhs ON hbhs.identifier = points.identifier \
    JOIN hmix ON hmix.identifier = points.identifier \
    WHERE lamsu=0' #mhh2<128 and mhh2>122 and zh12*zh12>0.1 and zh12*zh12<0.15'
    newp = points("~/raid1/pointdbs/light_singlet_large_mus.db",command)
    # newp2 = points("~/raid1/pointdbs/light_singlet_large_mus_neglam.db",command)
    
    # newp3 = points("~/raid1/pointdbs/light_singlet_large_mus_constLam.db",command)
    # command = 'SELECT points.mbdrc, points.ms2, points.lamtu,mhh1, masses.mhh2,\
    # hbhs.hbexcl, hbhs.p, zh12*zh12\
    # FROM points \
    # JOIN masses ON masses.identifier = points.identifier \
    # JOIN hbhs ON hbhs.identifier = points.identifier \
    # JOIN hmix ON hmix.identifier = points.identifier \
    # WHERE (1.414*lamsu*700+0.362*mbdrc)>5 and (1.414*lamsu*700+0.362*mbdrc)<20'
    # newp4 = points("~/raid1/pointdbs/light_singlet_offdiag.db",command)
    # 1-(246*0.362*mbdrc)*(246*0.362*mbdrc)/((4*mbdrc*mbdrc+ms2-mhh1*mhh1)*(4*mbdrc*mbdrc+ms2-mhh1*mhh1)+(246*0.362*mbdrc)*(246*0.362*mbdrc))\
    # and 246*abs(1.4142*lamsu*muu+0.362*mbdrc)<60*60 and 246*abs(1.4142*lamsu*muu+0.362*mbdrc)>40*40
    outfile = "/home/diessner/research/phd/rsymmetry/lightsinglet/exclusion_0_new.pdf"
    # command = 'select mhh1, zh23*zh23,lamsu,mbdrc,ms2 , hbexcl, hbhs.p from hmix \
    # join masses on hmix.identifier=masses.identifier join hbhs on hbhs.identifier=hmix.identifier \
    # join points on points.identifier=hmix.identifier \
    # where mhh2>123 and mhh2<127'
    # newp = points("~/raid1/pointdbs/light_singlet_large_mus.db",command)
    # newp2 = points("~/raid1/pointdbs/light_singlet_large_mus_neglam.db",command)
    
    # mass_mixing_plot(newp+newp2,outfile)
    plotting(newp,outfile)
    # points_with_correct_mh_mw1("~/raid1/pointdbs/lightsinglethbhs.db")
    # higgsmassplot(points_with_correct_mh_mw2("~/raid1/pointdbs/lightsinglettree.db"), 
    #               points_with_correct_mh_mw2("~/raid1/pointdbs/lightsinglet3.db")
    #               +points_with_correct_mh_mw2("~/raid1/pointdbs/lightsinglet4.db"),
    #               points_with_correct_mh_mw2("~/raid1/pointdbs/lightsinglet2l.db"))
    # bm2lplots()
    # print correct_points("~/raid1/pointdbs/scan2l.db", BM4,-2)

    # command= "select points.modrc, points.mo2, hmix.zh11, hmix.zh12, hmix.zh13, hmix.zh14 from points join hmix on points.identifier = hmix.identifier "
    # points1 = points("~/research/colnolambda1l.db",command)
    # points2 = points("~/research/colnolambda2l.db",command)
    # points1 = points("~/research/lowmo1l.db",command)
    # print points1
    # points2 = points("~/raid1/pointdbs/lowmo2l.db",command)
    # simpleplot(points1)
    command = "select points.m3,points.m2, mhmw.mh1 from points join mhmw on points.identifier = mhmw.identifier"
    # # points1 = points("~/raid1/pointdbs/MSSMcol1l.db",command)
    # # points2 = points("~/raid1/pointdbs/MSSMcol2l.db",command)
    # points3 = points("~/raid1/pointdbs/MSSMbm31lnomix.db",command)
    # points4 = points("~/raid1/pointdbs/MSSMbm32lnomix.db",command)
    # points5 = points("~/raid1/pointdbs/MSSMbm31lfullmix.db",command)
    # points6 = points("~/raid1/pointdbs/MSSMbm32lfullmix.db",command)
    # command = "select points.modrc, points.mo2, mhmw.mh1 from points join mhmw on points.identifier = mhmw.identifier "
    # points1 = points("~/raid1/pointdbs/glbm31l.db",command)
    # points2 = points("~/raid1/pointdbs/glbm32l.db",command)
    # points7 = points("~/raid1/pointdbs/glbm31lnoso.db",command)
    # points8 = points("~/raid1/pointdbs/glbm32lnoso.db",command)
    # #plot_of_massdiff(points1,points2,points3,points4,points5,points6,points7,points8)
    # points1 = points("~/raid1/pointdbs/bm3all1l.db",command)
    # points2 = points("~/raid1/pointdbs/bm3all2l.db",command)
    # points3 = points("~/raid1/pointdbs/bm3noso1l.db",command)
    # points4 = points("~/raid1/pointdbs/bm3noso2l.db",command)  
    # points5 = points("~/raid1/pointdbs/bm3nosogo1l.db",command)
    # points6 = points("~/raid1/pointdbs/bm3nosogo2l.db",command)  
    # points7 = points("~/raid1/pointdbs/bm3nosogovg1l.db",command)
    # points8 = points("~/raid1/pointdbs/bm3nosogovg2l.db",command)  
    # points9 = points("~/raid1/pointdbs/bm3nosogovgyu1l.db",command)
    # points10 = points("~/raid1/pointdbs/bm3nosogovgyu2l.db",command)  
    # # print len(points1),len(points2)
    # command = "select points.modrc, points.mo2, mhmw.mh1, mgmso.mso from points join mhmw on points.identifier = mhmw.identifier join mgmso on points.identifier = mgmso.identifier "
    # # points3 = points("~/raid1/pointdbs/lightsingletcol1l.db",command)

    # plot_of_massdiff2(points1,points2,points3,points4,points5,points6,points7,points8,points9,points10)

    # points1 = points("~/raid1/pointdbs/lightsingletcol1l.db",command)
    # points2 = points("~/raid1/pointdbs/lightsingletcol2l.db",command)
    # plot_mo_massdiff(points1,points2)
    # command = "select points.lamtu, mhmw.mh1, mhmw.mh2, hmix.zh12,hmix.zh13,hmix.zh22, hmix.zh23\
    # from points \
    # join mhmw on points.identifier = mhmw.identifier \
    # join hmix on points.identifier = hmix.identifier"

    # tree = points("~/raid1/pointdbs/bm4ltutree.db",command)
    # onel = points("~/raid1/pointdbs/bm4ltu1l.db",command)
    # twol = points("~/raid1/pointdbs/bm4ltu2l.db",command)
    # bm4plots(tree,onel,twol)
    # mhh1,mhh2,mhh3,mhh4\zh12*zh12, zh13*zh13,zh22*zh22,zh23*zh23
    # command = 'SELECT points.ms2, mhh1,mhh2,mhh3,mhh4,zh12*zh12, zh13*zh13,zh22*zh22,zh23*zh23\
    # FROM points \
    # JOIN masses ON masses.identifier = points.identifier\
    # JOIN hmix ON hmix.identifier = points.identifier\
    # WHERE mbdrc=30'
    # newp = points("~/raid1/pointdbs/bm6_mixing_scan.db",command)
    # higgses_masses(newp)
