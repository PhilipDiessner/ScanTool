from functools import partial
import Init
import Run
import MRSSMfunctions as mrf

def run_mg():
    runfunc = Run.run_on_dir(scanpath)
    method = Init.get_allpointids(outdb, "points")
    runfunc(mrf.mg_run,method=method,parallel=False)
    
def run_cm():
    runfunc = Run.run_on_dir(scanpath)
    method = Init.get_allpointids(outdb, "points")
    runfunc(mrf.cm_run,method=method,parallel=False)    

def run_base(running_func, scanpath, db, parallel=True,method=None):
    runfunc = Run.run_on_dir(scanpath, db=db)
    if not method:
        method = Init.get_allpointids(db, "points")
    if type(running_func) in (tuple, list):
        for func in running_func:
            runfunc(func, method=method, parallel=parallel, ncores=12)
    else:
        runfunc(running_func, method=method, parallel=parallel, ncores=12)

spheno_run = partial(run_base, mrf.SPheno_MRSSM)
masses_write = partial(run_base, mrf.write_masses)
zhmix_write = partial(run_base, mrf.zhmix)
hbhs_run = partial(run_base, (mrf.hbhs_uncertain_file,
                              mrf.HB_MRSSM,mrf.HS_MRSSM,mrf.HBHS_write_wrapper,
                             ))  
lhc_run = partial(run_base, mrf.lhc_study) # (mrf.lhc_study,
dm_run = partial(run_base, (mrf.run_dm, mrf.write_omega,))
lhc_write = partial(run_base, mrf.lhc_out)
mass_table = partial(Init.table_init, 'masses', zip(mrf.masspar, ['real']*len(mrf.masspar)))
zhmix_table = partial(Init.table_init, 'hmix', zip(mrf.hmixpar,['real']*len(mrf.hmixpar)))
hbhs_table = partial(Init.table_init, 'hbhs',
                     zip(['hbexcl','hbchan','hbrate','hscsqmu','hscsqmh',
                          'hscsqtot','hsnmu','hsnmh','hsntot','p'],
                         ['real']*10))
lhc_table = partial(Init.table_init, 'lhc', zip(['analysis','r','cl'],
                                                ['text','real','real']))
dm_table = partial(Init.table_init, 'relic', zip(['omega','pval','loglike'],
                                                 ['real','real','real']))
