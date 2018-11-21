import processx.processX as px
import memory.memmgr as mema
import memory.memmgmt as mgmt
import threading

def modify(px):
    nbr = px.get_mypid()
    vectorlist = px.get_vectors()
    for v in vectorlist:
        for r in range(0,v.shape[0]):
            v[r] = nbr

def printMgmt():
    print("================= Global Memory Management ================")
    mema.MemMgr.display_mem()
    mgmt.MemMgmt.display_mgmt()
    print (mgmt.MemMgmt.process_table)
    print(" ==========================================================")

def printProcess(myprocess):
    myprocess.display_ProcessMgT()
    

def mythread(T_name,px,pages):
    print("****Thread ", T_name, " Starts****")
    print(T_name, " : ask for ",len(pages)," block of memory")
    px.load_pages(pages)
    modify(px)
    print(T_name,' : exit')
    return  

# first process
print(" ************** Process : P1 Starts with two threads ***********")
p1 = px.ProcessX(4)
t11 = threading.Thread(target = mythread, args = ('P1_T1',p1,[0,1]))
t12 = threading.Thread(target = mythread, args = ('P1_T2',p1,[2]))
t11.start()

# second process
print(" ************** Process : P2 Starts with two threads************")
p2 = px.ProcessX(3)
t21 = threading.Thread(target = mythread, args = ('P2_T1',p2,[0]))
t22 = threading.Thread(target = mythread, args = ('P2_T2',p2,[1]))
t21.start()

# First preocess thread 2
t12.start()

# Second preocess thread 2
t22.start()

# third process
print(" ************** Process : P3 Starts with one thread*************")
p3 = px.ProcessX(3)
t31 = threading.Thread(target = mythread, args = ('P3_T1',p3,[0,1]))
t31.start()

# fourth process
print(" ************** Process : P4 Starts with one thread*************")
p4 = px.ProcessX(4)
t41 = threading.Thread(target = mythread, args = ('P4_T1',p4,[0]))
t42 = threading.Thread(target = mythread, args = ('P4_T2',p4,[2]))
t41.start()
t42.start()
t12.join()
print("************** Process : P1 **************")
printProcess(p1)
t22.join()
print("************** Process : P2 **************")
printProcess(p2)
t31.join()
print("************** Process : P3 **************")
printProcess(p3)
t41.join()
print("************** Process : P4 **************")
printProcess(p4)
printMgmt()