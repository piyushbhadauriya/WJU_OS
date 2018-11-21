import multiprocessing as mp 

def foo(q):
    q.put('hello')
    q.put([42,None,'hello'])

if __name__ == '__main__':
    ctx = 
    q = ctx.Queue()
    p = ctx.Process(Target=foo,args=(q,))
    p.start()
    print(q.get())
    print(q.get())
    print(q.get())
    p.join()