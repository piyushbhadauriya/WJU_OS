import numpy as np
import diskpy
class BlockBitMap():
    def __init__(self, blockNbr):
        self.disk = diskpy.mydisk()
        self.blockNbr = blockNbr # 1
        self.arraysize= self.disk.blocksize #512
        self.blockbitmap = np.zeros(shape=(self.arraysize,1), dtype='int8')
        
        self.blockbitmap[:6] = 1 # Used (reserved) for superblock and blockmap, inodemap, 3 inodes
        self.blockbitmap[6:64] = 0 # total 64 blocks
        self.blockbitmap[64:512]= 99 # set unusable blocks to bad  
        self.saveToDisk()
    
    def init(self):
        self.disk.disk_open()
        bitmap = self.disk.disk_read(self.blockNbr)
        self.blockbitmap = np.frombuffer(bitmap,dtype='int8')
        self.disk.disk_close()

    def setFree(self, atOffset):
        self.blockbitmap[atOffset] = 0
        self.saveToDisk()

    def setUsed(self, atOffset):
        self.blockbitmap[atOffset] = 1
        self.saveToDisk()

    def findFree(self):
        self.init()
        for i in range(0,64):
            if self.blockbitmap[i] == 0:
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
        for i in range(0,64):
            if self.blockbitmap[i] == 0:
                free += 1
            elif self.blockbitmap[i] == 1:
                used += 1
            else :
                bad += 1
        print('Free : ',free)
        print('Used : ',used)
        print('Bad  : ',bad)

    