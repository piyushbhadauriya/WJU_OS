import processx.processX as px
import memory.memmgr as mema
import memory.memmgmt as mgmt
import threading
import time

def modify(px):
    nbr = px.get_mypid()
    vectorlist = px.get_vectors()
    for v in vectorlist:
        for r in range(0,v.shape[0]):
            v[r] = nbr

def mythread(ps,T_name,pages):
    print(T_name, " : ask for ",len(pages)," block of memory")
    ps.load_pages(pages)
    print(T_name,' : exit')
    return   

def printAll(astring,myprocess):
    myprocess.display_ProcessMgT()
    print("======== Global Memory Management ==========")
    mema.MemMgr.display_mem()
    mgmt.MemMgmt.display_mgmt()
    print(" ******************** end: ", astring, '******************')

# first process
p1 = px.ProcessX(4)
t11 = threading.Thread(target = mythread, args = (p1,'P1_T1',[1]))
t11.start()
time.sleep(2)
t12 = threading.Thread(target = mythread, args = (p1,'P1_T2',[0]))
t12.start()
time.sleep(2)
modify(p1)
printAll("First Process p1 ",p1)

# second process
p2 = px.ProcessX(3)
t21 = threading.Thread(target = mythread, args = (p2,'P2_T1',[0,1]))
t21.start()
time.sleep(2)
t22 = threading.Thread(target = mythread, args = (p2,'P2_T2',[2]))
t22.start()
time.sleep(2)
modify(p2)
printAll("Second process p2 ",p2)


# third process
p3 = px.ProcessX(3)
t31 = threading.Thread(target = mythread, args = (p3,'P3_T1',[2]))
t31.start()
time.sleep(2)
modify(p3)
printAll("Third process p3 ",p3)

# fourth process
p4 = px.ProcessX(1)
t41 = threading.Thread(target = mythread, args = (p4,'P4_T1',[0]))
t41.start()
time.sleep(2)
modify(p4)
printAll("Fourth process p4 ",p4)