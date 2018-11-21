import threadingx.nthread as nt

t1 = nt.CountdownThread("t1",10)
t1.start()

t2 = nt.CountdownThread("t2",20)
t2.start()

print("exit Main thread")