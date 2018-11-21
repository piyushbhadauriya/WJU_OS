import threading
x = 0
nn = 100000

def addx():
    global x
    for i in range (nn):
        x += 1
    print ('exit from addx')
    return

def subx():
    global x
    for i in range(nn):
        x -= 1
    print ('exit from subx')
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
 