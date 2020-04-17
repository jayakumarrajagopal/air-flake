import string
from time import gmtime, strftime
import sys 
s = string.printable #"some string object"
max_possible_line_size = 20000

def read_bulk( sourcefile, stoponerror=False, bulksize=10000) :
    lines = 0
    currline = 0
    oklines = []
    errorlines = []
    with open(sourcefile) as F :
        for line in F:
            currline +=1
            if len(line) > max_possible_line_size : 
                print (currline,": Line too long in :",sourcefile)
                raise Exception("LineToolong")
            err = False
            for c in line:
                if c not in string.printable:
                    err = True
                    errorlines.append([currline,line,str.find(line,c),ord(c)])
                    if stoponerror :
                        print (currline,": Wrong Char[",ord(c),"] at :", str.find(line,c))
                        raise Exception('InvalidChar')
            if not err :   
                # oklines.append(line)
                lines +=1
                
            if lines == bulksize :
                yield oklines,errorlines
                oklines = []
                errorlines = []   
                lines = 0  
        # file ended.. check buffer has more lines
        if lines > 0 :
            yield  oklines, errorlines  
        #if stoponerror == True or bulksize <=0 :
        #   return oklines

filename = None # data filename
if len( sys.argv) == 1 :
    # just test run the program with program file as datafile
    filename = sys.argv[0]
    for lines in read_bulk(filename,True,10):
        for line in (lines[0]) :
            print (line, end='')
        print ("Processed 10 line Fecth from ", filename)
else :
    filename = sys.argv[1]
    n=0
    for linesarray in read_bulk(filename,True,100):
        n +=1
        outfile = "{}_{}".format(filename,n)
        if len(linesarray[0]) > 0 :
          with open(outfile , 'w') as f:
            for line in linesarray[0]:
               f.write("%s" % line)
               #print (line,end='')
        if len(linesarray[1]) > 0 :
            # error lines present...
            outfile = "{}_{}".format(filename+"__err",n)
            with open(outfile , 'w') as f:
               for line in linesarray[1]:
                   f.write("%s" % line)
            
        print ("{} *********** wrote : {}".format(strftime("%Y-%m-%d %H:%M:%S", gmtime()), outfile))
