import time
import threading

def countdown(aname, account):
    while account > 0:
        print(aname, " : counting down ",account)
        account -=1
        time.sleep(1)
    print(aname,' : exit')
    return

t1 = threading.Thread(target = countdown, args = ('t1',10,))
t1.start()
t1.join()

t2 = threading.Thread(target = countdown, args = ('t2',20,))
t2.start()
t2.join()
print('exit main thread')
