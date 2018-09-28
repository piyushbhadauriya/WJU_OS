import numpy as np

def save(myarray,start_index):
    # open file 
    with open("out",'r') as f:
        out = ''
        for i in range(start_index):
            line = f.readline()
            if line =='':
                out+='\n'
                continue
            out+=line
        for i in range(len(myarray)):
            out += (str(start_index+i)+':'+str(myarray[i])+'\n')
    with open("out",'w+') as f:
        f.write(out)


def load(index):
     for line in open("out",'r'):
        # print(line)
        if (line.split(':')[0] == str(index)):
            return np.array(eval(line.split(':')[1].strip().replace(' ',',')))
            



memarray = np.zeros(shape=(6,6), dtype = 'int8')
viewa = memarray[0:2]

viewa[0] = 22
viewa[1] = 44
save(viewa,0)

viewb = memarray[2:5]

viewb[0] = load(0)
viewb[1] = load(1)
viewb[2] = 33

print("Content of view-b")
print(viewb)
print("Content of whole memory array")
print(memarray)

'''
# initialize 6X6 memory array
memarray = np.zeros(shape=(6,6), dtype = 'int8')
# Get a view-a of 2x6
viewa = memarray[0:2]
# Change first row to ‘22’ and 2nd to ’44’
viewa[0] = 22
viewa[1] = 44
# Store this view-a in a binary file.
np.save("view-a",viewa)
# Get another view-b of 3x6
viewb = memarray[2:5]
# Restore the binary file into this new view-b
viewb[0:2] = np.load("view-a.npy")
# Change 3rd row to ’33’
viewb[2] = 33
# Print contents of view-b 
print("Content of view-b")
print(viewb)
# Print contents of memarray 
print("Content of whole memory array")
print(memarray)
'''