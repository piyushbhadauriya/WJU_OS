import numpy as np
from memory.memmgr import MemMgr 

class ProcessX:
    pid_counter = 111
    pid_increment = 111
    invalid_pageframe = -1
    pageFrame_column = 0

    def __init__(self,initialNbrOfPages):
        self.logPhyMgt = np.zeros(shape=(initialNbrOfPages,1),dtype ='int64')
        self.tablevector = []
        for r in range (0,initialNbrOfPages):
            self.logPhyMgt[r,self.pageFrame_column] = self.invalid_pageframe
            self.tablevector.append([None])
        
        self.mypid = self.get_pid()

    def get_pid(self):
        aa = ProcessX.pid_counter
        ProcessX.pid_counter += ProcessX.pid_increment
        return aa
    
    def get_mypid(self):
        return self.mypid   
    
    def setx(self,page,pageframe,vectora):
        self.logPhyMgt[page] = pageframe
        self.tablevector[page] = vectora
        
            

    def load_pages(self,listofpages):
        sizel = len(listofpages)
        listPageFrameVector = MemMgr.get_mem(self.mypid,sizel)
        if (listPageFrameVector == [None] or listPageFrameVector == []):
            print("failed to find free memory")
        else :
            sizel = len(listofpages)
            for ii in range(0,sizel):
                pageframe,vectora = listPageFrameVector[ii]
                self.setx(listofpages[ii],pageframe,vectora)
    
    def get_vectors(self):
        res = []
        for r in range(0,len(self.tablevector)):
            if self.tablevector[r][0] != None:
                res.append(self.tablevector[r])

        return res


    def display_PMT(self):
        print ('----------Process Mgmt --------')
        for r in range(len(self.tablevector)):
            print(str(r)+' : '+str(self.logPhyMgt[r])+"  "+str(self.tablevector[r]))
        print('--------------------------------')

