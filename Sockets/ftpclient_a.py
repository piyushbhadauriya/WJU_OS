# Import socket module 
import socket                
ip = '127.0.0.1'
def sendCmd(socket, astr):
    str_bytes = bytes(astr,'utf-8')
    socket.send(str_bytes)

    # receive data from the server 
    answer =  socket.recv(1024).decode('utf-8') 
    print('server response: ', answer)

# Create a socket object 
cs = socket.socket()          
ls = socket.socket()  
# Define the port on which you want to connect 
cport = 12345                
dport =  12346
# connect to the server on local computer 

ls.bind(('', dport))
ls.listen(1)

cs.connect((ip, cport)) 
sendCmd(cs, 'PORT 12346')
ds, (ip, port)  = ls.accept()
data = ds.recv(1024).decode('utf-8')
print(data)
sendCmd(cs,'LIST')
data = ds.recv(1024).decode('utf-8')
print(data)
# sendCmd(s, 'RETR somfile.txt' )
# sendCmd(s, 'STOR thisfile.bin')
# sendCmd(s, 'SYSTEM')
# sendCmd(s, 'QUIT')