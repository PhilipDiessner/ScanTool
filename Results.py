import os.path as osp

def readfile(filename):
    with open(filename) as f:
        result = f.readlines()
    return [result[-3].split()]+[result[-1].split()]

def readHB(i,scandir):
    out =  readfile(osp.join(scandir,i,"HiggsBounds_results.dat"))
    return out[-1][-4:-1]
    
def readHS(i,scandir):
    out = readfile(osp.join(scandir,i,"HiggsSignals_results.dat"))
    return out[-1][-7:]
