import numpy as np
import scipy as sp
from scipy.interpolate import interp1d,RectBivariateSpline
    
from Init import points
from Run import runwrapper, partial_runwrapper, touch#, replace_line_in_file

NLL = "/home/diessner/research/nllfast/nllfast"
NLLpath = "/home/diessner/research/nllfast/"
ss="research/rsymmetry/NLO_xsec_qlqr.db"
sb="research/rsymmetry/NLO_xsec_qlqr.db"

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
        return  RectBivariateSpline(x0,y0,np.transpose(z0))

    def xsecs(self,msq,mgl):
        """xsec in pb"""
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
        print mo,xsec
        return interp1d(mo,xsec,kind="cubic")
                
def MSSMKfac(msq,mgl,process = ["gg","ss","sb","sg"]): 
    lo=0
    nlo=0
    for pro in process:
        nlloutput=runwrapper([NLL, pro,"nnpdf",str(msq),str(mgl)],NLLpath)  
        lo += float(nlloutput.split()[-9])
        nlo += float(nlloutput.split()[-8])
    return nlo,lo,nlo/lo

def MRSSMKfac(msq,mgl,process = ["gg","ss","sb","sg"]): 
    lo = 0
    tabs = [ "t3000", "t10000","t30000", "t100000","t1000" ]
    nlo = np.zeros((1,len(tabs)-1))
    ssgr = GridDB(ss,tabs)
    sbgr = GridDB(sb,tabs)
    for pro in process:
        if pro in ["gg","sg"]:
            nlloutput=runwrapper([NLL, pro,"nnpdf",str(msq),str(mgl)],NLLpath)  
            lo += float(nlloutput.split()[-9])
            nlo += float(nlloutput.split()[-8])
        elif pro == "ss":
            temp = ssgr.xsecs(msq,mgl)
            lo += temp[-1]
            nlo += temp[:-1]
        elif pro == "sb":
            temp = sbgr.xsecs(msq,mgl)
            lo += temp[-1]
            nlo += temp[:-1]
    return nlo.min(),lo,nlo/lo


if __name__ == "__main__":
    #print(points(db,".tables"))
    #print MSSMKfac(1100,500)
    print MRSSMKfac(1100,500)
    #test = GridDB(ss,[ "t1000","t3000", "t10000","t30000", "t100000" ])
    #print (test.interpolmo(500,500))(2000)
