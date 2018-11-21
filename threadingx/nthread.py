import time
import threading

class CountdownThread(threading.Thread):

    def __init__(self,name,account):
        threading.Thread.__init__(self)
        self.name = name
        self.count = account

    def run(self):
        while self.count >0:
            print(self.getName(),":Counting Down",self.count)
            self.count -=1
            time.sleep(3)
        print("exit thread",self.getName())
        return


