import diskpy
from sfs import sfs
import createDirStructure

def help():
    print('# cmds                             *** Display List of commands ')
    print('# disk_init [Number of Blocks]     *** Initialize a disk to a given number of blocks')
    print('# disk_format                      *** Create a formated file syatem')
    print('# disk_open [File Name]            *** Open a disk with a filename')
    print('# disk_read [Block No]             *** read block from disk to buffer and print')
    print('# disk_write [Block No]            *** Write buffer to the Disk')
    print('# disk_close                       *** Close disk')
    print('# display_buffer                   *** print current buffer')
    print('# write_to_buffer [string]         *** write a string or number to buffer')
    print('# create_file [Name]               *** create a file at current directory')
    print('# mkdir [Name]                     *** create a directory at current directory ')
    print('# dir                              *** display contents of current directory')
    print('# cd [dirctory]                    *** change directory')
    print('# pwd                              *** Current directory path')
    print('# exit                             *** Exit shell')
    print('------------------------------------------------------')

    
    
disk = diskpy.mydisk()
buffersize = disk.blocksize
buffer = bytearray()
location = '/'
c_inode = None

def disk_init(user_input):
    if len(user_input) == 2 and user_input[1].isdigit():
        sfs.fs_init(int(user_input[1]))
        print('disk initialized')
    else :
        print ('Wrong Arguments :',user_input)

def disk_open(user_input):
    if len(user_input) == 2 :
        res = sfs.fs_open(user_input[1])
        if res == True:
            print('Disk of file "', user_input[1],'" opened')
    else :
        print ('Wrong Arguments :',user_input)

def disk_status(user_input):
    disk.disk_status()

def disk_read(user_input):
    global buffer
    if len(user_input) == 2 and user_input[1].isdigit():
        r = disk.disk_read(int(user_input[1]))
        if r != None:
            buffer = r[:buffersize]
            print('Block ', user_input[1] ,' read to buffer')
            #print(r)
    else :
        print ('Wrong Arguments :',user_input)

def disk_close(user_input):
    res = disk.disk_close()
    if res == True:
        print('Disk of file "', user_input[1],'" Closed')

# def buffer_create(user_input):
#     global buffer
#     global buffersize
#     if len(user_input) == 2 and user_input[1].isdigit():
#         buffer = bytearray()
#         buffersize = int(user_input[1])
#     else :
#         print ('Wrong Arguments :',user_input)
#        help()

def read_to_buffer(user_input):
    global buffer
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

def write_to_buffer(user_input):
    global buffer
    if buffer == None:
        print("Buffer not created")
    # elif len(buffer) >= buffersize:
    #     print("Buffer full use buffer_clear to delete or buffer_write to save")
    elif len(user_input) == 2 :
        buffer = bytearray(user_input[1], "utf8")
        buffer = buffer[:buffersize]
    else :
        print ('Wrong Arguments :',user_input)
#        help()

def disk_write(user_input):
    global buffer
    if buffer == None:
        print("no Buffer to write")
    elif len(user_input) == 2 and user_input[1].isdigit():
        blockNo = int(user_input[1])
        print('Warning: Disk write is unprotected and it can corrupt the file system')
        print('Format the disk again before using directry structure cmds')
        disk.disk_write(blockNo,buffer[:disk.blocksize])
        print('*******Done: wrote ',len(buffer),' bytes')
        buffer = bytearray()
    else :
        print ('Wrong Arguments :',user_input)
#        help()

def display_buffer(user_input):
    global buffer
    if buffer == None:
        print("Buffer not created")
    else :
        print(buffer)

def buffer_clear(user_input):
    global buffer
    if buffer == None:
        print("Buffer not created")
    else :
        buffer = bytearray()
        
def scan(user_input):
    if disk.filename == None :
        print('Disk file not avilable. Use disk_init to create one')
    else :
        try:
            print('---Block Bitmap(Total ',disk.nbrOfBlocks,')---')
            sfs.scan_BlockBitMap()
            print('---Node Bitmap(Total 48)---')
            sfs.scan_NodeBitMap()
        except:
            print('Disk not formated')

def disk_format(user_input):
    global c_inode
    if disk.filename == None :
        print('Disk file not avilable. Use disk_init to create one')
    else :
        sfs.fs_format()
        c_inode = 1

def dir_structure(user_input):
    if disk.filename == None :
        print('Disk file not avilable. Use disk_init to create one')
    else :
        createDirStructure.createDirectoryStructure() 
       
def dir(user_input):
    if c_inode == None :
        print('Disk not formated use disk_format')
    else :
        sfs.showDir(c_inode)

def mkdir(user_input):
    if c_inode == None :
        print('Disk not formated use disk_format')
    elif len(user_input) == 2 :
        sfs.fs_mkdir(user_input[1],c_inode)
        print(' at location:',location)
    else :
        print ('Wrong Arguments :',user_input)
        
def create_file(user_input):
    if c_inode == None :
        print('Disk not formated use disk_format')
    elif len(user_input) == 2 :
        sfs.fs_mkfile(user_input[1],c_inode)
        print(' at location: ',location)
    else :
       print ('Wrong Arguments :',user_input) 

def pwd(user_input):
    if c_inode == None :
        print('Disk not formated use disk_format')
    else :
        print(location)

def cd(user_input):
    global c_inode
    global location
    if c_inode == None :
        print('Disk not formated use disk_format')
        return
    new = sfs.getinode(user_input[1],c_inode)
    if new == None:
        print('No Directry named [d_]'+user_input[1])
    else :
        c_inode = new
        if user_input[1] == '..':
            index = location.rstrip('/').rfind('/')
            #print(index)
            #print(location)
            if index == -1:
                index = 0
            location = location[:index+1]
            #print(location)
        elif user_input[1] == '.':
            location = location
        else:
            location += user_input[1]+'/'
        print('Changed to directory path ',location)

print("\n###########\nStarting Simple File System")   
help()
while True:
    user_input = input('SFS>').strip().split(' ')
    func = user_input[0].lower()
    if func == 'cmds':
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
    elif func == 'write_to_buffer':
        write_to_buffer(user_input)
    elif func == 'display_buffer':
        display_buffer(user_input)
    elif func == 'buffer_clear':
        buffer_clear(user_input)
    elif func == 'scan':
        scan(user_input)
    elif func == 'disk_format':
        disk_format(user_input)
    elif func == 'dir_structure':
        dir_structure(user_input)
    elif func == 'dir':
        dir(user_input)
    elif func == 'mkdir':
        mkdir(user_input)
    elif func == 'create_file':
        create_file(user_input)
    elif func == 'cd':
        cd(user_input)
    elif func == 'pwd':
        pwd(user_input)
    elif func == 'exit':
        print('Exit Simple File System')
        break
    else :
        print ('Wrong command :',user_input)
        print('use "cmds" for list of commands')
