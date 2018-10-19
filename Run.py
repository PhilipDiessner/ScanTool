import itertools as it
import os
import os.path as osp
import multiprocessing as mp
import subprocess as spr 
import Init
import SLHA_extract_values as SLHA
from functools import partial

class KeyboardInterruptError(Exception): pass
##
# test and delete unnecessary stuff
##
# try:
#     import dill
# except:
#     pass
# else:
#     dillin = True
#     def run_dill_encoded(what):
#         fun, args = dill.loads(what)
#         return fun(*args)
        
#     def apply_async(pool, fun, args):
#         return pool.apply_async(run_dill_encoded, (dill.dumps((fun, args)),))

def run_on_dir(scandir, db=None):
    """
    wrapper to produce function that will run a function on directories in scandir
    with the a possible conntected sqlite3 database db
    note that the function generated runs the functions with two arguments
    i from the method listing and scandir from the generating function
    and a possible third argument db, given as keyword, if the database should be forwarded
    this also decides if function will be possibly run in parallel or not
    """
    join = osp.join
    exists = osp.exists
    if type(scandir) in (tuple, list):
        scandir = map(lambda x: osp.realpath(osp.expanduser(x)), scandir)
    else:
        scandir = osp.realpath(osp.expanduser(scandir))
    print scandir
    def run_fun(fun,
               method=it.count(1), parallel=True, ncores=0):
        try:
            len(method)
            finite=True
        except TypeError:
            finite= False
        if parallel:
            if ncores == 0:
                ncore = mp.cpu_count()-1
            else:
                ncore = ncores
            pool = mp.Pool(ncore) # ,maxtasksperchild=10)
            
        for i in method:
            try:
                fun(i, scandir,db=db)
                # enforce non parallel running for IO on same db
            except TypeError: # if db is actually not needed
                if parallel:
                    # if dillin:
                    #     apply_async(pool, fun, (i,scandir,))
                    # else:
                    try:
                        pool.apply_async(fun,(i,scandir,)) #.get(9999999)
                    except KeyboardInterrupt:
                        print 'got ^C while pool mapping, terminating the pool'
                        pool.terminate()
                    except Exception, e:
                        print 'got exception: %r, terminating the pool' % (e,)
                        pool.terminate()
                else:
                    fun(i, scandir)
            except OSError:
                if finite:
                    print 'done'
                    pass
                else:
                    print 'parallel breaking'
                    break
        if parallel:
            pool.close()
            pool.join()
    return run_fun

def partial_runwrapper(toexecute,i,scandir):
    i = str(i)
    cwd = osp.join(scandir,Init.ident_to_path(i))
    execute = ['nice','-n','10'] + [x.format(i,scandir) for x in toexecute]
    print i
    try:
        out = spr.check_output(execute,
                               stderr=spr.STDOUT, cwd=cwd)
        return out
    except spr.CalledProcessError as E:
        print "run: s.t. wrong for " + i
        raise E
    except KeyboardInterrupt:
        raise KeyboardInterruptError()
        
def runwrapper(toexecute,cwd):
    """
    executes toexecute with niceness
    """
    execute = ['nice','-n','10'] + list(toexecute)
    #print execute, cwd
    
    try:
        out = spr.check_output(execute,
                               stderr=spr.STDOUT, cwd=cwd)
        return out
    except spr.CalledProcessError as E:
        print "run: s.t. wrong for " + ' '.join(toexecute)
        raise E
    except KeyboardInterrupt:
        raise KeyboardInterruptError()

def SPheno_run(sphenodir,model,input_SLHA,out_spectrum):
    """
    wrapper generating SPheno fun returning stdout
    """
    execut = "bin/SPheno"+model
    #print input_SLHA
    return partial(partial_runwrapper,[osp.join(sphenodir, execut), 
                                input_SLHA, out_spectrum])

def Flex_run(sphenodir,model,input_SLHA,out_spectrum):
    """
    wrapper generating FlexSusuy fun
    SPhenodir - path to SPheno
    model - model name of SARAH model
    input_SLHA - full path to input spectrum
    out_spectrum full path to output spectrum
    """
    execut = osp.join(sphenodir,"models",model+"/run_"+model+".x")
    return partial(partial_runwrapper,[execut, "--slha-input-file="+input_SLHA, 
                                       "--slha-output-file="+out_spectrum])

def HB_run(hbdir, neutralhiggs, chargedhiggs, name):
    """
    wrapper generating Higgsbounds fun
    """
    execut = osp.join(hbdir,"HiggsBounds")
    return partial(partial_runwrapper,
                   [execut, "LandH", "effC", str(neutralhiggs), 
                    str(chargedhiggs), name])

def HS_run(hbdir, neutralhiggs, chargedhiggs, name):
    """
    wrapper generating Higgssignals fun
    """
    execut = osp.join(hbdir,"HiggsSignals")
    return partial(partial_runwrapper,
                   [execut, "latestresults", "peak", "2",  "effC", 
                    str(neutralhiggs), str(chargedhiggs), name])
   
def readfile(filename):
    """
    base func of reading hb and hs file
    """
    with open(filename) as f:
        result = f.readlines()
    return [result[-3].split()]+[result[-1].split()]

def read_HB(i,scandir):
    """
    produces need hb output
    """
    out =  readfile(osp.join(scandir,Init.ident_to_path(i),"HiggsBounds_results.dat"))
    return out[-1][-4:-1]
    
def read_HS(i,scandir):
    """
    produces needed hs output
    """
    out = readfile(osp.join(scandir,Init.ident_to_path(i),"HiggsSignals_results.dat"))
    return out[-1][-7:]

def read_hbhs(i,scandir):
    """
    combining the above producing the output to write to db
    """
    try:
        hbout = read_HB(i,scandir)
        hsout = read_HS(i,scandir)
    except IOError:
        pass
    else: 
        return hbout+hsout
 
def read_param(param,spec_file,i,scandir):
    """
    specialized SLHA read functions from scan path naming 
    """
    i = str(i)
    filename = osp.join(scandir,Init.ident_to_path(i),spec_file)
    return SLHA.getvalues(filename, param)

def write_wrapper(read_func,table,i,scandir,db):
    """
    higher order functions for all writing
    """
    try:
        out = read_func(i,scandir)
        # point = [i]+readHB(i,scandir)+readHS(i,scandir)
        print i
    except IOError:
        pass
    
    else:
        try:
            point = [int(i)]+out
            Init.register_point(db, table, point)
        except:
            pass

def write_more_wrapper(read_func,table,i,scandir,db):
    """
    higher order functions for all writing, expects a list of several
    entries for one parameter point
    """
    try:
        out = read_func(i,scandir)
        print i
    except IOError:
        print "IOError for" + i
        pass
    else:
        for part in out:
            point = [int(i)]+list(part)
            Init.register_point(db, table, point)
        
def adaptive_scan(param, outpar, value,func,createSLHAin,
                  sphenofunc, eps=0.01,model="MRSSM"):
    """
    vary param using func to get outpar closer to value
    assume that correct init SLHA exists
    param and outpar in getvalues form [name,BLOCK,[ind]]
    """

    def measure(val, value):
        test = []
        for i in range(len(val)):
            test.append((val[i]-value[i])/value[i])
        return test

    def fun(i, scanpath):
        j = 0
        lim = 3
        i = str(i)
        filename = osp.join(scanpath,Init.ident_to_path(i),"SPheno.spc."+model)
        sphenofunc(i,scanpath) 
        for m,val in enumerate(value):
            if type(val) in (list, tuple):
                result = SLHA.getvalues(filename, [val])
                value[m] = float(result[0])
                # interpret as SLHA line and return wanted value
        while j < lim:
            j+=1  
            try: 
                val = [float(x) for x in SLHA.getvalues(filename, outpar)]
                paramval = [float(x) for x in SLHA.getvalues(filename, param)]
           ## check if spectrum was created,
               
            except OSError as e:
                break
            print val, paramval
            if all([abs(x) < eps for x in measure(val,value)]):
                break
            else:
                os.remove(filename)
                newpar = func(val,value,paramval)
                pointpath = osp.join(scanpath, Init.ident_to_path(i))
                Init.changeSLHA(osp.join(pointpath,i + ".SLHA.in"),
                                createSLHAin,param,newpar)
                sphenofunc(i,scanpath)
    return fun

#def replace_line_in_file(oldline,newline, infile):
#    with open(infile, 'r') as input_file, open(infile+".tmp", 'w') as output_file:
#        for line in input_file:
#            if line.strip() == oldline:
#                output_file.write(newline+'\n')
#            else:
#                output_file.write(line)
#    os.rename(infile+".tmp",infile)

def touch(fname, times=None):
    fhandle = open(fname, 'a')
    try:
        os.utime(fname, times)
    finally:
        fhandle.close()

        

def run_base(running_func, scanpath, db, parallel=True,method=None,ncores=20):
    runfunc = run_on_dir(scanpath, db=db)
    if not method:
        method = Init.get_allpointids(db, "points")
    if type(running_func) in (tuple, list):
        for func in running_func:
            try:
                runfunc(func, method=method, parallel=parallel, ncores=ncores)
            except Exception as err:
                #print "trouble with "+ func.__name__ + " for "+ db
                print err
                pass
    else:
        try:
            runfunc(running_func, method=method, parallel=parallel, ncores=ncores)
        except Exception as err:
            #print "trouble with "+ running_func.__name__+ " for "+ db
            print err
            pass
            
