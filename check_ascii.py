import string
from time import gmtime, strftime
import sys 

def check_for_non_ascii(sourcefile,bulksize=10000):
    lines = 0
    with open(sourcefile) as F :
        for line in F:
            lines +=1
            for c in line:
                if c not in string.printable:
                    raise Exception("Invalid Char " + str(ord(c)) + "present in "+ str( line ) )
            if lines % bulksize == 0 :
                yield lines 
    yield lines

for lineno in ( check_for_non_ascii (sys.argv[1], 1000) ):
    print ("{} processed {} lines".format(strftime("%Y-%m-%d %H:%M:%S", gmtime()), lineno) )
print ("No issue found in ", sys.argv[1])