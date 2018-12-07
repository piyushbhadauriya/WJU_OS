import numpy as np
import diskpy
class BlockBitMap:
    FREE = 0
    USED = 1
    BAD = 99
    size = 64

    def __init__(self, blockNbr=None,size=None):
        if blockNbr == None or size == None:
            self.blockNbr = 1
            self.disk = diskpy.mydisk()
            self.size = self.disk.nbrOfBlocks
            self.arraysize = self.disk.blocksize
            self.init()
            self.saveToDisk()
        else:
            self.disk = diskpy.mydisk()
            self.blockNbr = blockNbr # 1
            self.size = size
            self.arraysize= self.disk.blocksize #512
            self.blockbitmap = np.zeros(shape=(self.arraysize,1), dtype='int8')
            
            self.blockbitmap[:6] = self.USED # Used (reserved) for superblock and blockmap, inodemap, 3 inodes
            self.blockbitmap[6:self.size] = self.FREE # total 64 blocks
            self.blockbitmap[self.size:512]= self.BAD # set unusable blocks to bad  
            self.saveToDisk()
    
    def init(self):
        self.disk.disk_open()
        bitmap = self.disk.disk_read(self.blockNbr)
        self.blockbitmap = np.frombuffer(bitmap,dtype='int8')
        self.disk.disk_close()
        

    def setFree(self, atOffset):
        self.blockbitmap.setflags(write=1)
        self.blockbitmap[atOffset:] = self.FREE
        self.saveToDisk()

    def setUsed(self, atOffset):
        self.blockbitmap.setflags(write=1)
        self.blockbitmap[atOffset] = self.USED
        self.saveToDisk()

    def findFree(self):
        self.init()
        for i in range(0,self.size):
            if self.blockbitmap[i] == self.FREE:
                self.setUsed(i)
                return i
        raise Exception('No free space')
        

    def saveToDisk(self):
        self.disk.disk_open()
        self.disk.disk_write(self.blockNbr,self.blockbitmap.tobytes(),0)
        self.disk.disk_close()

    def scan(self):
        free = 0
        used = 0
        bad = 0
        self.disk.disk_open()
        bitmap = self.disk.disk_read(self.blockNbr)
        self.disk.disk_close()
        self.blockbitmap = np.frombuffer(bitmap,dtype='int8')
        for i in range(0,self.size):
            if self.blockbitmap[i] == self.FREE:
                free += 1
            elif self.blockbitmap[i] == self.USED:
                used += 1
            else :
                bad += 1
        print('Free : ',free)
        print('Used : ',used)
        print('Bad  : ',bad)

    