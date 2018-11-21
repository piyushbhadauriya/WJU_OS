import multiprocessing as mp
import numpy as np
import os

def worker(arr, X_shape, rowIndex, value1):
    print(os.getppid(), " --worker -------->", os.getpid())
    x_np = np.frombuffer(arr, dtype=np.int).reshape(X_shape)
    x_np[rowIndex,:] = value1
    print(arr[:])
    print(x_np)
    print()

if __name__ == '__main__':
    X_shape = (3,4)
    X = mp.RawArray('i', X_shape[0] * X_shape[1])
    print("---- main ----")
    print(X[:])
    worker(X,X_shape, 0,11)
    p = mp.Process(target=worker, args=(X, X_shape, 1, 22,))
    p.start()
    p.join()
    print(" ---- main - after process change --- ")
    print(X[:])