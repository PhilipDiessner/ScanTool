import numpy as np
import scipy as sp
from scipy.interpolate import interp1d,RectBivariateSpline
from matplotlib import pyplot as plt

from Init import points
from Run import runwrapper, partial_runwrapper, touch#, replace_line_in_file


NLL = "/afs/desy.de/user/d/diessner/theorie/nllfast/nllfast"
NLLpath = "/afs/desy.de/user/d/diessner/theorie/nllfast/"
NNLL = "/afs/desy.de/user/d/diessner/theorie/nnllfast/nnllfast"
NNLLpath = "/afs/desy.de/user/d/diessner/theorie/nnllfast/"

ss="/afs/desy.de/user/d/diessner/theorie/pointdbs/NLO_xsec_qlqr.db"
sb="/afs/desy.de/user/d/diessner/theorie/pointdbs/NLO_xsec_qlql.db"

class GridDB(object):
    """
    Interpolation Grid for K factor
    only for nlo xsec we have octet dependence
    """

    def __init__(self,db,tablenames):
        """
        db contains several nlo tables for octet mass and lo table
        """
        self.db = db
        self.names = tablenames
        # set up interpolate grids
        self.grids = [self.getGridFunc(x) for x in tablenames]
        

    def getGridFunc(self,table):
        """
        2D interpolation in msquark mgluino
        """
        # read grids from db
        command = "select * from "+table
        data = np.asarray(points(self.db,command))
        x0 = np.unique(data[:,1])
        y0 = np.unique(data[:,2])
        z0  = data[:,4]
        z0 = np.reshape(z0,[x0.size,y0.size])
        return  RectBivariateSpline(x0,y0,z0, kx=1, ky=1)

    def xsecs(self,msq,mgl):
        """xsec in pb, also works for msq mgl as vectors"""
        return [grid.ev(msq,mgl) for grid in self.grids]

    def interpolmo(self,msq,mgl):
        """returns function interpolation for mo for given msq mgl """
        mo=[]
        xsec=[]
        for i,tab in enumerate(self.names):
            try:
                mo.append(float(tab[1:]))
                xsec.append(self.grids[i].ev(msq,mgl))
            except:
                pass
        return interp1d(mo,xsec,kind="cubic")

def MSSMKfaccompare(msq,mgl,pro):
    nlloutput=runwrapper([NLL, pro,"nnpdf",str(msq),str(mgl)],NLLpath)
    nnlloutput=runwrapper([NNLL, pro,str(msq),str(mgl)],NNLLpath)
    
    Knlo = float(nlloutput.split()[-2])#/float(nlloutput.split()[-11])
    Knll = float(nlloutput.split()[-1])
    Knnl = float(nnlloutput.split()[-1])
    return [Knlo,Knlo*Knll,Knlo*Knnl]

def Kplot():
    mgl=1500
    process = 'ss'
    res = []
    msqx = xrange(500,3001,100)
    for msq in msqx:
        res.append(MSSMKfaccompare(msq,mgl,process))
    knlo = [x[0] for x in res]
    knll = [x[1] for x in res]
    knnl = [x[2] for x in res]
    print res
    plt.plot(msqx,knlo,label = 'K(NLO/LO)')
    plt.plot(msqx,knll,label = 'K(NLL/LO)')
    plt.plot(msqx,knnl,label = 'K(NNLL/LO)')
    plt.legend(loc='best')
    plt.ylabel("K")
    plt.xlabel(r"$m_{\tilde q}$ [GeV]")
    plt.title(r"$m_{\tilde g}=1.5$ GeV, $\tilde q \tilde q$")
    plt.savefig("Kss.pdf")
    plt.show()
    
def MSSMKfac(msq,mgl,process = ["gg","ss","sb","sg"]): 
    lo=0
    nlo=0
    for pro in process:
        nlloutput=runwrapper([NLL, pro,"mstw",str(msq),str(mgl)],NLLpath)  
        lo += float(nlloutput.split()[-11])
        nlo += float(nlloutput.split()[-10])
    return nlo/lo

def MRSSMKfacgen(process = ["gg","ss","sb","sg"]):
    tabs = [ "t1000","t3000", "t10000","t30000", "t100000","lo" ]
    tabs = ["t10000","lo"]
    ssgr = GridDB(ss,tabs)
    sbgr = GridDB(sb,tabs)
    
    def MRSSMKfac(msq,mgl,process = process): 
        nlo = np.zeros(len(tabs))
        for pro in process:
            if pro in ["gg","sg"]:
                if msq >3000:
                    msqg = 3000
                else:
                    msqg= msq
                if mgl >3000:
                    mglg = 3000
                else:
                    mglg = mgl
                nlloutput=runwrapper([NLL, pro,"mstw",str(msqg),str(mglg)],NLLpath)
                nlo[-1] += float(nlloutput.split()[-11]) # LO
                nlo[:-1] += float(nlloutput.split()[-10]) #NLO
            elif pro == "ss":
                #print msq,mgl, ssgr.xsecs(msq,mgl)
                temp = np.asarray([x for x in ssgr.xsecs(msq,mgl)])
                #print temp
                nlo += temp
            elif pro == "sb":
                #print msq,mgl, sbgr.xsecs(msq,mgl)
                temp = np.asarray([x for x in sbgr.xsecs(msq,mgl)])
                #print temp
                nlo += temp
        
        lo = nlo[-1]
        nlo = nlo[:-1]
        return [x/lo for x in nlo]
    
    return MRSSMKfac
    
def MRSSMKfacsgluon(msq,mgl,process = ["ss","sb"]): 
    tabs = [ "t1000", "t100000", "t10000" ]
    ssgr = GridDB(ss,tabs)
    sbgr = GridDB(sb,tabs)
    nlo = np.zeros(len(tabs))
    for pro in process:
        
        if pro == "ss":
            temp = np.asarray([x for x in ssgr.xsecs(msq,mgl)])
            #print temp
            nlo += temp
        elif pro == "sb":
            temp = np.asarray([x for x in sbgr.xsecs(msq,mgl)])
            #print temp
            nlo += temp
    lo = nlo[-1]
    nlo = nlo[:-1]
    return [x/lo for x in nlo]
    
    
def NNLLKfac(msq,mgl,process = ["gg","ss","sb","sg"]): 
    nlo = 0
    nnl = 0
    pdf = 0
    if msq >3000:
        msq = 3000
    if mgl >3000:
        mgl = 3000
    for pro in process:
        nlloutput=runwrapper([NNLL, pro,str(msq),str(mgl)],NNLLpath).split("\n")[-2].split()
        #print nlloutput
        nnl += float(nlloutput[3])
        nlo += float(nlloutput[2])
        pdf += float(nlloutput[2])*float(nlloutput[6])/100.
    pdf = pdf/nlo
    return nnl/nlo

def MRSSMnloanduncert(lo,msq,mgl,process = ["gg","ss","sb","sg"],MRSSMKfac=None):
    sgluon = MRSSMKfacsgluon(msq,mgl,process)
    nll = NNLLKfac(msq,mgl,process)
    nlok = lo*MRSSMKfac(msq,mgl,process)[0]
    up = np.sqrt((sgluon[-1]-1)**2+(nll-1)**2)
    down = np.sqrt((sgluon[0]-1)**2+(nll-1)**2)
    #print nlok,nlok*(1+up),nlok/(1+down)
    return [nlok,nlok*(1+up),nlok/(1+down)]
    
if __name__ == "__main__":
    #print(points(db,".tables"))
    #print MSSMKfac(1100,500)
    #MRSSMKfac= MRSSMKfacgen(process = ["ss","sb"])
    #for mgl in xrange(2000,4000,200):
    #    print MRSSMKfac(900,mgl)
    #test = GridDB(ss,[ "t1000","t3000", "t10000","t30000", "t100000" ])
    #print (test.interpolmo(500,500))(2000)
    Kplot()
