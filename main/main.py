import os
import sys
sys.path.insert(1,os.path.join(sys.path[0],".."))
print(sys.path) 

from memory import test1 

test1.printString("call from main")