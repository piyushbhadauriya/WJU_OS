import diskpy
from bmaps import Bmaps
import sys
import numpy as np
FREE = (0).to_bytes(4,sys.byteorder)
encoding = 'utf-8'



class DirEntry:
    ninodes = 48
    disk = diskpy.mydisk()
    inobeBlock_BN = 3
    INTEGER_SIZE = 'int32'
    # inode
    inode_size = 32
    idx_isvalid = 0 # set 0 for empty inode and 1 for used inode
    idx_size = 1  #  128 Bytes 
    idx_direct = 2 # index of Data Block
    FREE = 0
    FILE = 1
    DIR = 2
    BAD = 99
    
    @classmethod
    def init_dir(cls,childInode,parantInode):
        block_nbr = cls.getBlockno(childInode)
        child_dir = bytearray(32)
        child_dir[0:4] = childInode.to_bytes(4,sys.byteorder)
        child_dir[4:32] = bytearray('d_.',encoding)
        parant_dir = bytearray(32)
        parant_dir[0:4] = parantInode.to_bytes(4,sys.byteorder)
        parant_dir[4:32] = bytearray('d_..',encoding)
        cls.disk.disk_open()
        cls.disk.disk_write(block_nbr,child_dir,0)
        cls.disk.disk_write(block_nbr,parant_dir,32)
        cls.disk.disk_close()
                
    @classmethod
    def add_dirname(cls,name,c_inode):
        inodeNo = Bmaps.inodebmap.findFree()
        cls.createinode(inodeNo,cls.DIR)
        cls.init_dir(inodeNo,c_inode)
        block_nbr = cls.getBlockno(c_inode)
        cls.disk.disk_open() 
        arr = bytearray(cls.disk.disk_read(block_nbr))
        cls.disk.disk_close()
        print('Creating Directry : ',name, end="", flush=True)
        for offset in range(0,16):
            if arr[offset*32:offset*32+4] == FREE:
                entry = bytearray(32)
                entry[0:4] = inodeNo.to_bytes(4,sys.byteorder)
                entry[4:32] = bytearray('d_'+name,encoding)
                arr[offset*32:(offset+1)*32] = entry
                cls.disk.disk_open()
                cls.disk.disk_write(block_nbr,arr)
                cls.disk.disk_close()
                return True
        return False
        
    @classmethod
    def add_filename(cls,name,c_inode):
        inodeNo = Bmaps.inodebmap.findFree()
        cls.createinode(inodeNo,cls.FILE)
        block_nbr = cls.getBlockno(c_inode)
        cls.disk.disk_open() 
        arr = bytearray(cls.disk.disk_read(block_nbr))
        cls.disk.disk_close()
        print('Creating File : ',name, end="", flush=True)
        for offset in range(0,16):
            if arr[offset*32:offset*32+4] == FREE:
                entry = bytearray(32)
                entry[0:4] = inodeNo.to_bytes(4,sys.byteorder)
                entry[4:32] = bytearray('f_'+name,encoding)
                arr[offset*32:(offset+1)*32] = entry
                cls.disk.disk_open()
                cls.disk.disk_write(block_nbr,arr)
                cls.disk.disk_close()
                return True
        return False
    
    @classmethod
    def set_block(cls,block_nbr):
        cls.block_nbr = block_nbr

    @classmethod
    def showDir(cls,d_block):
        cls.disk.disk_open()
        arr = cls.disk.disk_read(d_block)
        for offset in range(0,16):
            if arr[offset*32:offset*32+4] != FREE:
                entry = arr[offset*32:(offset+1)*32]
                inode = int.from_bytes(entry[:4],sys.byteorder)
                name = entry[4:].decode(encoding)
                print (name)

    @classmethod
    def changeDir(cls,dir_name,c_inode):
        d_block = cls.getBlockno(c_inode)
        cls.disk.disk_open()
        arr = cls.disk.disk_read(d_block)
        for offset in range(0,16):
            if arr[offset*32:offset*32+4] != FREE:
                entry = arr[offset*32:(offset+1)*32]
                inode = int.from_bytes(entry[:4],sys.byteorder)
                name = entry[4:].decode(encoding)
                if name == dir_name:
                    return inode
        print("Directry [",dir_name,"] Not Found" )
    
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
    def findDir(cls,dir_name,c_inode):
        d_block = cls.getBlockno(c_inode)
        cls.disk.disk_open()
        arr = cls.disk.disk_read(d_block)
        for offset in range(0,16):
            if arr[offset*32:offset*32+4] != FREE:
                entry = arr[offset*32:(offset+1)*32]
                inodeNo = int.from_bytes(entry[:4],sys.byteorder)
                name = entry[4:].decode(encoding)
                if name[:2] != 'd_':
                    pass
                name = name.lstrip('d_').split('\x00',1)[0]
                if name==dir_name:
                    return inodeNo
        return None
            