from bmaps import Bmaps
from direntry import DirEntry

def createDirectoryStructure(): 
    direntry_block = Bmaps.blockbmap.findFree()
    print('Found free block',direntry_block)
    DirEntry.set_block(direntry_block)
    DirEntry.add_dirname('.',0)
    DirEntry.add_dirname('..',0)
    DirEntry.add_dirname('etc')
    DirEntry.add_dirname('bin')
    DirEntry.add_filename('abcd')