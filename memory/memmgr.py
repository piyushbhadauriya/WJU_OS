
import numpy as np
from memory.memcommon import MemCommon
from memory.memmgmt import MemMgmt 
from memory.memerror import NOMEMORY

class MemMgr:
    row_size = MemCommon.row_size
    column_size = MemCommon.column_size
    mgmt_row_size = MemCommon.mgmt_row_size
    mgmt_column_size = MemCommon.mgmt_column_size

    memarray = np.zeros(shape=(row_size,column_size), dtype = 'int64')
    

    @classmethod
    def get_mem(cls, pid, nbrblocks):
        mem_list = [] 
        try:
            alist = MemMgmt.find_free_space(pid,nbrblocks)
        except NOMEMORY :
            return [None]
        
        if len(alist) == nbrblocks:
            for pageFrameIndex in alist:
                aa = MemMgr.memarray[pageFrameIndex]
                tuplea = (pageFrameIndex,aa)
                mem_list.append(tuplea)
        return mem_list

    @classmethod
    def release_mem(cls, pid):
        MemMgmt.release_mem(pid)

    @classmethod
    def display_mem(cls):
        print ('----------memory array --------')
        for i in range(0,MemMgr.row_size):
            print(str(i)+' : '+ str(MemMgr.memarray[i,:MemMgr.column_size]))
        print('--------------------------------')
    