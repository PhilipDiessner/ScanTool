import subprocess as sp
import numpy as np
import sys
import os

def pathtoSLHAlist(leshouchesdir):
    """
    returns the content of leshouchesdir as list using ls
    without subdirs
    """
    print leshouchesdir
    # lslist = sp.check_output(['./bin/listdir',leshouchesdir]).split()
    lslist = os.listdir(leshouchesdir)
    leshoucheslist = []
    i = 0
    for entry in lslist:
        i += 1
        if not os.path.isdir(leshouchesdir+entry):
            leshoucheslist.append(entry)
        if (i % 5000) == 0:
            print i
    return leshoucheslist

def autoflt(string):
    """
    doesn't return error when try to typecast to float and not having a number,
    returns original object if so
    """
    try:
        return float(string)
    except ValueError:
        return string

def autostr(var, precision=8):
    """Automatically numerical types to the right sort of string."""
    if type(var) is float or type(var) is np.float64:
        return ("%." + str(precision) + "E") % var
    return str(var)

def readcomargs():
    return sys.argv[1:]

def flatten(l, ltypes=(list, tuple, np.ndarray)):
    """flattens a list of ltypes"""
    ltype = type(l)
    l = list(l)
    i = 0
    while i < len(l):
        while isinstance(l[i], ltypes):
            if not l[i]:
                l.pop(i)
                i -= 1
                break
            else:
                l[i:i + 1] = l[i]
        i += 1
    return ltype(l)

def checksign(row, sign,var):
    if row[var]*sign>0:
        return True
    else:
        return False

def clearfolder(foldername):
    """
    finds all files in given dir and removes them
    """
    print "all files in directory " + foldername + " will be removed"
    # try: 
    #     map(os.remove, map( lambda x:foldername+x, os.listdir(foldername)))
    # except OSError:
#rewrite with subprocess
    list = sp.check_output(["ls", foldername])
    for filename in list.split():
        try:
            sp.check_call(["rm", foldername+filename])
        except sp.CalledProcessError:
            pass

def writedata(data,filepath,mode='a',depth=0):
    writeable = ''
    if depth==0:
        for number in map(autostr,data):
            writeable += number + '\t'
        writeable += '\n'
    elif depth==1:
        for line in data:
            for number in map(autostr,line):
                writeable += number + '\t'
            writeable += '\n'
    with open(filepath, mode) as f1:
        f1.write(writeable)

def linear_curve(x1,y1,x2,y2):
    dx = x2-x1
    dy = y2-y1
    if dx==0:
        a = 0
    else:
        a = dy/dx
    b = y2 - a*x2
    return a,b

def linear_y(x,a,b):
    return a*x+b

def linear_interpolate_two_points(x1,y1,x2,y2,x3):
    a,b = linear_curve(x1,y1,x2,y2)
    return linear_y(x3,a,b)

def linear_interpolate_two_points_one(x1,y1,x2,y2):
    return linear_interpolate_two_points(x1,y1,x2,y2,1)

def linear_polate_two_points(limit):
    def interpolation(x1,y1,x2,y2):
        return linear_interpolate_two_points(x1,y1,x2,y2,limit)
    return interpolation

def zprime_linear(lines,limit=1870):
    lam_arr = []
    vs_high = []
    vs_low = []
    z_high = []
    z_low =[]
    for line in lines:
        line = map(float,line.split())
        if line[0] not in lam_arr:
            lam_arr.append(line[0])
            vs_low.append(line[1])
            vs_high.append(line[1])
            z_low.append(line[2])
            z_high.append(line[2])    
        else:
            ind = lam_arr.index(line[0])
            if line[2]<z_low[ind]:
                z_low[ind] = line[2]
                vs_low[ind] = line[1]
            elif line[2]>z_high[ind]:
                z_high[ind]=line[2]
                vs_high[ind] = line[1]
    interfunc = linear_polate_two_points(limit)
    #print interfunc(100,1000,200,2000)
    vs_arr = np.array(map(interfunc, z_low,vs_low,z_high,vs_high))
    lamarr = np.array(lam_arr)
    index = lamarr.argsort()
    return map(lambda x,y: [x,y],lamarr[index],vs_arr[index])

def find_points_1(lines,limit=1,inde=6,overm12=False):
    print limit,inde
    m0_arr = []
    m12_low = []
    m12_high = []
    msq_low = []
    msq_high = []
    mglu_low = []
    mglu_high = []
    x_low = []
    x_high = []
    for line in lines:
        line = map(float,line.split())
        if overm12:
            m12 = line[1]
            m0 = line[0]
            line[0]=m12
            line[1]=m0
        if line[0] not in m0_arr:
            m0_arr.append(line[0])
            m12_low.append(line[1])
            m12_high.append(line[1])
            msq_low.append(line[4])
            msq_high.append(line[4])
            mglu_low.append(line[5])
            mglu_high.append(line[5])
            if line[inde]<limit:
                x_low.append(line[inde])
                x_high.append(100*limit)
            else:
                x_high.append(line[inde])    
                x_low.append(-100*limit)
        else:
            ind = m0_arr.index(line[0])
            if line[inde]<limit and line[inde]>x_low[ind]:
                x_low[ind] = line[inde]
                m12_low[ind] = line[1]
                msq_low[ind] = line[4]
                mglu_low[ind] = line[5]
            elif line[inde]>limit and line[inde]<x_high[ind]:
                x_high[ind]=line[inde]
                m12_high[ind] = line[1]
                msq_high[ind] = line[4]
                mglu_high[ind] = line[5]
    interpol=linear_polate_two_points(limit)
    m12_arr = np.array(map(interpol,x_low,m12_low, x_high,m12_high))
    msq_arr = np.array(map(interpol,x_low,msq_low, x_high,msq_high))
    mglu_arr = np.array(map(interpol,x_low,mglu_low, x_high,mglu_high))
    m0arr = np.array(m0_arr)
    index = m0arr.argsort()
    return map(lambda x,y,a,b: [x,y,a,b], m0arr[index], 
               m12_arr[index], msq_arr[index], mglu_arr[index])

def find_points_2(lines):
    return None

def get_contour_line(infile,outfile,lim=1,indi=6,overm12=False):
    filen = open(infile)
    lines = filen.readlines()
    filen.close()
    print outfile
    writedata(find_points_1(lines,limit=lim,inde=indi,overm12=overm12), 
              outfile, mode='w',depth=1)


if __name__ == "__main__":
    # infile = "/home/diessner/raid1/MSSM/plot-MSSMoff-7TeV-5fb-0l-exp.txt"
    infile = "/home/diessner/zihfast/mssm/NLL-plotable.txt"
    outfile = "/home/diessner/zihfast/mssm/MSSMexclline-0l-NLL.txt"
    get_contour_line(infile, outfile,overm12=False)
    # path ="/home/diessner/raid1/test/"
    # for infile in pathtoSLHAlist(path):
    #     if infile[-3:] == "awk":
    #         print infile[-15:-12]
    #         if infile[-15:-12] == "cls":
    #             print infile
    #             bound=0.05  
    #         else:
    #             bound=2.7
    #         get_contour_line(path+infile, path+infile[:-3]+"line", lim = bound,indi=8)
    # filen = open("/home/diessner/Documents/talks/DPG2013/zprimemasscan.txt")
    # lines = filen.readlines()
    # filen.close()
    # array=  zprime_linear(lines,1870)
    # writedata(array, "/home/diessner/Documents/talks/DPG2013/zprimelimit.txt", mode='w',depth=1)
