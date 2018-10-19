"""
Options taken from HEPpaths
"""
import datetime
import time
import os.path as osp
import MRSSMroutines as mrr 
from MRSSMfunctions import createSLHAinMRSSM
import Init
from Run import adaptive_scan
from HEPpaths import scanname,scandir1,scandir2,dbdir,\
    switches,parameter,para_types,scanfunc,parallel,ncores,\
    init,spheno,lhc,dm,hbhs,runonly,writeonly

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
    if init and not writeonly:
        scan(scanpath,makedb=True)
    if not writeonly:
        if spheno:
            mrr.spheno_run(scanpath, outdb, parallel=parallel,ncores=ncores)
        if lhc:
            print "LHC run"
            mrr.lhc_run(scanpath,outdb, parallel=parallel,ncores=ncores)
        if dm:
            mrr.dm_run(scanpath, outdb,parallel=parallel,ncores=ncores)
        if hbhs:
            # not actually implemented yet again
            mrr.hbhs_run(scanpath, outdb, parallel=parallel,ncores=ncores)
    # first run everything, than write as e.g. lhc_run might change SPheno.spc
    if not runonly:
        if spheno:
            mrr.mass_table(outdb)
            mrr.masses_write(scanpath, outdb)
            mrr.par_table(outdb)
            mrr.par_write(scanpath, outdb)
        if lhc:
            mrr.sul_table(outdb)
            mrr.sulmix_write(scanpath, outdb)
            mrr.lhc_table(outdb)
            mrr.lhc_write(scanpath,outdb)
        if dm:
            mrr.dm_table(outdb)
            mrr.dm_write(scanpath, outdb)
        if hbhs:
            mrr.zhmix_table(outdb)
            mrr.zhmix_write(scanpath, outdb)    
            mrr.hbhs_table(outdb)
            mrr.hbhs_write(scanpath, outdb)
            
    end = time.time()
    diff = end - start
    print datetime.timedelta(seconds=diff)
    m, s = divmod(diff, 60)
    h, m = divmod(m, 60)
    print "%d:%02d:%02d" % (h, m, s)
