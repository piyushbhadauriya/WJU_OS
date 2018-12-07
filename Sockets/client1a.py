# Import socket module 
import socket                
  
# Create a socket object 
s = socket.socket()          
  
# Define the port on which you want to connect 
port = 12345                
  
ahost = '172.31.12.255'
# connect to the server on local computer 
s.connect((ahost, port)) 
s.send(bytes('LIST','utf-8'))
print(s.recv(1024).decode('utf-8'))
s.send(bytes('QUIT','utf-8'))
print(s.recv(1024).decode('utf-8'))
# receive data from the server 
# print(s.recv(1024).decode('utf-8') )
# close the connection 
s.close()        