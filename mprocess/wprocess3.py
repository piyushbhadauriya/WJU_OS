from multiprocessing import Process, Value, Array

def(n,a):
    n.Value = 3.141
    for i in range(len(a)):
        a[i] = -a[i]

if __name__ == '__main__':
    num = Value('d':0.0)
    arr = Array
