import numpy as np
import diskpy

class NodeBitMap():
    def __init__(self, blockNbr):
        self.disk = diskpy.mydisk()
        self.blockNbr = blockNbr # 2
        self.arraysize = self.disk.blocksize #512
        self.nodebitmap = np.zeros(shape=(self.arraysize,1), dtype='int8')

        self.nodebitmap[0] = 99 # bad 1 
        self.nodebitmap[1:48] = 0 # free 47
        self.nodebitmap[48:512]= 99 # total 48  
        self.saveToDisk()
    
    def init(self):
        self.disk.disk_open()
        bitmap = self.disk.disk_read(self.blockNbr)
        self.nodebitmap = np.frombuffer(bitmap,dtype='int8')
        self.disk.disk_close()

    def setFree(self, atOffset):
        self.nodebitmap[atOffset] = 0
        self.saveToDisk()

    def setUsed(self, atOffset):
        self.nodebitmap[atOffset] = 1
        self.saveToDisk()

    def findFree(self):
        self.init()
        for i in range(0,48):
            if self.nodebitmap[i] == 0:
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
        for i in range(0,48):
            if self.nodebitmap[i] == 0:
                free += 1
            elif self.nodebitmap[i] == 1:
                used += 1
            else :
                bad += 1
        print('Free : ',free)
        print('Used : ',used)
        print('Bad  : ',bad)

    