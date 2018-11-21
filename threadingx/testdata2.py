import threading
x = 0
nn = 100000
x_lock = threading.Lock()

def addx():
    global x
    x_lock.acquire()
    for i in range (nn):
        x += 1
    print ('exit from addx')
    x_lock.release()
    return

def subx():
    global x
    x_lock.acquire()
    for i in range(nn):
        x -= 1
    print ('exit from subx')
    x_lock.release()
    return

# test program
t1 = threading.Thread(target=addx)
t2 = threading.Thread(target=subx)

t1.start()
t2.start()

# wait for completion
t1.join()
t2.join()

print ('value of x = ', x)
print('Exit from main thread')
 

'''import threading
class Aa(Object):
nn = 100000
lock = 
x = 0 #shard object

    @classmethod
    def addx(cls):

        pass

    @classmethod
    def subx(cls):
        pass


threads = []
for func in [Aa.addx.Aa.subx]:
    threads.append(threading.Thread(target=func))
    threads[-1].start()

for thread in threads:

    thread.join()

print('Value of x ',Aa.x)
print ('exit from main thread') 
'''