import re

fi = "/home/diessner/raid2/MRSSMscans/lhc_bmtest/3/lhc.out"

# strings

nbarcb = '.*N[1-4]barCB[1-2]'
nbarca = '.*N[1-4]barCA[1-2]'
ncabar = '.*N[1-4]CA[1-2]bar'
ncbbar = '.*N[1-4]CB[1-2]bar'
cbbarcb = '.*CB[1-2]barCB[1-2]'
cabarca = '.*CA[1-2]barCA[1-2]'
nnbar =  '.*N[1-4]N[1-4]bar'
llbar = '.*se[1-2]se[1-2]c'
ttbar = '.*se3se3c'
strarr= [nnbar,ncabar,ncbbar,nbarca,nbarcb,cabarca,cbbarcb,llbar,ttbar]
# patterns
patternarr = [re.compile(a) for a in strarr]
xsec = [0]*len(patternarr)
with open(fi) as f:
    for line in f.readlines():
        line=line.split()
        try:
            if line[0][0:2]== "ME" and line[-1]!='0':
                process = line[0] #.split('bar2')[1]
                
                test = re.split('\)|\(', line[-1])
                zahl = float(test[0]+test[-1])
                ind = [p.match(process) for p in patternarr]
                for i, k in enumerate(ind):
                    if k:
                        xsec[i]+=zahl
                
        except IndexError:
            continue

print strarr
print xsec
print "total: ",reduce(lambda x,y: x+y,xsec)
