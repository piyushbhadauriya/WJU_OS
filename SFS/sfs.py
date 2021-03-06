import diskpy
import numpy as np
# from blockbitmap import BlockBitMap
# from inodebitmap import NodeBitMap
from bmaps import Bmaps
from direntry import DirEntry
class sfs:
    filename = 'image'
    encoding = 'utf-8'
    INTEGER_SIZE = 'int32'

    disk = diskpy.mydisk()
    # inode
    inode_size = 32
    idx_isvalid = 0 # set 0 for empty inode and 1 for used inode
    idx_size = 1  #  128 Bytes 
    idx_direct = 2 # index of Data Block
    FREE = 0
    FILE = 1
    DIR = 2
    BAD = 99

    #superblock
    superblock_size = 5
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
    
    superblock_BN = 0
    inobeBlock_BN = 3 #3,4,5
    blockbitmap_BN = 1
    nodebitmap_BN = 2
    
    @classmethod
    def init_Superblock(cls):
        sBlock = np.zeros(shape=(cls.superblock_size, 1),dtype=cls.INTEGER_SIZE)
        sBlock[cls.idx_magic] = cls.magic
        sBlock[cls.idx_nblocks] = cls.nblocks
        sBlock[cls.idx_ninodeblocks] = cls.ninodeblocks
        sBlock[cls.idx_ninodes] = cls.ninodes
        sBlock[cls.idx_dentry] = cls.dentry_inode
        cls.disk.disk_open(cls.filename)
        superblock = sBlock.tobytes()
        # write superblock to Block0  
        cls.disk.disk_write(cls.superblock_BN, superblock)
        cls.disk.disk_close()
    
    @classmethod
    def init_inodes(cls):
        cls.disk.disk_open(cls.filename)
        for i in range (cls.ninodeblocks):
            cls.disk.disk_write(cls.inobeBlock_BN+i, bytearray(cls.disk.blocksize))
        cls.disk.disk_close()
        


    # @classmethod
    # def init_blockmap(cls):
    #     cls.bitmap = BlockBitMap(cls.blockbitmap_BN)
    #     cls.bitmap.init()
    #     cls.bitmap.saveToDisk()
    
    # @classmethod
    # def init_nodemap(cls):
    #     cls.nodemap = NodeBitMap(cls.nodebitmap_BN)
    #     cls.nodemap.init()
    #     cls.nodemap.saveToDisk()
    
    @classmethod
    def fs_init(cls,nbrblock):
        cls.nblocks = nbrblock
        cls.disk.disk_init(cls.filename,cls.nblocks)
        print('Disk initiatized with ',cls.nblocks,' Blocks Of Block Size ',cls.disk.blocksize, ' Bytes')

    @classmethod
    def fs_format(cls):
        cls.disk.disk_init(cls.filename,cls.nblocks)
        # set up Superblock
        if cls.disk.filename == None : 
            print('No disk to format.')
            return
        cls.init_Superblock()
        print('Superblock created on block 0')
        #create block Map and inode Map
        Bmaps.init(cls.nblocks,cls.ninodes)
        # create inodes 
        cls.init_inodes()
        print('iNodes created on blocks 3 - 5')
        cls.createinode(cls.dentry_inode,cls.DIR)
        DirEntry.init_dir(cls.dentry_inode,cls.dentry_inode)
        print ('directory structure created')
    
    @classmethod
    def scan_BlockBitMap(cls):
        Bmaps.blockbmap.scan()
    @classmethod
    def scan_NodeBitMap(cls):
        Bmaps.inodebmap.scan()
    @classmethod
    def showDir(cls,d_inode):
        d_block = cls.getBlockno(d_inode)
        DirEntry.showDir(d_block)

    @classmethod
    def fs_mkdir(cls,name,c_inode):
        DirEntry.add_dirname(name,c_inode)
    @classmethod
    def fs_mkfile(cls,name,c_inode):
        DirEntry.add_filename(name,c_inode)
    
    @classmethod
    def getBlockno(cls,d_inode):
        if d_inode > cls.ninodes:
            print('invalid inode ',d_inode)
            return None
        else:
            cls.disk.disk_open()
            block = int(cls.inobeBlock_BN+d_inode/16)
            offset = int(cls.inode_size*(d_inode%16))
            b_array = cls.disk.disk_read(block)[offset:offset+cls.inode_size]
            inode = np.frombuffer(b_array,dtype=cls.INTEGER_SIZE)
            cls.disk.disk_close()
            return inode[cls.idx_direct]
    
    @classmethod
    def getinode(cls,name,c_inode):
        return DirEntry.findDir(name,c_inode)   

    @classmethod
    def createinode(cls,inodeNo,type,dataNode=None,):
        if dataNode == None:
            dataNode = Bmaps.blockbmap.findFree()
        inode = np.zeros(shape=(int(cls.inode_size/4), 1),dtype=cls.INTEGER_SIZE)
        inode[cls.idx_isvalid] = type
        inode[cls.idx_size] = 0
        inode[cls.idx_direct] = dataNode
        if inodeNo > cls.ninodes:
            print('invalid inode ',inodeNo)
            return False
        else:
            cls.disk.disk_open()
            block = int(cls.inobeBlock_BN+inodeNo/16)
            offset = int(cls.inode_size*(inodeNo%16))
            sucess = cls.disk.disk_write(block,inode.tobytes(),offset)
            cls.disk.disk_close()
            return sucess
    
    @classmethod
    def fs_open(cls,filename):
        sucess = cls.disk.disk_open(filename)
        if sucess == True:
            cls.filename = filename
            b_array = cls.disk.disk_read(cls.superblock_BN)[:cls.superblock_size*32]
            superblock = np.frombuffer(b_array,dtype=cls.INTEGER_SIZE)
           # print(superblock)
            cls.nblocks = superblock[cls.idx_nblocks]
            cls.disk.setnbrOfBlocks(cls.nblocks)
           # print (cls.disk.nbrOfBlocks)
            Bmaps.init(None,None)
            cls.disk.disk_open(filename)
        return sucess

        


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
    
    # @classmethod
    # def print_info(cls): # print superblock and inode info
    #     cls.disk.disk_open(cls.filename)
    #     sb = cls.disk.disk_read(cls.superblock_BN)
    #     sbArray = np.frombuffer(sb[:16],dtype=cls.INTEGER_SIZE)
    #     print("==================== Super Block ====================")
    #     print('Blocksize : ', cls.disk.blocksize)
    #     print('Number of Blocks in Disk : ',sbArray[cls.idx_nblocks])
    #     print('Number of inode blocks : ',sbArray[cls.idx_ninodeblocks])
    #     print('Number of inodes : ',sbArray[cls.idx_ninodes])
    #     print(sb)

    #     ind = cls.disk.disk_read(cls.blocki)
    #     inodelist =[]
    #     [inodelist.append(ind[i*cls.inode_size:(i+1)*cls.inode_size]) for i in range(sbArray[cls.idx_ninodes])]
    #     print("==================== inodes ====================")
    #     count = 0
    #     for inode in inodelist:
    #         inodeArray = np.frombuffer(inode,dtype=cls.INTEGER_SIZE)
    #         if inodeArray[cls.idx_isvalid] == 1:
    #             print('inode ',count,' -----> ','Block No ',inodeArray[cls.idx_direct])
    #             print('Size of inode',inodeArray[cls.idx_size])
    #             print(inode)
    #         else: 
    #             print('inode ',count,' : Empty')
    #         count += 1 
    #     cls.disk.disk_close()

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


