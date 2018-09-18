
import numpy as np
from memory.memcommon import MemCommon
from memory.memmgmt import MemMgmt 

class MemMgr:
    row_size = MemCommon.row_size
    column_size = MemCommon.column_size
    mgmt_row_size = MemCommon.mgmt_row_size
    mgmt_column_size = MemCommon.mgmt_column_size

    memarray = np.zeros(shape=(row_size,column_size), dtype = 'int8')
    

    @classmethod
    def get_mem(cls, pid, nbrblocks):
        start_index,end_index = MemMgmt.find_free_space(pid,nbrblocks)
        
        if start_index == MemCommon.Invalid:
            return MemCommon.NULLARRAY
        else:
            aa = MemMgr.memarray[start_index:end_index+1,:MemMgr.column_size]
        return aa
      

    @classmethod
    def release_mem(cls, pid):
        MemMgmt.release_mem(pid)

    @classmethod
    def display_mem(cls):
        print ('----------memory array --------')
        for i in range(0,MemMgr.row_size):
            print(str(i)+' : '+ str(MemMgr.memarray[i,:MemMgr.column_size]))
        print('--------------------------------')
    
      