import random,time
from threading import BoundedSemaphore, Thread
max_item = 5
container = BoundedSemaphore(max_item)

def preoducers (nloop):
    for i in range nloops:
        #sleep
            #print
            try:
                pass
            except expression as identifier:
                pass

def consumer(nloops):

    for i in range(nloops):
        #sleep
        #print
        if container.acquire(False):
            print ("consumed an item")
        else:
            print('empty')


threads = []
nloops =random.randrange(3,6)

print("Starting with %s items", %max_item)

threads.append(Thread(target=property))
threads.append(Thread(target=consumer), random.randrange(nloop,nloops+max_item+2))

for thread in threads:
    thread.start()

for thread in threads:
    thread.join()
print("allfone")