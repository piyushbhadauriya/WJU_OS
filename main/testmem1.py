from memory.memmgr import MemMgr
from memory.memmgmt import MemMgmt

def change_contenets(array1,value1):
    for r in range(0,array1.shape[0]):
        for c in range(0,array1.shape[1]):
            array1[r,c] = value1

MemMgr.display_mem()
MemMgmt.display_mgmt()
a1 = MemMgr.get_mem(222,2)
change_contenets(a1,22)
MemMgmt.display_mgmt()
a1 = MemMgr.get_mem(333,1)
MemMgmt.display_mgmt()
a1 = MemMgr.get_mem(444,2)
MemMgmt.display_mgmt()
a1 = MemMgr.get_mem(555,1)
MemMgmt.display_mgmt()
MemMgr.release_mem(333)
MemMgmt.display_mgmt()
# display a1 - add code

# modify a1 - add code

# display a1 - add code
change_contenets(a1,11)
MemMgr.display_mem()
#print(a1)

#print(MemMgr.find_free_space(8))
#MemMgr.display_mgmt()

#a2 = MemMgr.get_mem(222,2)

# display a2 - - add code
# modify a2 - add code
# display a2 - add code

#a3 = MemMgr.get_mem(333,3)

#MemMgr.display_mgmt()

#MemMgr.release_mem(111)
#MemMgr.release_mem(222)
#MemMgr.release_mem(333)

#MemMgr.display_mgmt()