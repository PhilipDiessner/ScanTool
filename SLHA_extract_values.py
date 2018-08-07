#! /usr/bin/python

import numpy as np
import os.path as osp
from functools import total_ordering
import argparse

def pathtoSLHAlist(leshouchesdir):
    """
    returns the content of leshouchesdir as list using ls
    without subdirs
    """
    print leshouchesdir
    lslist = sp.check_output(['./bin/listdir',leshouchesdir]).split()
    # lslist = os.listdir(leshouchesdir)
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

def writedata(data,filepath,mode='a',depth=0):
    writeable = ''
    if depth == 0:
        for number in map(autostr,data):
            writeable += number + '\t'
        writeable += '\n'
    elif depth == 1:
        for line in data:
            for number in map(autostr,line):
                writeable += number + '\t'
            writeable += '\n'
    with open(filepath, mode) as f1:
        f1.write(writeable)

def autostr(var, precision=8):
    """Automatically numerical types to the right sort of string."""
    if type(var) is float: # or type(var) is np.float64:
        return ("%." + str(precision) + "E") % var
    return str(var)

class Line(object):
    """
    Class for a Line in a SLHA block, containing id's, value and comment
    ids is tuple of ints, value is float, comment is string
    Method to write Line to string
    Access to line only through Block object
    """
    def __init__(self,ident,val,comment=None):
        try:
            self.ids = tuple(ident)
        except TypeError:
            self.ids = int(ident),
        self.val = val
        if comment:
            self.com=comment
        else:
            self.com=''

    def write(self):
        string = " "
        for i in self.ids:
            string += str(i) + "  "
        string += autostr(self.val) + "  # "+ self.com + "\n"
        return string

    
class DecayLine(Line):
    """
    Class for a Decay block line, needs a different write
    """
    def write(self):
        string = autostr(self.val) 
        for i in self.ids:
            string += "  " + str(i)
        string +=   "  # "+ self.com + "\n"
        return string
 
@total_ordering
class Block(object):
    """
    Object representation of a BLOCK elements.  Blocks
    have a name, may have an associated Q value, and collection of Lines
    totalordering that decay blocks come last
    """
    # sets typ of block 2 for matrix
    # 1 for parameters
    # 0 for mass
    def __init__(self, name,idshape, q=None):
        self.name = name.upper()
        self.lines = []
        self.q = q
        self.idshape=idshape

    def __eq__(self, other):
        return ((not isinstance(self,Decay) and not isinstance(other,Decay))
                or (isinstance(self,Decay) and isinstance(other,Decay)))

    def __gt__(self, other):
        return (isinstance(self,Decay) and not isinstance(other,Decay))
        
    def reshape_id(self,ids):
        try:
            ident = tuple(ids)
        except TypeError:
            ident = int(ids),
        if len(ident) != self.idshape:
            raise Exception("Entry shape does not match Block shape")
        return ident
           
    def sorting(self):
        """
        Sort Lines by id's
        """
        self.lines=sorted(self.lines,key=lambda x: x.ids)
        
    def write_Block(self):
        """
        Return a SLHA Block as a string
        """
        if self.lines == []:
            return ''
        else:
            self.sorting()
            out = ""
            namestr = self.name
            if self.q is not None:
                namestr += " Q= " + autostr(self.q)
            out += "BLOCK %s\n" % namestr
            
            for s in self.lines:
                out += s.write() 
        return out

    def add_entry(self, ident,value,comment=None):
        """
        adds entry to self.lines in needed form
        checking that it hasn't been there before
        """
        ids=self.reshape_id(ident)
        if ids in [l.ids for l in self.lines]:
            raise Exception("Entry already exists, use update_entry instead")
        else:
            self.lines.append(Line(ids,value,comment))

    def update_entry(self, ident,value,comment=None):
        """
        Checks if entry exists in lines, if so updates value, else creates new one
        """
        ids=self.reshape_id(ident)
        inds=[l.ids for l in self.lines]
        if ids in inds:
            i=inds.index(ids)
            (self.lines[i]).val=value
            if comment:
              (self.lines[i]).comment=comment  
        else:
            #print ids,"Entry not found, adding it"
            self.lines.append(Line(ids,value,comment))
        
    def text_entry(self,text):
        """
        convert line of SLHA file
        """
        line = text.split("#")
        values = line[0].split()
        comment = line[1]
        result = float(values[-1])
        ids = [int(x) for x in values[:-1]]
        if not self.idshape:
            self.idshape = len(ids)
            self.update_entry(ids,result,comment)
        elif self.idshape == len(ids):
            self.update_entry(ids,result,comment)
        else:
            print text, " in wrong shape for "+self.name
    

    def get_entry(self, ident):
        """
        returns value if ids matches in lines
        does not check for block name 
        """
        ids=self.reshape_id(ident)
        inds = [x.ids for x in self.lines]
        if ids in inds:
            i=inds.index(ids)
            return (self.lines[i]).val
        else:
            print ids,"Entry not found in block ", self.name
            return None

        
class Decay(Block):
    """
    Class for a decay block
    needs two and three body entries at some point
    For this ids and sorting need to be adapted
    name is particle pid as string
    Q is Width as float
    """
    def write_Block(self):
        """
        Return a Decay Block as a string
        """
        out = ""
        namestr = self.name + " " + autostr(self.q)
        out += "DECAY %s\n" % namestr
            
        if self.lines != []:
            self.sorting()
            for s in self.lines:
                out += s.write() 
        return out
    
        
class SLHA(object):
    """
    SLHA file containing Blocks and Comment Header
    """

    def __init__(self,filename=None,slhastr=None):
        self.header = ''
        self.blocks = []
        if filename and slhastr:
            raise Exception("Can not init from file and string input")
        elif filename:
            self.filetoSLHA(filename)
        elif slhastr:
            self.strtoSLHA(slhastr)

    def strtoSLHA(self,slhastr):
        """
        takes the str of complete slha file
        """
        isheader = True
        ismeta = False
        isdecay = False
        #if self.blocks:
        #    print "would override exisiting slha blocks, passing"
        #    return
        strlist = "\n".split(slhastr)
        for line in strlist:
            linespl=line.split()
            if linespl==[]: # empty line
                continue
            elif '#' in linespl[0]: # comment
                if isheader:
                    self.header += line
                else:
                    continue
            elif linespl[0].upper()=='BLOCK':
                isdecay=False
                isheader=False
                if linespl[1].upper() in ["SPINFO"]:
                    ismeta = True
                    continue
                else:
                    ismeta = False
                if len(linespl)> 3 and linespl[2] == 'Q=':
                    block = Block(linespl[1],None, float(linespl[3]))
                else:
                    block = Block(linespl[1],None)
                self.blocks.append(block)
            elif linespl[0].upper()=='DECAY':
                isheader=False
                block = Decay(linespl[1],(2,3),float(linespl[2]))
                self.blocks.append(block)
                isdecay=True
            else:
                if isdecay or ismeta:
                    # BRs not implemented
                    continue
                else:
                    # block holds last generated block
                    block.text_entry(line[:-1]) # rm newline
        #print [[line.val for line in block.lines] for block in self.blocks]

    def filetoSLHA(self,filename):
        """read in SLHA textfile to fill"""
        with open(filename) as f:
            lines = f.read()
        strtoSLHA(lines)
                    
    def tofile(self,filename):
        """
        write to textfile
        """
        text = self.header
        self.sortblocks()
        for block in self.blocks:
            text += block.write_Block()
        with open(filename,"w") as f:
            f.write(text)

    def sortblocks(self):
        self.blocks=sorted(self.blocks)

    def getvalue(self,param):
        """
        param as [own name, Block,[inds]]
        Extracts value of param
        """
        name = param[1].upper()
        inds = [int(x) for x in param[2]]
        value = None
        for block in self.blocks:
            if name == block.name:
                value = block.get_entry(inds)
                return value
        if value is None:
            print param, " not found with getvalue"

    def setvalue(self,param,val):
        """
        Not implemented
        """
        raise Exception("slha.setvalue Not implemented")

    
def getvalues(filename, variables):
    """
    Finds value of variables out of SLHA file if Block name and entry 
    identifiers are given as second and third
    element of variable
    getvalues form [name,BLOCK,[ind]]
    returns list of the values
    """
    slha = SLHA(filename=filename)
    values = map(slha.getvalue,variables)
    return values

def flavor_order(slhafile,newslhafile=None,toRSSM=False):
    """
    Given a slha file produced by sarah it replaces it by a file where the sfermion mixing is
    not mass but flavor ordered
    """
    if not newslhafile:
        newslhafile=slhafile # overwrite
    slha = SLHA(filename=slhafile)
    blocks=slha.blocks
    flavnames = ["DSQMIX","USQMIX","SELMIX"]
    rssmflavnames = [["DLSQMIX","DRSQMIX"],["ULSQMIX","URSQMIX"],["SRELMIX","SLELMIX"]]
    flavblocks = filter(lambda x: x.name in flavnames,blocks)
    massblock = filter(lambda x: x.name in ["MASS"],blocks)[0]

    usq = [1000002,1000004,1000006,2000002,2000004,2000006]
    dsq = [1000001,1000003,1000005,2000001,2000003,2000005]
    lep = [1000011,1000013,1000015,2000011,2000013,2000015]
    otherblocks = filter(lambda x: x.name not in flavnames+["MASS"],blocks)

    udec = filter(lambda x: x.name in map(str,usq),otherblocks)
    ddec = filter(lambda x: x.name in map(str,dsq),otherblocks)
    ldec = filter(lambda x: x.name in map(str,lep),otherblocks)
    otherblocks = filter(lambda x: x.name not in map(str,usq+dsq+lep),otherblocks)
    
    usqval = [ massblock.get_entry(sq) for sq in usq]
    dsqval = [ massblock.get_entry(sq) for sq in dsq]
    lepval = [ massblock.get_entry(sq) for sq in lep]
    
    flavs = [dsq,usq,lep]
    flavsval = [dsqval,usqval,lepval]
    flavsdec = [ddec,udec,ldec]
    for i,block in enumerate(flavblocks):
        flav = flavs[i][:]
        flavval = flavsval[i][:]
        decval = flavsdec[i][:]
        #decays
        widths = []
        for sq in flav:
            for x in decval:
                if x.name == str(sq):
                   widths.append(x.q) 
        widths = [x.q for sq in flav for x in decval if x.name == str(sq) ]
        #find reordering
        matrix=np.zeros((6,6))
        for line in block.lines:
            (a,b),c = line.ids, line.val
            matrix[a-1][b-1]=c
        maxpos = np.argmax(abs(matrix),axis=1)
        repl = [0]*6
        for k,l in enumerate(maxpos):
            repl[l]=k
        #mass and decay reordering
        flavval = [flavval[k] for k in repl]
        widths = [widths[k] for k in repl]
        for dec in decval:
            for k,sq in enumerate(flav):
                if str(sq)==dec.name:
                    dec.q = widths[k]
        #updating to existing blocks
        for line in block.lines:
            a,b = line.ids
            line.val = (matrix[repl,:])[a-1][b-1]
        if toRSSM:
            for j,name in enumerate(rssmflavnames[i]):
                newblock=Block(name,2, q=block.q)
                slha.blocks.append(newblock)
                for a in range(3):
                    for b in range(3):
                        newblock.add_entry((a+1,b+1),(matrix[repl,:])[3*j+a][3*j+b])
                        
        [massblock.update_entry( sq,flavval[k]) for k,sq in enumerate(flav)]
    if toRSSM:
        newblock=Block("imdrsqmix",2, q=block.q)
        slha.blocks.append(newblock)
        for a in range(3):
            for b in range(3):
                newblock.add_entry((a,b),0)
            
    slha.tofile(newslhafile)
    
def get_sq_gl_masses(slhafile,pathtoslha):
    var = [['mg','MASS',['1000021']],
           ['mu1','MASS',['1000002']],
           ['md1','MASS',['1000001']],
           ['ms1','MASS',['1000003']],
           ['mc1','MASS',['1000004']],
           ['mu2','MASS',['2000002']],
           ['md2','MASS',['2000001']],
           ['ms2','MASS',['2000003']],
           ['mc2','MASS',['2000004']]# ,
#            ['mb1','MASS',['1000005']],
#            ['mb2','MASS',['2000005']]
           ]
    path=osp.join(pathtoslha,slhafile)
    data = getvalues(path,var)
    if None not in data:
        data = map(float,getvalues(path,var))
        msq = reduce(lambda x,y: x+y, data[1:])/float(len(var)-1)
    else:
        msq=None
    return autostr(msq), autostr(data[0])


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Flavour order sfermions in a SLHA file')
    parser.add_argument('infile',  type=str)
    parser.add_argument('-outfile',default=None)
    parser.add_argument('-splitMRSSM',  type=int,default=0,
                        help='Are the sfermions left-right-split in the MRSSM, if True diagonal mixing 3x3 blocks are added')
    
    args = vars(parser.parse_args())
    flavor_order(args["infile"],args["outfile"],toRSSM=args["splitMRSSM"])
