import os

class mydisk:
    diskimage = None # file pointer
    filename = None # name of the image file
    blocksize = 512
    nbrOfBlocks = 0
    
    @classmethod
    def disk_init(cls,image, nbrOfBlocks):
        cls.nbrOfBlocks = int(nbrOfBlocks)
        cls.diskimage = None
        cls.filename = image
        arr = bytearray(cls.blocksize)
        with open(cls.filename, 'wb') as fb:
            [fb.write(arr) for i in range(nbrOfBlocks)]   

    # Open an existing disk
    @classmethod
    def disk_open(cls,filename = None):
        if filename == None:
            filename = cls.filename
        try:
            cls.diskimage = open(filename, 'rb+')
            cls.filename = filename
            return True
        except Exception as es:
            print('invalid filename use init_disk to create it')
            print(es)
            return False
        

    #Read the whole block and return an array or list of bytes
    @classmethod
    def disk_read(cls,blockNumber,size=blocksize):
        if cls.diskimage == None:
            print('plese open the disk image using disk_open berfore reading')
            return None
        elif (blockNumber < 0):
            print('read failed: invalid Block number')
            return None
        else :
            try :
                #cls.diskimage.seek(blockNumber*cls.blocksize)
                # go to the start
                cls.diskimage.seek(0, 0)
                cls.diskimage.seek(blockNumber*cls.blocksize)
                return cls.diskimage.read(size)
            except Exception as es:
                print('read failed, unable to read block',blockNumber)
                print(es)

    # Write a block of bytes to a designated block number
    # Returns error code or success code
    @classmethod
    def disk_write(cls,blockNumber, byteArray,offset=0):
        if cls.diskimage == None:
            print('plese open the disk image using disk_open berfore writing')
            return False
        elif (blockNumber >= cls.nbrOfBlocks):
            print('write failed: invalid Block number')
            return False
        else:
            cls.diskimage.seek(0, 0)
            cls.diskimage.seek(int(blockNumber*cls.blocksize+offset))
            if len(byteArray) > cls.blocksize:
                print ('given bytearray is bigger then block size')
                return False
            else: 
                cls.diskimage.write(byteArray)
                return True

    # Display the statistics of disk
    @classmethod
    def disk_status(cls):
        if cls.filename != None:
            print("Diskimage : ",cls.filename)
            print("Block size : ",cls.blocksize," Bytes")
            size = os.path.getsize(cls.filename)
            print("Number Of Blocks : ",cls.nbrOfBlocks)
            print ("Disk Size : ", size, " Bytes")
        else:
            print ("No image file")
        if cls.diskimage != None:
            print("DiskStatus : Open :",cls.filename)
        else :
             print("DiskStatus : Closed")

    # Forces all outstanding writes to disk and closes the associated image file
    @classmethod
    def disk_close(cls):
        if cls.diskimage != None:
            cls.diskimage.close()
            cls.diskimage = None
            return True
        else: 
            print('No Disk image to close')
            return False

    @classmethod
    def setnbrOfBlocks(cls,nbrOfBlocks):
        cls.nbrOfBlocks = nbrOfBlocks

'''
mydisk.disk_init("image1.10",10)
mydisk.disk_open("image1.10")
mydisk.disk_write(2,b'\xAB\xCD\xeF')
mydisk.disk_write(1,b'\xaa' * 20)
print(mydisk.disk_read(1))
print(mydisk.disk_read(2))

mydisk.disk_close()
mydisk.disk_open("image1.10")

print(mydisk.disk_read(2))
mydisk.disk_status()
'''