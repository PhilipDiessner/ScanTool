"""
TODO: argparser to select options!!!!
"""
import datetime
import time
import os.path as osp
import numpy as np
from functools import partial
import MRSSMroutines as mrr 
from MRSSMfunctions import createSLHAinMRSSM
import Init
from Run import adaptive_scan
from HEPpaths import scanname,scandir1,scandir2,dbdir,\
    switches,parameter,para_types,scanfunc

outdb = osp.join(dbdir,scanname+".db")
newscanpath = (osp.join(scandir1,scanname), osp.join(scandir2,scanname))
scanpath = newscanpath[0]

print outdb

def scan(scanpath,makedb=True):
    points = scanfunc()
    if type(scanpath) in (list,tuple):
        Init.init_struc(points, scanpath[0], zip(parameter, para_types), 
                        switches, createSLHAinMRSSM, dbdir,makedb=makedb)
        
        Init.init_struc(points, scanpath[1], zip(parameter, para_types), 
                        switches, createSLHAinMRSSM, dbdir,makedb=False)     
    else:
        Init.init_struc(points, scanpath, zip(parameter, para_types), 
                        switches, createSLHAinMRSSM, dbdir,makedb=makedb)


if __name__ == "__main__":
    start = time.time()
    #method=[2]
    #scan(scanpath,makedb=True)
    ## TODO: argparser to select options!!!!
    #mrr.spheno_run(scanpath, outdb, parallel=True,ncores=35)
    # mrr.hbhs_run(scanpath, outdb, parallel=True,ncores=20)
    # slepton_run(scanpath,outdb,parallel=False)
    mrr.lhc_run(scanpath,outdb, parallel=True,ncores=38)
    # mrr.dm_run(scanpath, outdb,parallel=True,ncores=15)


    #mrr.mass_table(outdb)
    #mrr.sul_table(outdb)
    # #mrr.par_table(outdb)
    # # mrr.zhmix_table(outdb)
    #mrr.masses_write(scanpath, outdb)
    #mrr.sulmix_write(scanpath, outdb)
    # #mrr.par_write(scanpath, outdb)
    # # mrr.zhmix_write(scanpath, outdb)
    
    # #mrr.hbhs_table(outdb)
    # #mrr.hbhs_write(scanpath, outdb)
    
    #mrr.lhc_table(outdb)
    #mrr.lhc_write(scanpath,outdb)
    
    # mrr.dm_table(outdb)
    # mrr.dm_write(scanpath, outdb)

    end = time.time()
    diff = end - start
    print datetime.timedelta(seconds=diff)
    m, s = divmod(diff, 60)
    h, m = divmod(m, 60)
    print "%d:%02d:%02d" % (h, m, s)
