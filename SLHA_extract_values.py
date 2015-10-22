import numpy as np

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

def autostr(var, precision=8):
    """Automatically numerical types to the right sort of string."""
    if type(var) is float or type(var) is np.float64:
        return ("%." + str(precision) + "E") % var
    return str(var)

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
    Opens file infilename and returns content
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
    Opens file infilename 
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

if __name__ == "__main__":
    # infile = "/home/diessner/raid1/MSSM/plot-MSSMoff-7TeV-5fb-0l-exp.txt"
    infile = "/home/diessner/raid2/SPheno-3.2.4/SPheno.spc.MRSSM" # "/path/to/LesHouches/File"
    variables = [['LSD','HMIX',['301']],
                 ['mh','MASS',['25']]
                 #['mt','MASS',['1000006']],
                 #['mcha2','MASS',['1000037']]
                 ]
    out = getvalues(infile, variables)
    for i in range(len(variables)):
        print variables[i][0],out[i]
