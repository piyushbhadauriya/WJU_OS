# Import socket module 
import socket                
  
def sendCmd(socket, astr):
    str_bytes = bytes(astr,'utf-8')
    socket.send(str_bytes)

    # receive data from the server 
    answer =  socket.recv(1024).decode('utf-8') 
    print('server response: ', answer)

# Create a socket object 
s = socket.socket()          
  
# Define the port on which you want to connect 
port = 12345                
  
# connect to the server on local computer 
s.connect(('127.0.0.1', port)) 

sendCmd(s, 'LIST')
sendCmd(s, 'RETR somfile.txt' )
sendCmd(s, 'STOR thisfile.bin')
sendCmd(s, 'SYSTEM')
sendCmd(s, 'QUIT')

# close the connection 
s.close()        