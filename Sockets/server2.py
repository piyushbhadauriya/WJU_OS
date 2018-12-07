import socket			 
import os
from threading import Thread

port = 12345

class ClientThread(Thread):

    def __init__(self,ip,port,sock):
        Thread.__init__(self)
        self.ip = ip
        self.port = port
        self.sock = sock
        print( " New thread started for "+ip+":"+str(port))

    def do_something(self, cmdstr):
        # split the string using white space as delimiter
        ss = cmdstr.split()
        cmd = ss[0]
        return cmd, 'response to cmd: ' + cmd + ' is 45'

    def run(self):
        while True:
            aa = self.sock.recv(1024)
            aa_str = aa.decode('utf-8')
            print('received : ', aa_str)
            # expect this form: cmd a1 
        
            cmd, bb = self.do_something(aa_str)
            print('servicing cmd: ',cmd)

            if cmd == 'QUIT':     
                bb = 'Shutdown session'
            elif cmd == 'LIST':
                bblist = os.listdir('.')
                bb = ''
                for a1 in bblist:
                    bb += ' ' + a1 

            print('send response: ',bb)
            bb_bytes = bytes(bb, 'utf-8')
            self.sock.send(bb_bytes)
            if cmd == 'QUIT':
                self.sock.close()
                print('client thread ending')
                break

            
s = socket.socket()		 				
s.bind(('', port))		 
print( "socket binded to %s" %(port) )

# put the socket into listening mode 
s.listen(5)	 
print( "socket is listening")			
threads = [] # keep a list of threads so to do a join()

# wait for multiple clients to connect
while True:
    print('server3 waiting on accept')
    conn, (ip, port)  = s.accept()	# tuple of IP and Port of client
    print ('Got connection from ', ip, 'at port: ', port )
    newthread = ClientThread(ip, port, conn)
    newthread.start()
    threads.append(newthread)
    

for t in threads:
    t.join()
print('server3 is done')
     
    

