import processx.processX as px
import memory.memmgr as mema
import memory.memmgmt as mgmt

p1 = px.ProcessX(4)
p1.display_PMT()

print(" ***** before loading ****")
mema.MemMgr.display_mem()
mgmt.MemMgmt.display_mgmt()
print(" ******************")

alist = [0,1]
p1.load_pages(alist)

print(" ***** after loading ****")
p1.display_PMT()
mema.MemMgr.display_mem()
mgmt.MemMgmt.display_mgmt()
print(" ******************")

# now get those vestors
vectorlist = p1.get_vectors()
nbr = 22
for v in vectorlist:
    for r in range(0,v.shape[0]):
        v[r] = nbr
    nbr += 11

print(" ***** modifying  ****")
mema.MemMgr.display_mem()
print(" ******************")