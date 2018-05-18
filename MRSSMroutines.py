from functools import partial
import Init
from Run import run_base, run_on_dir
import MRSSMfunctions as mrf

def run_mg():
    runfunc = run_on_dir(scanpath)
    method = Init.get_allpointids(outdb, "points")
    runfunc(mrf.mg_run,method=method,parallel=False)
    
def run_cm():
    runfunc = run_on_dir(scanpath)
    method = Init.get_allpointids(outdb, "points")
    runfunc(mrf.cm_run,method=method,parallel=False)
    
masses_write = partial(run_base, mrf.write_masses)
zhmix_write = partial(run_base, mrf.zhmix)
par_write = partial(run_base, mrf.write_derived_par)
sulmix_write = partial(run_base, mrf.write_sulmix)
dm_write =  partial(run_base, mrf.write_omega)
hbhs_write =  partial(run_base, mrf.HBHS_write_wrapper)
lhc_write = partial(run_base, mrf.lhc_out)


spheno_run = partial(run_base, mrf.SPheno_MRSSM)
hbhs_run = partial(run_base, (mrf.hbhs_uncertain_file,
                              mrf.HB_MRSSM,mrf.HS_MRSSM,
                             ))  
lhc_run = partial(run_base, mrf.lhc_study)
cm_rerun = partial(run_base, mrf.rerun_CM) # (mrf.lhc_study,
dm_run = partial(run_base, mrf.run_dm)

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
dm_twodm_table = partial(Init.table_init, 'relic', zip(['omega','omega1','omega2'],
                                                 ['real','real','real']))
par_table = partial(Init.table_init, 'derivedpar', zip(mrf.derivedpar, ['real']*len(mrf.derivedpar)))
sul_table = partial(Init.table_init, 'sulmix', zip(mrf.sulpar, ['real']*len(mrf.sulpar)))
