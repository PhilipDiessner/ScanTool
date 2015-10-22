from helper_functions import autostr,pathtoSLHAlist,writedata
import numpy as np

class Block(object):
    """
    Object representation of a BLOCK elements read from the Peters output.  Blocks
    have a name, may have an associated Q value, and then a collection of data
    entries
    """
    # sets typ of block 2 for matrix
    # 1 for parameters
    # 0 for mass
    def __init__(self, name, q=None):
        self.name = name.upper()
        self.entries = []
        self.q = q
        self.nbrofctrl=None

    def write_Block(self):
        """\
        Return a SLHA Block as a string, from the supplied block object.
        """
        if self.entries == []:
            return ''
        else:
            out = ""
            namestr = self.name
            if self.q is not None:
                namestr += " Q= " + autostr(self.q)
            out += "Block %s\n" % namestr
            for s in sorted(self.entries):
                out += s + "\n"
        #out += "\n"
        return out

    def add_entry(self, entry):
        """
        adds entry to self.entries in needed form
        """
        str_entry = ""
        dbl = "  "
        sep = "   "
        if len(entry) < 2:
            raise Exception("Block entries must be at least a 2-tuple")
        # entry = map(autostr, entry)
        # if self.name == 'ALPHA':
        #     str_entry +=
        if entry[1] < 0:
        # cosmetical if-else-clause to reduce length of white space if there is a minus sign
        # proably not needed
            if entry[0] == 'MASS':
                #entry = ino_masssign(entry)
                str_entry += sep + entry[-1][0] + dbl + dbl + autostr(entry[1]) \
                + "   # " + entry[2]
            elif entry[0] == 'ALPHA':
                #entry = ino_masssign(entry)
                str_entry += sep +autostr(entry[1])+ "   # " + entry[2]
            elif self.nbrofctrl == 2:
                str_entry += dbl  + entry[-1][0] + dbl + entry[-1][1] + dbl \
                +autostr(entry[1])+ "   # " + entry[2]
            else:
                str_entry += sep + dbl + entry[-1][0] + dbl + dbl + autostr(entry[1]) \
                + "   # " + entry[2]
        else:
            if entry[0] == 'MASS':
                #entry = ino_masssign(entry)
                str_entry += sep  + entry[-1][0] + dbl + sep \
                +autostr(entry[1])+ "   # " + entry[2]
            elif entry[0] == 'ALPHA':
                #entry = ino_masssign(entry)
                str_entry += sep +autostr(entry[1])+ "   # " + entry[2]
            elif self.nbrofctrl == 2:
                str_entry += dbl  + entry[-1][0] + dbl + entry[-1][1] + sep \
                +autostr(entry[1])+ "   # " + entry[2]
            else:
                str_entry += sep + dbl + entry[-1][0] + sep + dbl + autostr(entry[1]) \
                + "   # " + entry[2]
        self.entries += [str_entry]
        
def SLHAtoblocks(infilename):
    """
    returns a list of the block objects out of a SLHA text file
    """
    out, blocknames = readInputSLHA(infilename)
    blocklist = []
    # out = filter(lambda x: x.[0]=='#' or x.[0][0]=='#' ,out)
    # blockheaders = filter(lambda x: x[0]=='Block' or x[0]=='BLOCK' ,out)
    content=[]
    file_in = open(infilename)
    for line in file_in:
        if line[0] == '#':
            continue
        elif line[:5].upper()=='BLOCK':
            splitline = line.split()
            if blocklist != []:
                blocklist[-1].entries = content
            if len(splitline)> 3 and splitline[2] == 'Q=':
                block = Block(splitline[1], float(splitline[3]))
            else:
                block = Block(splitline[1])
            content=[]
            blocklist.append(block)
        else:
             content.append(line)
    blocklist[-1].entries = content
    file_in.close()
    return blocklist
                      
def readInput(infilename):
    """
    Opens file infilename and returns outfile
    """
    out = []
    file_in = open(infilename)
    for line in file_in:
        splitline = line.split()
        out += [splitline]
    file_in.close()
    return out

def readInputSLHA(infilename):
    """
    Opens file infilename and returns outfile
    out contains  blockcontent
    """
    out = []
    header = []
    content=[]
    with  open(infilename) as file_in:
        for line in file_in:
            if line[0] == '#':
                continue
            elif line[:5]=='Block' or line[:5]=='BLOCK':
                splitline = line.split()
                if header != []:
                    out.append(content)
                content=[]
                header.append(splitline)
            else:
                content.append(line)
        out.append(content)
    return out, header

def getvalue(var,blocks):
    dim = len(var[2])
    value = None
    for block in blocks:
        if var[1].upper() == block.name.upper():
            for line in block.entries:
                splitline = line.split()
                if splitline[:dim] == var[2]:
                    value = splitline[dim]
    if value is None:
        print var, " not found with getvalue"
    else:
        return value
    
    
def getvalues(filename, variables):
    """
    Finds value of variables out of SLHA file if Block name and entry 
    identifiers are given as second and third
    element of variable
    returns list of the values
    """
    blocks = SLHAtoblocks(filename)
    values = map(lambda x: getvalue(x,blocks),variables)
    return values


def SLHA_to_txt(leshfiles, outfile,variables):
    values = []
    for infile in leshfiles:
        value = getvalues(infile,variables)
        if not None in value:
            values.append(value)
        #print infile
    writedata(values,outfile, 'w', 1)

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
    data = getvalues(pathtoslha+slhafile,var)
    if None not in data:
        data = map(float,getvalues(pathtoslha+slhafile,var))
        msq = reduce(lambda x,y: x+y, data[1:])/float(len(var)-1)
    else:
        msq=None
    return autostr(msq), autostr(data[0])

def addhiggsmassestoexclusionfiles(infilename,slhafiles,outfilename):
    infile = open(infilename) # 14.05.12.15.37 06.06.12.17.10
    inlines = infile.readlines()
    infile.close()
    var = [['lam3','EXTPAR',['10']],
           ['lam12','EXTPAR',['11']],
           ['kap','EXTPAR',['13']],
           ['vS','EXTPAR',['16']],
           ['sol','EXTPAR',['17']],
           ['tanbeta','EXTPAR',['25']],
           ['mh','MASS',['0000025']],
           ['chi1','MASS',['1000022']],
           ['stop1','MASS',['1000006']],
           ['mueff','HMIX',['1']]]
    values=[]
    for spectrum in slhafiles:
        values.append(map(lambda x: autostr(float(x)),getvalues(spectrum,var)))
    newlines = []
    for line in inlines:
        line = line.split()
        for value in values:
           if [round(float(x),3) for x in line[:6]] == [round(float(x),3) for x in value[:6]]:
               newline = line#[:33]
               #newline.append(max(line[-11:]))
               newline.extend(value[6:])
               newlines.append(newline)
               break
    writeable = ""
    for line in newlines:
        for entry in line:
            writeable += entry + '\t'
        writeable += '\n'
    infile = open(outfilename, 'a') # 14.05.12.15.37 06.06.12.17.10
    infile.write(writeable)
    infile.close() 
   
if __name__ == "__main__":
    path1 = "/home/diessner/raid1/e6smalllam/SLHA/"
    path2 = "/home/diessner/raid2/CMSSMscan/"
    paths = ["/home/diessner/raid1/e6smalllam/SLHA/","/home/diessner/raid2/newE6/SLHA/","/home/diessner/raid2/fullce6/SLHA/","/home/diessner/raid2/cE6/SLHA/", 
             "/home/diessner/raid1/newsmallce6/SLHA/"]
    infile = "/home/diessner/research/whk/cesix_lhc_limit_obs_allpoints.txt"
    #infiles =  map(lambda x: path1+x,pathtoSLHAlist(path1))
    infiles = []
    for path in paths:
        infiles.extend(map(lambda x: path+x,pathtoSLHAlist(path)))
    outfilename = "/home/diessner/research/whk/cesix-exclusion_masses.txt"
    variables = [['m0','MINPAR',['1']],
                 ['m12','MINPAR',['2']],
                 ['A0','MINPAR',['5']],
                 ['tanbeta','EXTPAR',['25']],
                 ['mh','MASS',['25']]
                 #['mt','MASS',['1000006']],
                 #['mcha2','MASS',['1000037']]
                 ]
    # for slha in infiles:
    #     mglu,msq=get_sq_gl_masses(slha,"")
    #     data = getvalues(slha,variables)
    #     data.append(msq)
    #     data.append(mglu)
    #     if None not in data:
    #         writedata(data,outfilename, 'a', 0)
    addhiggsmassestoexclusionfiles(infile,infiles,outfilename)
    # SLHA_to_txt(infiles, outfilename,variables)
