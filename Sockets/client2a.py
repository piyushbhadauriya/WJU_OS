# Import socket module 
import socket                
  
def sendCmd(socket, astr):
    str_bytes = bytes(astr,'utf-8')
    print('waiting to send',astr)
    socket.send(str_bytes)

    # receive data from the server 
    answer =  socket.recv(1024).decode('utf-8') 
    print('server response: ', answer)

def store(s,filename):
    chunklist= []          # list of chunks
    counter = 1
    while True:
        s.send('ready'.encode())
        chunk = s.recv(1024).decode('utf-8')
        print('######## Chunk : ',counter," received") 
        counter += 1
        if chunk == 'end of file':
            print (chunk,' received')
            break
        chunklist.append(chunk)
    # finally reassemble the message
    message = ''.join(chunklist) 
    with open(filename,'w+') as f:
        f.write(message)
        print('Written to file',filename)

# Create a socket object 
s = socket.socket()          
  
# Define the port on which you want to connect 
port = 12345                
  
# connect to the server on local computer 
s.connect(('127.0.0.1', port)) 

sendCmd(s, 'LIST')
sendCmd(s, 'RETR test.txt')
store(s,'newfile.txt')
#sendCmd(s, 'STOR thisfile.bin')
sendCmd(s, 'SYSTEM')
sendCmd(s, 'QUIT')

# close the connection 
s.close()        