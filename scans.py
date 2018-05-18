import MRSSMBMP as mrf

def scan2Dinit():
    points = []
    mbdrc = range(100,2001,100)
    mwdrc = range(100,2001,100)
    muu = range(100,1501,100)
    mud = range(100,1501,100)
    mru2 = [x*x for x in range(500,2001,100)]
    mrd2 = [x*x for x in range(500,2001,100)]
    lamtd = [float(x)/10. for x in xrange(-20,21,2)]
    lamtu = [float(x)/10. for x in xrange(-20,21,2)]
    lamsd = [float(x)/10. for x in xrange(-20,21,2)]
    lamsu = [float(x)/10. for x in xrange(-20,21,2)]
    tanb = [2,3,6]+range(10,51,5)
    #ms2 = [x*x for x in range(0,120,5)]
    #bmu = [x*x for x in range(100,1600,50)]
    me2 = [x*x for x in range(500,1501,100)]
    me332 = [x*x for x in range(500,1501,100)]
    ml332 = [x*x for x in range(500,1501,100)]
    #mq2 = [x*x for x in range(1000,2600,100)]
    inds= [0,1,2,3,4,5,6,11,16,17,18,19,21,22]
    mrssm_value_arrays = [tanb,lamsd,lamsu,lamtd,lamtu,mud,muu,ml332,me2,me332,mru2,mrd2,mbdrc,mwdrc]
    #inds= [1,21]
    #mrssm_value_arrays = [lamsd,mbdrc]
    print reduce(lambda x,y: x+y, [len(z) for z in mrssm_value_arrays])
    for bm in mrf.BM1,mrf.BM2,mrf.BM3:
        point = bm()
        for x in range(len(mrssm_value_arrays)-1):
            for y in range(x+1,len(mrssm_value_arrays)):
                points.extend(scan_2D(point,mrssm_value_arrays[x],
                                      mrssm_value_arrays[y],inds[x],inds[y]))
    print len(points)
    return points
    
def scan_init():
    #point = mrf.BM6()
    points = []
    for point in ( mrf.BM4,):
        points.append(point()[:])
                  # mrf.BM4(),mrf.BM5(),mrf.BM6(),
                  # mrf.BM7(),mrf.BM8(),mrf.BM9() 
        # for x in range(50,300,10)+range(300,1001,50): # mslep
        for x in range(100,350,50)+range(350,851,75):
            for y in range(100,350,50)+range(350,851,75):
                pointtmp = point()[:]
                # pointtmp[5] = x
                # pointtmp[6] = x
                #pointtmp[21] = 0
                # pointtmp[22] = y
                #pointtmp[23] = 5000
                pointtmp[6] = x
                pointtmp[5] = y
                # pointtmp[14] = y*y
                
                points.append(pointtmp)
                    
            # massind  = [21,22,23]
            # mass2ind = range(7,21)
            # mass2ind2= range(24,26)
            # for ind in massind:
            #     pointtmp[ind] = msusy/2
            # for ind in mass2ind:
            #     pointtmp[ind] = msusy*msusy
            # for ind in mass2ind2:
            #     pointtmp[ind] = 2*msusy*msusy
            #points.append(pointtmp)
    print len(points)
    return points

#mixing
        #         m2=x*x
        #         s= np.sqrt(y)
        #         m1=1500*1500
        #         try:
        #             a,b,c = eigensystemtomatrix(m1,m2,s)
        #         except Exception:
        #             continue
        #         #if x>y:
        #         #    continue
        #     #keep mud,muu
        # #          #if y<=x:
        #         pointtmp = point()[:]
        #         # pointtmp[5] = x
        #         # pointtmp[6] = x
        #         pointtmp[21] = 0
        #         # pointtmp[22] = y
        #         pointtmp[23] = 5000
        #         pointtmp[8] = a
        #         pointtmp[9] = b
        #         pointtmp[12] = a
        #         pointtmp[13] = b
        #         pointtmp[14] = a
        #         pointtmp[15] = b
        #         mixing = [0]*9
        #         mixing[1]=c
        #         mixing[4]=c
        #         mixing[7]=c
        #         secondgen=[m1]*3
        #         print a,b,c
        #         points.append(pointtmp+mixing+secondgen)
        
def scan2l_init():
    points = []
    params = [1,2,4]
    ranges=[[float(x)/10. for x in xrange(-20,21,1)],
            [float(x)/10. for x in xrange(-20,21,1)],
            [float(x)/10. for x in xrange(-20,21,1)]]
    for point in [BM1(),BM2(),BM3(),BM4()]:
        print len(points)
        for i in xrange(len(params)):
            for value in ranges[i]:
                pointtmp = point[:]
                pointtmp[params[i]] = value
                points.append(pointtmp)
    return points

def scan_2D(point,ar1,ar2,ind1,ind2):
    out = []
    temp=point[:]
    for i in ar1:
        temp[ind1]=i
        for j in ar2:
            temp[ind2]=j
            out.append(temp[:])
    return out
    
def adapt_sleptons(val,value,param):
    comb1 = param[0]-val[0]**2
    return [comb1+value[0]]
    # comb1 = [param[0]-val[0]**2, param[1]-val[1]**2]
    # comb2 = [param[0]-val[1]**2, param[1]-val[0]**2]
    # print comb1, comb2
    # goal = value[:2]#((val[-2]+val[-1])/2.)**2
    # if abs(comb1[0])+abs(comb1[1]) < abs(comb2[0])+abs(comb2[1]):
    #     return [comb1[0]+goal[0]**2,comb1[1]+goal[1]**2]
    # else:
    #     return [comb2[0]+goal[0]**2,comb2[1]+goal[1]**2]

def slepton_mass(i,scandir):
    # fit1 = adaptive_scan([["me332","EXTPAR",["17"]],["me2","EXTPAR",["16"]]],
    #                      [["se1","MASS",["1000011"]],["se3","MASS",["1000015"]]],
    #                      [100,100], adapt_sleptons,
    #                          Init.changemultiparameter,
    #                   mrf.SPheno_MRSSM)
    fit1 = adaptive_scan([["me332","EXTPAR",["17"]]],
                         [["se1","MASS",["1000011"]]],
                         [10000], adapt_sleptons,
                             Init.changemultiparameter,
                      mrf.SPheno_MRSSM)
    fit1(i, scandir)
    
def eigensystemtomatrix(ew1,ew2,sint):
    """ Returns elements a,b,x of matrix ((a,x),(x,b) 
    with eigenvalues ew1,ew2 and sine of mixing angle sint.
    Assuming mixing angle between 0 and Pi/2, setting x>0
    Not able to deal with equal eigenvalues"""
    if abs(ew1-ew2)/float(ew1)<0.0001:
        raise Exception("Can't deal with equal eigenvalues")
    cost = np.sqrt(1-sint*sint)
    x = abs((ew1-ew2))*cost*sint
    if (ew1>ew2 and sint<1/np.sqrt(2)) or (ew1<ew2 and sint>1/np.sqrt(2)):
        a = 0.5*(ew1+ew2)+np.sqrt(0.25*(ew1+ew2)**2-ew1*ew2-x*x)
    else:
        a = 0.5*(ew1+ew2)-np.sqrt(0.25*(ew1+ew2)**2-ew1*ew2-x*x)
    b = ew1+ew2-a
    return a,b,x    

scanfunc = scan_init
