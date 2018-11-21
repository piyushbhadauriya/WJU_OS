import threading
import multiprocessing as mp 
import time

ntimes = 1000000

def count(n):
    while n>0:
        n-=1

if __name__ == '__main__':
    t1_start = time.time()
    count(ntimes)
    count(ntimes)
    t1_end = time.time()

    print("seqential exe time :",t1_end-t1_start)

    t1_start = time.time()
    thread1 = mp.Process(target=count,args=(ntimes,))
    thread2 = mp.Process(target=count,args=(ntimes,))
    thread1.start()
    thread2.start() 
    thread1.join()
    thread2.join()
    t1_end = time.time()
    print("thread exe time :",t1_end-t1_start)