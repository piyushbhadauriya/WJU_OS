class Node: 
    ''' Node of a linked List'''
    def __init__(self,data):
        self.data = data
        self.next = None

    def addbefore(self,data):
        new = Node(data)
        new.next = self
        return new

head = Node(10)
head = head.addbefore(20)
head = head.addbefore(30)
head = head.addbefore(40)
head = head.addbefore(50)
head = head.addbefore(60)
head = head.addbefore(70)
def reverse(head):
    prev = nex = None
    current = head
    while current != None:
        nex = current.next
        current.next = prev
        prev = current
        current = nex
    return prev

def printll(pt):
    while pt!= None:
        print(pt.data,end='->')
        pt = pt.next
    print('')
print('Linked List ',end=':')
printll(head)
rev = reverse(head)
print('Reversed List ',end=':')
printll(rev)

def BlockRevUtil(head,k):
    current = head
    prev = None
    for i in range(0,k):
        if current != None:
            nex = current.next
            current.next = prev
            prev = current
            current = nex
    if (current != None):
        head.next = BlockRevUtil(current,k)
    return prev

print('Block 3 Reversed List ',end=':')
kRev = BlockRevUtil(head,3)
printll(rev)