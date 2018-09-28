import numpy as np
from memory.memcommon import MemCommon
import memory.memerror as me
#from memory.memmgr import MemMgr
class MemMgmt:
    mgmt =  np.zeros(shape=(MemCommon.mgmt_row_size,MemCommon.mgmt_column_size), dtype = 'int32')
    
    @classmethod
    def find_free_space(cls, pid, nbrblocks):
        pid_coulmn = MemCommon.pid_column
        indexList = []
        for r in range(0,MemCommon.mgmt_row_size):
            if (MemMgmt.mgmt[r,pid_coulmn] == 0):
                indexList.append(r)
            if len(indexList) == nbrblocks:
                MemMgmt.update_mgmt(pid,indexList)
                return indexList
        raise me.NOMEMORY

                

    @classmethod
    def update_mgmt(cls, pid, indexes):   
        # update the mgmt table
        pid_column = MemCommon.pid_column
        for r in indexes:
           MemMgmt.mgmt[r,pid_column] = pid

    @classmethod
    def release_mem(cls, pid):
        found = False
        for x in range(0,MemCommon.mgmt_row_size):
            if (MemMgmt.mgmt[x,0] == pid):
                found = True
                MemMgmt.mgmt[x,0] = 0
        if found :
            return pid
        else :
            return MemCommon.Invalid

    
    @classmethod
    def display_mgmt(cls):
        print ('----------Management array --------')
        for r in range(0,MemCommon.mgmt_row_size):
            print(str(r) + ' : '+ str(MemMgmt.mgmt[r,:MemCommon.mgmt_column_size]))
        print('--------------------------------')