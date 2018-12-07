import socket			 
import os
from threading import Thread

cport = 12345

class NewClientThread(Thread):

    def __init__(self,ip,port,ds):
        Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.cs = cs
        self.ds = ds
        print( " New thread started for "+ip+":"+str(port))

    def run(self):
        ds.connect((self.ip, self.port))
        #cs.connect((self.ip,cport))
        ds.send(bytes('connect', 'utf-8'))
        while True:
            data = ds.recv(1024).decode('utf-8')
            print('received : ', data)
            result =  'A B C D'
            ds.send(bytes(result, 'utf-8'))
            ds.send(bytes('OK', 'utf-8'))

            
cs = socket.socket()
ds = socket.socket()	 				
cs.bind(('', cport))		 
print( "socket binded to %s" %(cport) )

# put the socket into listening mode 
cs.listen(5)	 
print( "socket is listening")			
threads = [] # keep a list of threads so to do a join()

# wait for multiple clients to connect
while True:
    print('server3 waiting on accept')
    conn, (ip, port)  = cs.accept()	# tuple of IP and Port of client
    print ('Got connection from ', ip, 'at port: ', port )
    aa = conn.recv(1024)
    aa_str = aa.decode('utf-8')
    print('received : ', aa_str)
    cmds = aa_str.split()
    dport = cmds[1]
    #conn.send(bytes('connected', 'utf-8'))
    newthread = NewClientThread(ip, int(dport), ds)
    newthread.start()
    threads.append(newthread)
    
for t in threads:
    t.join()
print('server3 is done')
     
    
