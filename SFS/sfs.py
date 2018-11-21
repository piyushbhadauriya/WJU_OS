import diskpy
import numpy as np
from blockbitmap import BlockBitMap
class sfs:
    filename = 'image_512.20'
    encoding = 'utf-8'
    INTEGER_SIZE = 'int32'

    disk = diskpy.mydisk()
    bitmap = None
    inodemap = None
    # inode
    blocki = 3 # inode start block
    inode_size = 32
    idx_isvalid = 0 # set 0 for empty inode and 1 for used inode
    idx_size = 1  #  128 Bytes 
    idx_direct = 2 # index of Data Block

    #superblock
    block0 = 0
    magic = 12345
    nblocks = 64 
    ninodeblocks = 3
    ninodes = int((disk.blocksize*ninodeblocks)/inode_size) #48
    dentry_inode = 1 
    idx_magic = 0
    idx_nblocks = 1
    idx_ninodeblocks = 2
    idx_ninodes = 3
    idx_dentry = 4 # directroy inode
    
    @classmethod
    def init_Superblock(cls):
        sBlock = np.zeros(shape=(4, 1),dtype=cls.INTEGER_SIZE)
        sBlock[cls.idx_magic] = cls.magic
        sBlock[cls.idx_nblocks] = cls.nblocks
        sBlock[cls.idx_ninodeblocks] = cls.ninodeblocks
        sBlock[cls.idx_ninodes] = cls.ninodes
        cls.disk.disk_open(cls.filename)
        superblock = sBlock.tobytes()
        # write superblock to Block0  
        cls.disk.disk_write(cls.block0, superblock)
        cls.disk.disk_close()
    
    @classmethod
    def init_inodes(cls):
        cls.disk.disk_open(cls.filename)
        for i in range (cls.ninodeblocks):
            freeblock = cls.bitmap.findFree()
            cls.disk.disk_write(freeblock, bytearray(cls.disk.blocksize))
        cls.disk.disk_close()
    @classmethod
    def fs_format(cls):
        cls.disk.disk_init(cls.filename,cls.nblocks)
        # set up Superblock
        cls.init_Superblock()
        # create bitmap 
        cls.bitmap = BlockBitMap(512,1)
        # create inodes 
        cls.init_inodes()
        
        # to-do: create inodemap

        
        

    # @classmethod
    # def fs_write(cls,inumber,data): # write to a inode
    #     # create and write a inode
    #     # write data to Block no in inode[idx_direct]
    #     inode = np.zeros(shape=(int(cls.inode_size/4), 1),dtype=cls.INTEGER_SIZE)
    #     inode[cls.idx_isvalid] = 1
    #     inode[cls.idx_size] = len(data) 
    #     inode[cls.idx_direct] = int(inumber+2) # hard coded inode --> Data block mapping, need block bitmap to find freeblock
    #     offset = int(32*inumber)
    #     if offset > cls.disk.blocksize*cls.ninodeblocks:
    #         print('invalid inode ',inumber)
    #         return False
    #     else:
    #         cls.disk.disk_open(cls.filename)
    #         sucess = cls.disk.disk_write(cls.blocki,inode.tobytes(),offset)
    #         sucess = sucess and cls.disk.disk_write(inode[cls.idx_direct],data)
    #         cls.disk.disk_close()
    #         if sucess:
    #             return True
    #         else:
    #             return False
    # @classmethod    
    # def fs_read(cls,inumber): # read data from the inode
    #     # go to inode inumber
    #     # read from Block no in inode[idx_direct]
    #     offset = int(cls.inode_size*inumber)
    #     if offset > cls.disk.blocksize*cls.ninodeblocks:
    #         print('invalid inode ',inumber)
    #         return False
    #     else:
    #         cls.disk.disk_open(cls.filename)
    #         aa = cls.disk.disk_read(cls.blocki)
    #         ia = aa[offset:offset+cls.inode_size]
    #         inode = np.frombuffer(ia,dtype=cls.INTEGER_SIZE)
    #         data = cls.disk.disk_read(inode[cls.idx_direct])
    #         cls.disk.disk_close()
    #         return data[:inode[cls.idx_size]]
    
    @classmethod
    def print_info(cls): # print superblock and inode info
        cls.disk.disk_open(cls.filename)
        sb = cls.disk.disk_read(cls.block0)
        sbArray = np.frombuffer(sb[:16],dtype=cls.INTEGER_SIZE)
        print("==================== Super Block ====================")
        print('Blocksize : ', cls.disk.blocksize)
        print('Number of Blocks in Disk : ',sbArray[cls.idx_nblocks])
        print('Number of inode blocks : ',sbArray[cls.idx_ninodeblocks])
        print('Number of inodes : ',sbArray[cls.idx_ninodes])
        print(sb)

        ind = cls.disk.disk_read(cls.blocki)
        inodelist =[]
        [inodelist.append(ind[i*cls.inode_size:(i+1)*cls.inode_size]) for i in range(sbArray[cls.idx_ninodes])]
        print("==================== inodes ====================")
        count = 0
        for inode in inodelist:
            inodeArray = np.frombuffer(inode,dtype=cls.INTEGER_SIZE)
            if inodeArray[cls.idx_isvalid] == 1:
                print('inode ',count,' -----> ','Block No ',inodeArray[cls.idx_direct])
                print('Size of inode',inodeArray[cls.idx_size])
                print(inode)
            else: 
                print('inode ',count,' : Empty')
            count += 1 
        cls.disk.disk_close()

# sfs.fs_format()
# print("----------- Writing strings and integer to Disk--------------------")
# # mystring = "hello"*250
# # if fs_write(0,mystring.encode(encoding)) == False:
# #     print ('##########Error: Fail to write###########')
# mystring = "hello "*20
# if sfs.fs_write(0,mystring.encode(sfs.encoding)) == True:
#     print ('Write string "hello"X20 to inode 0')
# mystring = "This is a Simple file system"
# sfs.fs_write(1,mystring.encode(sfs.encoding))
# print ('Write string "This is simple file System" to inode 1')
# mynumber = 1234
# sfs.fs_write(2,mynumber.to_bytes(4, byteorder='little'))
# print ('Write number 1234 to inode 2')
# sfs.print_info()

# print("######## Read from file and Print #######")
# data = sfs.fs_read(0)
# data1 = sfs.fs_read(1)
# print('Inode 0 --> Mystring 1 :',data.decode())
# print('Inode 1 --> Mystring 2 :',data1.decode())
# data2 = sfs.fs_read(2)
# print(data2)
# print('Inode 2 --> MyInt : ',int.from_bytes(data2, byteorder='little'))


