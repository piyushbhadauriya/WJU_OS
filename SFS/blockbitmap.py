import numpy as np
import diskpy
class BlockBitMap():
    def __init__(self, arraysize, blockNbr):
        self.blockNbr = blockNbr # 1
        self.arraysize= arraysize #512
        self.blockbitmap = np.zeros(shape=(arraysize,1), dtype='int8')
        self.disk = diskpy.mydisk()
    
    # "Initialize the array with FREE and BAD "
    def init(self):
        self.blockbitmap[:2] = 1 # used superblock and blockmap
        self.blockbitmap[2:64] = 0 # free
        self.blockbitmap[64:512]= 99 # bad
        self.saveToDisk()

    def setFree(self, atOffset):
        self.blockbitmap = 0

    def setUsed(self, atOffset):
        self.blockbitmap = 1

    def findFree(self):
        for i in range(0,64):
            if self.blockbitmap[i] == 0:
                return i
        raise Exception('No free space')

    def saveToDisk(self):
        self.disk.disk_open()
        self.disk.disk_write(self.blockNbr,self.blockbitmap.tobytes(),0)
        self.disk.disk_close()