
import numpy as np
import memory.memerror_1 as me


class MemMgr:
    row_size = 7               # max number of rows
    column_size = 6            # max number of columns
    mgmt_row_size = row_size    # max number of rows for mgmt
    mgmt_column_size = 1        # max number of columns for mgmt
                                #  -- one column of pid
    pid_column = 0              # column for pid

    # memory array to represent memory we manage
    mem = np.zeros(shape=(row_size,column_size), 
                    dtype='int8')
    # management of memory - an array of process identifiers pid
    mgmt = np.zeros(shape=(mgmt_row_size,mgmt_column_size),
                    dtype='int32')

    @classmethod
    def find_free_space(cls, nbr):
        start_row = 0  # indicates none
        end_row = MemMgr.row_size
        # start the search from row 0
        found = False
        for i in range(start_row, end_row):
            if MemMgr.mgmt[i,0] == 0:
                # found the first row that is free
                # now check whether we have nbr rows free
                nbrx = i+nbr
                found = True
                try:
                    for x in range(i, nbrx):
                        if MemMgr.mgmt[x,0] == 0:
                            continue
                        else:
                            found = False
                            break
                except IndexError:
                    raise me.NOMEMORY
            if found:
                start_index = i
                end_index = i+nbr-1
                return start_index, end_index

        raise me.NOMEMORY  # no empty space

    @classmethod
    def add_mgmt(cls, start_index, end_index, pid):
        for r in range(start_index, end_index+1):
            MemMgr.mgmt[r, MemMgr.pid_column] = pid

    @classmethod
    def get_mem(cls, pid, nbrblocks):

        assert(nbrblocks > 0),"[get_mem()] Number of blocks > 0"

        # find free space in memory
        start_index,end_index = MemMgr.find_free_space(nbrblocks)

        aa = MemMgr.mem[start_index:end_index+1,:MemMgr.column_size]
        
        # update the mgmt table
        MemMgr.add_mgmt(start_index, end_index, pid)
        

        return aa        # we did not check for errors. 
                         # Add error handling later.
                         # if the dimensions are not correct 
                         # get a ValueError - 
                         # use try except block

    @classmethod
    def release_mem(cls, pid):
        print('release_mem from pid ', pid)
        for r in range(0, MemMgr.mgmt_row_size):
            if MemMgr.mgmt[r,0] == pid:
                MemMgr.mgmt[r,0] = 0
        return pid

    @classmethod
    def display_mem(cls):
        print('--------- memory array -----')
        # todo: pretty print to include index
        for r in range(0, MemMgr.row_size):
            print(r, ' : ', MemMgr.mem[r,
                    :MemMgr.column_size])
    
        print('----------------------------')

    @classmethod
    def display_mgmt(cls):
        print('--------management array ------')
        # todo: pretty print to include index
        for r in range(0,MemMgr.mgmt_row_size):
            print(r, ' : ', MemMgr.mgmt[r,0])
        print('-------------------------------')