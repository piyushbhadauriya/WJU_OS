class MyNode:
    ''' Node of a Binory tree'''
    def __init__(self,data):
        self.data = data
        self.left = None
        self.right = None



root = MyNode(10)
root.left = MyNode(5)
root.right = MyNode(15)
#root.left.left = MyNode(0)
#root.left.left.left = MyNode(0)
root.right.right = MyNode(20)
hight = [0]
#root.left.right = MyNode(10)

def isbalanced(root,hight):
    if root == None:
        return True
    lh = [0]
    rh = [0]
    l = isbalanced(root.left,lh)
    r = isbalanced(root.right,rh)
    hight[0] = lh[0]+1 if lh[0] > rh[0] else rh[0]+1
    if abs(lh[0]-rh[0]) >=2:
        return False
    else:
        return l and r

print (isbalanced(root,hight))

    