import sqlite3
import itertools as it
import os
import os.path as osp
import numpy as np
import copy

###
# Rewrite to use one function to handle all sql stuff,
# pass string with one command, do it in far future
###
def ident_to_path(i):
    """break up identifier so there are only 10 files per dir"""
    return osp.join(*[x for x in str(i)])

def command_in_db(db,command,many=False):
    conn = sqlite3.connect(db)
    c = conn.cursor()
    if many:
        c.executescript(command)
    else:
        c.execute(command)
    conn.commit()
    conn.close()

def points(infile, command):
    result_db = osp.expanduser(infile)
    conn = sqlite3.connect(result_db)
    c = conn.cursor()
    c.arraysize = 100
    out = []
    if type(command) in [list, tuple]:
        c.executescript('; '.join(command)+';')
    else:
        c.execute(command )
    for i in c:
        out.append(i)
    conn.close()
    return out
    
def make_table(db,table,parameters):
    """
    parameters is list of lists that contain first  names second sqlite type
    """
    title ="(identifier int, "
    for par in parameters[:-1]:
        title += par[0] + " "+ par[1] + ", "
    title += parameters[-1][0] + " " + parameters[-1][1] + " )"
    print title
    command = '''CREATE TABLE '''+ table +' '+title
    command_in_db(db, command)

def create_index(db,table,param,index):
    command = 'CREATE INDEX ' + index + ' ON '+ table +  ' ( ' + \
              ', '.join(param) + ')'
    command_in_db(db, command)

def table_init( table, param, db):           
    make_table(db, table, param)
    create_index(db, table, ['identifier'] , table+'index')
    
def register_point(scan_db, table, point):
    lenpar=len(point)
    conn = sqlite3.connect(scan_db)
    c = conn.cursor()
    c.execute('INSERT INTO ' + table + ' VALUES (' + 
              ', '.join(['?' for _ in point])+')', point)
#     c.execute('''MERGE INTO tablename USING table_reference ON (condition) 
# WHEN MATCHED THEN
# WHEN NOT MATCHED THEN
# INSERT (column1 [, column2 ...]) VALUES (value1 [, value2 ...''')
    conn.commit()
    conn.close()

def register_points(scan_db, table, points):
    lenpar=len(points[0]) 
    conn = sqlite3.connect(scan_db)
    c = conn.cursor()
    c.executemany('INSERT INTO ' + table + ' ' + 'VALUES (' + 
                  ', '.join(['?' for _ in points[0]]) + ')', points)
    conn.commit()
    conn.close()

def make_db(scan_db, parameters, table, pointlst):
    print scan_db
    make_table(scan_db,table,parameters)
    if pointlst:
        register_points(scan_db, table,pointlst)

def get_pointid(scan_db, table, point,params):
    scan_db = osp.expanduser(scan_db)
    if len(point) == len(params):
        conn = sqlite3.connect(scan_db)
        c = conn.cursor()
        getting_point= ""
        for i in xrange(len(point)-1):
            getting_point += params[i] + " = " + str(point[i]) + " and "
        getting_point += params[-1] + " = " + str(point[-1])
        c.execute('SELECT identifier FROM ' + table + ' ' + 
                  'WHERE ' + getting_point)    
        out = c.fetchone()
        conn.close()
        return out
    else:
        print point, "does not match", params
        return None

def get_allpointids(scan_db,table,crit=''):
    scan_db = osp.expanduser(scan_db)
    conn = sqlite3.connect(scan_db)
    c = conn.cursor()
    getting_point= ""
    c.execute('SELECT identifier FROM ' + table+crit) 
    out =[]
    for line in c:
        out.append(line[0])
    conn.close()
    print len(out)
    return out

def add_point_to_scan(point, scanpath, createSLHAin,switches):
    tofile = createSLHAin(point[1:],switches)
    # print scanpath, ident_to_path(point[0])
    pointpath = osp.join(scanpath, ident_to_path(point[0]))
    try:
        os.makedirs(pointpath)
    except OSError:
        pass
    with open(osp.join(pointpath,str(point[0]) + ".SLHA.in"), 'w') as f:
        f.write(tofile) # model specific

def init_struc(points, path, parameters, switches, createSLHAin, dbpath, 
               makedb=True):
    scanpath = osp.expanduser(path)
    dbpath = osp.expanduser(dbpath)
    try:
        os.makedirs(scanpath)
    except OSError:
        pass
    fullpointgenerator = [(type(a[1]))([a[0]]) + a[1] for a in 
                          it.izip(it.count(1), points)]
    for point in fullpointgenerator:
        add_point_to_scan(point, scanpath, createSLHAin,switches)
    if makedb:
        print 'starting on db'
        outdb = osp.join(dbpath,osp.basename(scanpath) +".db")
        make_db(outdb, parameters, "points", fullpointgenerator)
        create_index(outdb, 'points', ['identifier'] , 'pointsindex')


def new_slha_file(createSLHAin,switches):
    def create(point,scanpath):
        tofile = createSLHAin(point[1:],switches)
        pointpath = osp.join(scanpath, str(point[0]))
        with open(osp.join(pointpath,str(point[0]) + ".SLHA.in"), 'w') as f:
            f.write(tofile) # model specific

def changeSLHA(filename,changing,par,newval):
    with open(filename, 'r') as f:
        oldfile = f.readlines()
    tofile = ''.join(changing(par,newval,oldfile))
    with open(filename, 'w') as f:
        f.write(tofile)

def changeoneparameter(param,newpar,oldfile):
    """ oldfile is from readlines()"""
    rightblock = False
    switch = False
    out = []
    for line in oldfile:
        sline = line.split()
        if rightblock and sline[:len(param[2])] == param[2]:
            if switch:
                out.append(' '.join(param[2]+["{0:d}".format(newpar)] + 
                                    sline[len(param[2])+1:])+'\n' )
            else:
                out.append(' '.join(param[2]+["{0:E}".format(newpar)] + 
                                    sline[-2:])+'\n' )
            rightblock = False
        else:
            out.append(line)
        if sline[0].upper() == "BLOCK" and sline[1] == param[1]:
            rightblock = True
            if sline[1] in ['SPhenoInput','MODSEL']:
                switch = True
        elif sline[0].upper() == "BLOCK" and sline[1] != param[1]:
            rightblock = False
    return out

def changemultiparameter(param,newpar,oldfile):
    """
    SLHA input file is short so no problem with time 
    for parsing using several iterations
    """
    for i in range(len(param)):
        oldfile = changeoneparameter(param[i],newpar[i],oldfile)
    return oldfile

def changeSLHAwrapper(changing,par,newval):
    def fun(i,scandir):
        changeSLHA(osp.join(scandir,ident_to_path(i),i+".SLHA.in"),changing,par,newval)
    return fun

