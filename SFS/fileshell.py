from SFS import diskpy
from SFS import sfs
def help():
    print('# help')
    print('# disk_init [File Name] [No of Blocks]')
    print('      *** Create a new disk')
    print('# disk_open [File Name]')
    print('      *** Open a existing')
    print('# disk_status')
    print('      *** display disk status')
    print('# disk_read [Block No]')
    print('      *** read block from disk and print')
    print('# disk_write [Block No]')
    print('      *** Write buffer to the Disk')
    print('# disk_close')
    print('      *** Close disk')
    print('------------------------------------------------------')
    print('# read_to_buffer [Block No]')
    print('      *** read block from disk and add to buffer')
    print('# buffer_fill [String]')
    print('      *** read block from String and add to buffer')
    print('# buffer_print')
    print('      *** print current buffer')
    print('# buffer_clear')
    print('      *** delete the buffer')
    print('# exit')
    
disk = diskpy.mydisk()
buffersize = 512
buffer = bytearray()

def disk_init(user_input):
    if len(user_input) == 3 and user_input[2].isdigit():
        disk.disk_init(user_input[1],int(user_input[2]))
    else :
        print ('Wrong Arguments :',user_input)
#        help()

def disk_open(user_input):
    if len(user_input) == 2 :
        disk.disk_open(user_input[1])
    else :
        print ('Wrong Arguments :',user_input)
#        help()

def disk_status(user_input):
    disk.disk_status()

def disk_read(user_input):
    if len(user_input) == 2 and user_input[1].isdigit():
        r = disk.disk_read(int(user_input[1]))
        if r != None:
            print(r.decode())
    else :
        print ('Wrong Arguments :',user_input)
#        help()

def disk_close(user_input):
    disk.disk_close()

def buffer_create(user_input):
    global buffer
    global buffersize
    if len(user_input) == 2 and user_input[1].isdigit():
        buffer = bytearray()
        buffersize = int(user_input[1])
    else :
        print ('Wrong Arguments :',user_input)
#        help()

def read_to_buffer(user_input):
    global buffer
    global buffersize
    if buffer == None:
        print("Buffer not created")
    elif len(buffer) == buffersize:
        print("Buffer full use buffer_clear to delete or buffer_write to save")
    elif len(user_input) == 2 and user_input[1].isdigit():
        buffer += bytearray(disk.disk_read(int(user_input[1])))
        buffer = buffer[:buffersize]
    else :
        print ('Wrong Arguments :',user_input)
#        help()

def buffer_fill(user_input):
    global buffer
    if buffer == None:
        print("Buffer not created")
    elif len(buffer) >= buffersize:
        print("Buffer full use buffer_clear to delete or buffer_write to save")
    elif len(user_input) == 2 :
        buffer += bytearray(user_input[1], "utf8")
        buffer = buffer[:buffersize]
    else :
        print ('Wrong Arguments :',user_input)
#        help()

def disk_write(user_input):
    global buffer
    if buffer == None:
        print("no Buffer to write")
    elif len(user_input) == 2 and user_input[1].isdigit():
        disk.disk_write(int(user_input[1]),buffer[:disk.blocksize])
        buffer = bytearray()
    else :
        print ('Wrong Arguments :',user_input)
#        help()

def buffer_print(user_input):
    global buffer
    if buffer == None:
        print("Buffer not created")
    else :
        print(buffer.decode())

def buffer_clear(user_input):
    global buffer
    if buffer == None:
        print("Buffer not created")
    else :
        buffer = bytearray()

def scan_blockmap(user_input):


print("\n###########\nStarting Simple File System")   
help()
while True:
    user_input = input('SFS>').strip().split(' ')
    func = user_input[0].lower()
    if func == 'help':
        help()
    elif func == 'disk_init':
        disk_init(user_input)
    elif func == 'disk_open':
        disk_open(user_input)
    elif func == 'disk_status':
        disk_status(user_input)
    elif func == 'disk_read':
        disk_read(user_input)
    elif func == 'disk_write':
        disk_write(user_input)
    elif func == 'disk_close':
        disk_close(user_input)
    elif func == 'read_to_buffer':
        read_to_buffer(user_input)
    elif func == 'buffer_fill':
        buffer_fill(user_input)
    elif func == 'buffer_print':
        buffer_print(user_input)
    elif func == 'buffer_clear':
        buffer_clear(user_input)
    elif func == 'scan_blockmap':
        scan_blockmap(user_input)
    elif func == 'exit':
        print('Exit Simple File System')
        break
    else :
        print ('Wrong command :',user_input)
#        help()

    