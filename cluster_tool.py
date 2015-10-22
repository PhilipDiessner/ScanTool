import subprocess as spr
import sys
import os.path as osp
import os

def runMG(binpath,paramcard):
    try:
        out = spr.call([binpath, paramcard],stderr=spr.STDOUT)
    except spr.CalledProcessError:
        print "MGrun: s.t. wrong for " + paramcard
        return "Error"

if len(sys.argv) != 3:
    print wrong number of args
    raise RuntimeError

j = sys.argv[1]
k = sys.argv[2]
for i in xrange(1,int(k)+1):
    if (i % 10) == int(j):
        runMG(osp.join("odd" + j, bin, madevent), osp.join("forwojtek","MGrun_" + i))
        os.rename(osp.join("odd"+j, "Events", i, "unweighted_events.lhe.gz"),
                  osp.join("forphilip", i + ".lhe.gz"))
