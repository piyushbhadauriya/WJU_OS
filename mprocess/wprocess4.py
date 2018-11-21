from multiprocessing import Process, Array, sharedctypes
import os
import numpy as np 

column_size = 8
row_size = 4
mema = np.empty(shape=(row_size,column_size),dtype='int8')

def modify(arr,vv):
    for r in range(0,len(arr)):
        arr[r] = vv
    print("[",os.getpid(),"]---") 
    print(arr[:])
    print()
    print(mema)
    print()


if __name__ == '__main__':
    viewa = mema[0:2,:column_size]
    modify(viewa,11)
    viewb = mema[2:4,:column_size]
    modify(viewb,33)

    # change viewa to 1d array arr 
    shape = viewa.shape
    viewa.shape = viewa.size
    arr = Array('i', viewa.tolist())

    p = Process(target=modify,args = (arr,22))
    p.start()
    p.join()

    # Update viewa
    for i in range(len(arr)):
        viewa[i] = arr[i]
    viewa.shape = shape

    print('Back to main: print whole array')
    print(mema)



