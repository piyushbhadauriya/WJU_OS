import numpy as np
import diskpy

class NodeBitMap:
    FREE = 0
    USED = 1
    BAD = 99
    size = 48
    def __init__(self, blockNbr=None,size=None):
        if blockNbr == None or size == None:
            self.blockNbr = 2
            self.disk = diskpy.mydisk()
            self.arraysize = self.disk.blocksize
            self.init()
            self.saveToDisk()
        else:
            self.disk = diskpy.mydisk()
            self.blockNbr = blockNbr # 2
            self.size = size
            self.arraysize = self.disk.blocksize #512
            self.nodebitmap = np.zeros(shape=(self.arraysize,1), dtype='int8')

            self.nodebitmap[0] = self.BAD # bad 1
            self.nodebitmap[1] = self.USED
            self.nodebitmap[2:self.size] = self.FREE # free 47
            self.nodebitmap[self.size:512]= self.BAD # total 48  
            self.saveToDisk()
    
    def init(self):
        self.disk.disk_open()
        bitmap = self.disk.disk_read(self.blockNbr)
        self.nodebitmap = np.frombuffer(bitmap,dtype='int8')
        self.disk.disk_close()
        return self

    def setFree(self, atOffset):
        self.nodebitmap.setflags(write=1)
        self.nodebitmap[atOffset] = self.FREE
        self.saveToDisk()

    def setUsed(self, atOffset):
        self.nodebitmap.setflags(write=1)
        self.nodebitmap[atOffset] = self.USED
        self.saveToDisk()

    def findFree(self):
        self.init()
        for i in range(0,self.size):
            if self.nodebitmap[i] == self.FREE:
                self.setUsed(i)
                return i
        raise Exception('No free space')

    def saveToDisk(self):
        self.disk.disk_open()
        self.disk.disk_write(self.blockNbr,self.nodebitmap.tobytes(),0)
        self.disk.disk_close()

    def scan(self):
        free = 0
        used = 0
        bad = 0
        self.disk.disk_open()
        bitmap = self.disk.disk_read(self.blockNbr)
        self.disk.disk_close()
        self.nodebitmap = np.frombuffer(bitmap,dtype='int8')
        for i in range(0,self.size):
            if self.nodebitmap[i] == self.FREE:
                free += 1
            elif self.nodebitmap[i] == self.USED:
                used += 1
            else :
                bad += 1
        print('Free : ',free)
        print('Used : ',used)
        print('Bad  : ',bad)
