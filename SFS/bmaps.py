from blockbitmap import BlockBitMap
from inodebitmap import NodeBitMap
blockbitmap_BN = 1
nodebitmap_BN = 2

class Bmaps:
    blockbmap = None
    inodebmap = None

    @classmethod
    def init(cls,numBloks,numInodes):
        if numBloks != None:
            print('Block bitmap created on block 1')
        cls.blockbmap = BlockBitMap(blockbitmap_BN,numBloks)
        if numInodes != None:
            print('iNode bitmap created on block 2')
        cls.inodebmap = NodeBitMap(nodebitmap_BN,numInodes)
    
        