import processx.processX as px
import memory.memmgr as mema
import memory.memmgmt as mgmt


def modify(px):
    nbr = px.get_mypid()
    vectorlist = px.get_vectors()
    for v in vectorlist:
        for r in range(0,v.shape[0]):
            v[r] = nbr
'''    

'''

def printAll(astring,myprocess):
    print(" ********* start: ", astring, '*********')
    myprocess.display_ProcessMgT()
    print("================= Global Memory Management ================")
    mema.MemMgr.display_mem()
    mgmt.MemMgmt.display_mgmt()
    print(" *********** end: ", astring, '***********')


# first process
p1 = px.ProcessX(4)
p1.load_pages([0,1])
modify(p1)
printAll("first process p1 ",p1)

# second process
p2 = px.ProcessX(3)
p2.load_pages([0])
modify(p2)
printAll("second process p2 ",p2)

# first process does another load_pages
p1.load_pages([2])
modify(p1)
printAll(" first process p1 do a load again",p1)

# second process does another load
p2.load_pages([1])
modify(p2)
printAll(" second process p2 do a load again",p2)

# third process
p3 = px.ProcessX(3)
p3.load_pages([0,1])
modify(p3)
printAll("third process p3 ",p3)

# forth process
p4 = px.ProcessX(3)
p4.load_pages([0])
modify(p4)
printAll("forth process p4 ",p4)

print ('###### PID to Process dict ############')  
print (mgmt.MemMgmt.process_table)
