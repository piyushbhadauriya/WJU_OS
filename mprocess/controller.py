import multiprocessing as mp 

class worker(mp.process):
    def __init__(self,inque,outque):
        self.inque = inque
        self.outque = outque
    
    def run(self):
        while True:
            pass

class dispatcher(mp.process):
    def __init__(self,orderque):
        self.outque = mp.Queue()
        [self.inqueues.append(mp.Queue()) for i in range(4)]
        [self.processque.append(mp.Process(target=worker,
                args = inque,outque,))for inque in inqueus]

    def run():
        pass



if __name__ == '__main__':
    orderque = mp.Queue()
    dispatch = dispatcher(orderque)
    resque = mp.Queue()
