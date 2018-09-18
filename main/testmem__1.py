from memory.memmgr_1 import MemMgr
import memory.memerror_1 as me
import traceback

def change_contents(array1, value1):
    for r in range(0, array1.shape[0]):
        for c in range(0, array1.shape[1]):
            array1[r,c] = value1
    
try:
    a1 = MemMgr.get_mem(222,13)
    change_contents(a1, 22)
    # print(a1)

    a2 = MemMgr.get_mem(333,1)
    change_contents(a2, 33)
    # print(a2)

    a3 = MemMgr.get_mem(444,1)
    change_contents(a3, 44)

    MemMgr.release_mem(333)

    a4 = MemMgr.get_mem(555, 2)
    change_contents(a4, 55)
except me.NOMEMORY:
    print("memory error caught *******************")
    traceback.print_exc()
    print("**********************")
    

MemMgr.display_mem()
MemMgr.display_mgmt()

# a2 = MemMgr.get_mem(222,2)

# display a2 - - add code
# modify a2 - add code
# display a2 - add code

# a3 = MemMgr.get_mem(333,3)

# MemMgr.release_mem(111)
# MemMgr.release_mem(222)
# MemMgr.release_mem(333)

# MemMgr.display_mgmt()