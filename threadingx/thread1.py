import time
import threading

def countdown(aname, account):
    while account > 0:
        print(aname, " : counting down ",account)
        account -=1
        time.sleep(2)
    print(aname,' :exit')
    return

t1 = threading.Thread(target = countdown, args = ('t1',10,))
t1.start()

t2 = threading.Thread(target = countdown, args = ('t2',20,))
t2.start()
print('exit main thread')