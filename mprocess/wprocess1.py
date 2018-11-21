import multiprocessing as mp 
import os

def info(title):
    print (title)
    print('module name:', __name__)
    print(' parant process',os.getppid())
    print(' process id',os.getpid())

def f(name):
    info('function f')