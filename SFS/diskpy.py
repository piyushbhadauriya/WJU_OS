import os

class mydisk:
    diskimage = None # file pointer
    image_name = None # name of the image file
    blocksize = 512
    nbrOfBlocks = 0
    
    @classmethod
    def disk_init(cls,filename, nbrOfBlocks):
        cls.image_name = filename
        cls.nbrOfBlocks = int(nbrOfBlocks)
        cls.diskimage = None
        arr = bytearray(cls.blocksize)
        with open(filename, 'wb') as fb:
            [fb.write(arr) for i in range(nbrOfBlocks)]
        

    # Open an existing disk
    @classmethod
    def disk_open(cls,filename= None):
        if filename == None:
            filename = cls.image_name
        try:
            cls.diskimage = open(filename, 'rb+')
            cls.image_name = filename
        except Exception as es:
            print('invalid filename use init_disk to create it')
            print(es)
        

    #Read the whole block and return an array or list of bytes
    @classmethod
    def disk_read(cls,blockNumber,size=blocksize):
        if cls.diskimage == None:
            print('plese open the disk image using disk_open berfore reading')
            return None
        elif (blockNumber >= cls.nbrOfBlocks):
            print('read failed: invalid Block number')
            return None
        else :
            try :
                cls.diskimage.seek(blockNumber*cls.blocksize)
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
        if cls.image_name != None:
            print("Diskimage : ",cls.image_name)
            print("Block size : ",cls.blocksize," Bytes")
            size = os.path.getsize(cls.image_name)
            print("Number Of Blocks : ",cls.nbrOfBlocks)
            print ("Disk Size : ", size, " Bytes")
        else:
            print ("No image file")
        if cls.diskimage != None:
            print("DiskStatus : Open :",cls.image_name)
        else :
             print("DiskStatus : Closed")

    # Forces all outstanding writes to disk and closes the associated image file
    @classmethod
    def disk_close(cls):
        if cls.diskimage != None:
            cls.diskimage.close()
            cls.diskimage = None
        else: 
            print('No Disk image to close')
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