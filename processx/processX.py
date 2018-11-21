import numpy as np
from memory.memmgr import MemMgr
from memory.memmgmt import MemMgmt
import threading

class ProcessX:
    pid_counter = 111
    pid_increment = 111
    invalid_pageframe = -1
    pageFrame_column = 0
    # lock access to pidcounter when a process instace calls init_pid
    # avoid two process with the same pid
    pid_counter_lock = threading.Lock()
    
    def __init__(self,initialNbrOfPages):
        #lock down the procees table to avoid 2 thread access it at the same time.
        self.thread_lock = threading.Lock()
        self.mapPageToPFrame = np.zeros(shape=(initialNbrOfPages,1),dtype ='int64')
        self.tableVector = []
        self.mypid = self.init_pid()
        for r in range (0,initialNbrOfPages):
            self.mapPageToPFrame[r,self.pageFrame_column] = self.invalid_pageframe
            self.tableVector.append([None])
        
        MemMgmt.register(self) 
    
    @classmethod
    def init_pid(cls):
        cls.pid_counter_lock.acquire()
        aa = ProcessX.pid_counter
        ProcessX.pid_counter += ProcessX.pid_increment
        cls.pid_counter_lock.release()
        return aa
    
    def get_mypid(self):
        return self.mypid   
    
    def set_frame(self,page,pageframe,vectora):
        self.thread_lock.acquire()
        self.mapPageToPFrame[page] = pageframe
        self.tableVector[page] = vectora
        self.thread_lock.release()

        
    def release_frame(self, pageframe):
        for r in range (len(self.mapPageToPFrame)):
            
            if (self.mapPageToPFrame[r,0] == pageframe):
                self.thread_lock.acquire()
                self.mapPageToPFrame[r,0] = self.invalid_pageframe
                self.tableVector[r] = [None]
                self.thread_lock.release()
                break

    def load_pages(self,listofpages):
        sizel = len(listofpages)
        listPageFrameVector = MemMgr.get_mem(self.mypid,sizel)
        if (listPageFrameVector == [None] or listPageFrameVector == []):
            print("failed to find free memory")
        else :
            sizel = len(listofpages)
            for ii in range(0,sizel):
                pageframe,vectora = listPageFrameVector[ii]
                self.set_frame(listofpages[ii],pageframe,vectora)
    
    def get_vectors(self):
        res = [] 
        for r in range(0,len(self.tableVector)):
            if self.tableVector[r][0] != None:
                res.append(self.tableVector[r])
        return res


    def display_ProcessMgT(self):
        print ('----------Process Mgmt --------')
        for r in range(len(self.tableVector)):
            print(str(r)+' : '+str(self.mapPageToPFrame[r])+"  "+str(self.tableVector[r]))
        print('--------------------------------')

