import socket			 
import os
from platform import uname
from threading import Thread
import datetime

listen_port = 21

class ClientThread(Thread):

    def __init__(self, ip, sock):
        Thread.__init__(self)
        self.client_ip = ip
        self.controlsock = sock
        self.dataport = 12346
        self.datasock = None
        print( " New thread started ")

    def parse(self, cmdstr):
        # split the string using white space as delimiter
        ss = cmdstr.split()
        arg = ''
        cmd = ss[0]
        if len(ss) > 1:
            arg = ss[1]
        return cmd, arg
    
    def send_status(self, astatus):
        print ('Return status: ',astatus)
        astat_bytes = bytes(astatus,'utf-8')
        self.controlsock.send(astat_bytes)

    def send_data(self, adata):
        if self.datasock != None:
            adata_bytes = bytes(adata, 'utf-8')
            self.datasock.send(adata_bytes)
            return True
        else:
            return False
    
    def do_CWD(self, location):
        try:
            os.chdir(location)
            self.send_status('200') 
            return True
        except FileNotFoundError:
            self.send_status('500')
            return False

    def do_STOR(self):
        with open('storfile.txt','w') as fd:
            x = datetime.datetime.now()
            fd.write(x.strftime("%c"))
            fd.write('\n')
            self.send_status('200')
            while True:
                try:
                    self.datasock.settimeout(2)
                    chunk = self.datasock.recv(1024)   # read some chunk
                    print('recv file line: ', chunk)
                    if chunk == b'' or not chunk:
                        print('zero length recv')
                        self.datasock.settimeout(0)
                        self.datasock.setblocking(True)
                        break
                    else:
                        fd.write(chunk.decode('utf-8'))
                except Exception as e:
                    #print("Exception: ", e)
                    self.datasock.settimeout(0)
                    self.datasock.setblocking(True)
                    break
        print('Done')    
    
    def do_RETR(self,filename):
        try:
            with open(filename, 'r') as fd:
                for aline in fd:
                    self.send_data(aline)
            self.send_status('200')
            return True
        except Exception as e:
            print(e)
            self.send_status('500') #file not found
            return False

    def setupDataPort(self, portNumber_str):
        self.dataport = int(portNumber_str) # portNumber is a string
        try:
            self.datasock = socket.socket()    
            self.datasock.connect((self.client_ip, self.dataport)) 
            aa = self.controlsock.recv(100)  # get the OK status
            print('connect dataport status: ', aa.decode('utf-8'))
            return True
        except Exception as e:
            print('Error in setting up data port: ',e)
            return False

    def do_LIST(self):
        bb = ''
        with os.scandir('.') as dir:
            for entry in dir:
                if entry.is_dir():
                    sentry = '[' + entry.name + ']'
                else:
                    sentry = entry.name
                bb +=  ' ' + sentry
        if self.send_data(bb) == True:
            self.send_status('200')
        else:
            self.send_status('500')
    
    def do_PWD(self):
        wd = os.getcwd()
        if self.send_data(wd) == True:
            self.send_status('200')
        else:
            self.send_status('500')
    
    def do_SYST(self):
        syst = uname()
        if self.send_data(str(syst)) == True:
            self.send_status('200')
        else:
            self.send_status('500')   
        
    def run(self):
        #print('new client thread started')
        while True:
            print('waiting on clientthread recv - controlsocket')
            aa = self.controlsock.recv(1024)
            aa_str = aa.decode('utf-8')
            print('received : ', aa_str)
            # expect this form: cmd a1 
        
            cmd, arg = self.parse(aa_str)
            print('servicing cmd: ',cmd, ' with arg: ', arg)

            if cmd == 'QUIT':
                self.send_status('200')
                self.controlsock.close()
                self.datasock.close()
                print('client thread ending')
                break
            elif cmd == 'LIST':
                self.do_LIST()
            elif cmd == 'PORT':
                self.setupDataPort(arg)
            elif cmd == 'RETR':
                if not self.do_RETR(arg):
                    print('File ',arg, ' not found')
            elif cmd == 'CWD':
                if not self.do_CWD(arg):
                    print('Location ',arg, ' not found')
            elif cmd == 'STOR':
                self.do_STOR()
            elif cmd == 'PWD':
                self.do_PWD()
            elif cmd == 'SYST':
                self.do_SYST()
            
            


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

print('server3 is done')
