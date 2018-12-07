# first of all import the socket library 
import socket			 

# next create a socket object 
s = socket.socket()		 
print( "Socket successfully created")

# reserve a port on your computer in our 
# case it is 12345 but it can be anything 
port = 12345				

# Next bind to the port 
# we have not typed any ip in the ip field 
# instead we have inputted an empty string 
# this makes the server listen to requests 
# coming from other computers on the network 
s.bind(('', port))		 
print( "socket binded to %s" %(port) )

# put the socket into listening mode 
s.listen(5)	 
print( "socket is listening")			

# a forever loop until we interrupt it or 
# an error occurs 
counter = 0
while True: 

    # Establish connection with client. 
    counter += 1
    c, addr = s.accept()	 
    print ('Got connection from [', counter, '] ',addr )

    # send a thank you message to the client. 
    # myname = socket.gethostname()
    # myIP = socket.gethostbyname('localhost')
    # str = myname + '[' + myIP + '] : Thank you for connecting'
    # m = c.recv(1024)
    # ms = m.decode('utf-8')
    # d = ms.split()
    # if d[0] == 'LIST':
    #     c.send(bytes("List recieved",'utf-8'))

    # ms = c.recv(1024).decode('utf-8')
    # d = ms.split()
    # if d[0] == 'QUIT':
    #     c.send(bytes("Quit recieved",'utf-8'))
    reply(c)
    reply(c)
    c.close()
    # Close the connection with the client 
def reply(c):
    ms = c.recv(1024).decode('utf-8')
    d = ms.split()
    if d[0] == 'QUIT':
        c.send(bytes("Quit recieved",'utf-8'))
    elif d[0] == 'LIST':
        c.send(bytes("List recieved",'utf-8'))

    