import multiprocessing as mp


try:
    import dill
except:
    pass
else:
    dillin = True
    def run_dill_encoded(what):
        fun, args = dill.loads(what)
        return fun(*args)
        
    def apply_async(pool, fun, args):
        return pool.apply_async(run_dill_encoded, (dill.dumps((fun, args)),))

def fun(a):
    def inner(b):
        return a+b
    return inner

def test(a):
    outer = fun(a)
    def inner(b):
        print b
        return outer(b)
    return inner

def wrapper(b):
    a = 2
    outer = fun(a)
    return outer(b)

test2= test(2)
ncore = mp.cpu_count()-1
print ncore
pool = mp.Pool(ncore) # ,maxtasksperchild=10)
#print pool.map(fun(2),range(15))
jobs = []
for i in range(15):
    jobs.append(apply_async(pool,fun(2),(i,)))
pool.close()
pool.join()
for job in jobs:
    print job.get()
