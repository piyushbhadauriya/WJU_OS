import socket			 
import os
from threading import Thread

listen_port = 1121

class ClientThread(Thread):

    def __init__(self, ip, sock):
        Thread.__init__(self)
        self.client_ip = ip
        self.controlsock = sock
        self.dataport = 12346
        self.datasock = None
        print( " New thread started ")

    def send_status(self, astatus):
        astat_bytes = bytes(astatus,'utf-8')
        self.controlsock.send(astat_bytes)

    def send_data(self, adata):
        adata_bytes = bytes(adata, 'utf-8')
        self.datasock.send(adata_bytes)

    def parse(self, cmdstr):
        # split the string using white space as delimiter
        ss = cmdstr.split()
        arg = ''
        cmd = ss[0]
        if len(ss) > 1:
            arg = ss[1]
        return cmd, arg

    def do_CWD(self, arg):
        try:
            os.chdir(arg)
            status = '200'
        except FileNotFoundError:
            status = '500'
        self.send_status(status)
        

    def do_PORT(self, portNumber_str):
        self.dataport = int(portNumber_str) 
        try:
            self.datasock = socket.socket()    
            self.datasock.connect((self.client_ip, self.dataport)) 
            aa = self.controlsock.recv(100)  # get the OK status
            print('connect dataport status: ', aa.decode('utf-8'))
        except Exception as e:
            self.datasock = None
            print('Error in setting up data port: ',e)  

    def do_LIST(self):
        bb = ''
        with os.scandir('.') as dir:
            for entry in dir:
                if entry.is_dir():
                    sentry = '[' + entry.name + ']'
                else:
                    sentry = entry.name
                bb +=  ' ' + sentry
        self.send_status('200')
        self.send_data(bb)
        

    def run(self):
        print('new client thread started')
        while True:
            try:
                print('waiting on clientthread recv - controlsocket')
                
                aa = self.controlsock.recv(1024)
                aa_str = aa.decode('utf-8')
                print('received : ', aa_str)
                # expect this form: cmd a1 
            
                cmd, arg = self.parse(aa_str)
                print('servicing cmd: ',cmd, ' with arg: ', arg)

                if cmd == 'CWD':
                    self.do_CWD(arg)

                if cmd == 'QUIT':     
                    self.controlsock.close()
                    self.datasock.close()
                    break
                elif cmd == 'LIST':
                    print('in LIST')
                    self.do_LIST()
                elif cmd == 'PORT':
                    self.do_PORT(arg)
                    
            except Exception as e:
                print('Exception caught : ', e)
                break

        print('Exiting thread')
        print('client thread ending')

#
# ===================================================


listen_sock = socket.socket()		 				# default is socket(AF_INET, SOCK_STREAM)
listen_sock.bind(('', listen_port))		 
print( "socket binded to %s" %(listen_port) )

# put the socket into listening mode 
listen_sock.listen(5)	 
print( "listen socket is listening")			
threads = [] # keep a list of threads so to do a join()

# wait for multiple clients to connect
while True:
    print('ftp server waiting on accept')
    try:
        control_sock_client, (client_ip, client_port)  = listen_sock.accept()	# tuple of IP and Port of client
        print ('Got connection from ', client_ip, 'at port: ', client_port )
        newthread = ClientThread(client_ip, control_sock_client)
        newthread.start()
        threads.append(newthread)
    except socket.error as e:
        print("Exception: ", e)
        break
    
        

[t.join() for t in threads]

print('ftpserver is shutting down')
  
    
