import numpy as np
from memory.memcommon import MemCommon
import memory.memerror as me
import threading

class MemMgmt:
    # lock down mgmt structure when it is updated relese Mem and updatemem
    mgmt_lock = threading.Lock()
    mgmt =  np.zeros(shape=(MemCommon.mgmt_row_size,MemCommon.mgmt_column_size), dtype = 'int32')
    counter = 1
    process_table = {}
    
    @classmethod
    def release_mem(cls, pid):
        found = False
        for x in range(0,MemCommon.mgmt_row_size):
            if (MemMgmt.mgmt[x,0] == pid):
                found = True
                cls.mgmt_lock.acquire()
                MemMgmt.mgmt[x,MemCommon.pid_column] = 0
                MemMgmt.mgmt[x,MemCommon.FIFO_column] =  0
                MemMgmt.mgmt[x,MemCommon.LRU_column] =  0
                cls.mgmt_lock.release()
        if found :
            return pid
        else :
            return MemCommon.Invalid
  
    @classmethod
    def update_mgmt(cls, pid, indexes):   
        # update the mgmt table
        pid_column = MemCommon.pid_column
        cls.mgmt_lock.acquire()
        for r in indexes:
           MemMgmt.mgmt[r,pid_column] = pid
           MemMgmt.mgmt[r,MemCommon.FIFO_column] =  cls.counter
           MemMgmt.mgmt[r,MemCommon.LRU_column] =  1
           cls.counter += 1
        cls.mgmt_lock.release()

    @classmethod
    def find_free_space(cls, pid, nbrblocks):
        index_free = cls.find_existing(pid,nbrblocks)
        index_replace = {}
        if nbrblocks-len(index_free) > 0 :
            index_replace = cls.find_FIFO(nbrblocks-len(index_free))
        for index in index_replace:
            cls.inform_process(index_replace[index],index)
            index_free.append(index)
        cls.update_mgmt(pid,index_free)
        return index_free

    @classmethod
    def find_existing(cls, pid, nbrblocks):
        pid_coulmn = MemCommon.pid_column
        indexList = []
        cls.mgmt_lock.acquire()
        for r in range(0,MemCommon.mgmt_row_size):
            if (MemMgmt.mgmt[r,pid_coulmn] == 0):
                indexList.append(r)
            if len(indexList) == nbrblocks:
                break 
        cls.mgmt_lock.release()       
        return indexList

    @classmethod
    def find_FIFO(cls,nbr):
        # funtion will return dict of {index:pid}
        adict = {}
        for r in range(0, nbr):
            arow, apid = MemMgmt.find_earliest()
            adict[arow] = apid
        return adict   
    @classmethod
    def find_earliest(cls):
        min = 9999
        fc = MemCommon.FIFO_column
        pc = MemCommon.pid_column
        min_row = -1
        cls.mgmt_lock.acquire()
        for r in range(0,MemCommon.mgmt_row_size):
            if (MemMgmt.mgmt[r,fc] != 0 and MemMgmt.mgmt[r,pc] != 0):
                if MemMgmt.mgmt[r,fc] < min:
                    min = MemMgmt.mgmt[r,fc]
                    min_row = r
        MemMgmt.mgmt[min_row,fc] = 0
        cls.mgmt_lock.release()
        return min_row, MemMgmt.mgmt[min_row,pc]
    
    @classmethod
    def find_LRU(cls,nbr):
        # funtion will return dict of {index:pid}
        adict = {}
        cls.sweep()
        for r in range(0, nbr):
            arow, apid = MemMgmt.find_LeastRecent()
            MemMgmt.mgmt[arow,MemCommon.LRU_column] = 0
            adict[arow] = apid
        return adict
    @classmethod
    def find_LeastRecent(cls):
        min = 9999
        lc = MemCommon.LRU_column
        pc = MemCommon.pid_column
        min_row = -1
        for r in range(0,MemCommon.mgmt_row_size):
            if (MemMgmt.mgmt[r,lc] != 0 and MemMgmt.mgmt[r,pc] != 0):
                if MemMgmt.mgmt[r,lc] < min:
                    min = MemMgmt.mgmt[r,lc]
                    min_row = r
        return min_row, MemMgmt.mgmt[min_row,pc]

    @classmethod
    def inform_process(cls,pid,index):
        px = cls.process_table[pid]
        px.release_frame(index)

    @classmethod
    def register(cls, obj):
        MemMgmt.process_table[obj.get_mypid()] = obj

    @classmethod
    def sweep(cls):
        lru = MemCommon.LRU_column
        for r in range (MemCommon.mgmt_row_size):
            if (MemMgmt.mgmt[r,lru] > 1 ):
                MemMgmt.mgmt[r,lru] -= 1

    @classmethod
    def mark(cls, index):
        if MemMgmt.mgmt[index,MemCommon.pid_column] != 0 :
            MemMgmt.mgmt[index,MemCommon.LRU_column] += 1 
    
    @classmethod
    def display_mgmt(cls):
        print ('----------Management array --------')
        print ('Ix: [PID  FIFO  LRU]')
        for r in range(0,MemCommon.mgmt_row_size):
            print(str(r) + ' : '+ str(MemMgmt.mgmt[r,:MemCommon.mgmt_column_size]))
        print('--------------------------------')