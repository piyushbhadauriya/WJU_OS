# Import socket module 
import socket                
  
# Create a socket object 
s = socket.socket()          
  
# Define the port on which you want to connect 
port = 12345                
  
ahost = '127.0.0.1'
# connect to the server on local computer 
s.connect((ahost, port)) 
  
# receive data from the server 
print( s.recv(1024).decode('utf-8') )
# close the connection 
s.close()        