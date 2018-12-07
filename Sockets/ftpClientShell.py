from cmd import Cmd
import socket			 
import os
from threading import Thread
import datetime
import traceback
myconn = None
class clientShell(Cmd):

    def do_connect(self,s):
        """ Connect to ftp server Syntex: 'connect server [port = 1121]' """
        global myconn
        if myconn != None:
            print('alreays connected to ftpserver. use bye to disconnect before connecting again')
            return
        #args = self.parse_args(s)
        args = s.split()
        if len(args) == 0:
            print ("*** enter the ftpserver address to connect")
            return
        elif len(args) == 1:
            port = 1121
            server =  args[0]
        elif len(args) >= 2:
            try:
                server =  args[0]
                port = int(args[1])
            except:
                print("invalid port no",port)
                return
        try:
            myconn = MyConnection(server, port)
            myconn.connect()
            print ("Connection to ", server, ':', port, ' SUCCESSFUL')
        except Exception as e:
            print ("*** Failed to connect", server,':',port)
            print(e)
    
    def do_ls(self, s):
        """ls - list the contents of current REMOTE directory"""
        #global myconn
        if myconn == None:
            print('No Connection found, connect to the server first')
            return
        results = myconn.sendCmd('LIST')
        for result in results.split():
            print(result)    

    def do_get(self, s):
        """get a file from the ftp server"""
        #global myconn
        if myconn == None:
            print('No Connection found, connect to the server first')
            return
        myconn.receiveFile('RETR '+s.split()[0])

    def do_bye(self, s):
        """Close the connection"""
        global myconn
        if myconn == None:
            print('No Connection to close')
            return
        myconn.sendCmd('QUIT')
        myconn.disconnect()
        myconn = None
        print ("connection closed")
    
    def do_exit(self, s):
        """Quits the program."""
        global myconn
        if myconn != None:
            myconn.sendCmd('QUIT')
            myconn.disconnect()
            myconn = None
            print ("Connection closed")
        print ("Quitting.")
        raise SystemExit

    def do_cd(self, s):
        """Change working REMOTE directory"""
        if myconn == None:
            print('No Connection found, connect to the server first')
            return
        results = myconn.sendCmd('CWD '+s.strip())
        if results == None:
            print('Location not found')
    
    def do_pwd(self, s):
        """print REMOTE directory"""
        #global myconn
        if myconn == None:
            print('No Connection found, connect to the server first')
            return
        result = myconn.sendCmd('PWD')
        print(result)
    
    def do_system(self, s):
        """show remote system type"""
        #global myconn
        if myconn == None:
            print('No Connection found, connect to the server first')
            return
        results = myconn.sendCmd('SYST')
        for result in results.split('(')[1].split(','):
            print(result.strip())

    def do_lcd(self, s):
        """Change working LOCAL directory"""
        try:
            os.chdir(s.strip())    
        except:
            print("Directry not found")
        print("current local directory",os.getcwd())
    
    def do_lls(self, s):
        """list the contents of current LOCAL directory"""
        with os.scandir('.') as dir:
            for entry in dir:
                if entry.is_dir():
                    print('[' , entry.name , ']')
                else:
                    print(entry.name)
        #print("current local directory",os.getcwd())
    
    def do_put(self, s):
        """Send a file to remote directory"""
        #global myconn
        if myconn == None:
            print('No Connection found, connect to the server first')
            return
        myconn.sendFile(s.split()[0])

OK = '200'
OK_bytes = bytes(OK,'utf-8')

class MyConnection():
    def __init__(self, server, port):
        self.server = server
        self.cport = port
        self.CSocket =  None
        self.listenport = 12345
        self.LSocket = None
        self.Dsocket = None

    def connect(self):
        self.CSocket = socket.socket()
        self.CSocket.connect((self.server, self.cport))
        # setup listen Port
        self.LSocket = socket.socket()
        self.LSocket.bind(("127.0.0.1",self.listenport))
        self.LSocket.listen(1)
        cmd = "PORT 12345"
        self.CSocket.send(cmd.encode())
        #status = self.CSocket.recv(1024)
        self.Dsocket,(ip, port)  = self.LSocket.accept()
        print ('Got connection from ', ip, 'at port: ', port)
        self.CSocket.send(OK_bytes)
        return True
    
    def disconnect(self):
        self.CSocket.close()
        self.LSocket.close()
        self.Dsocket.close()
        self.LSocket = None
        self.Dsocket = None
        return True
    
    def sendCmd(self, astr):
        str_bytes = bytes(astr,'utf-8')
        self.CSocket.send(str_bytes)
        # receive data from the server 
        status =  self.CSocket.recv(1024).decode('utf-8') 
        print('Server response: ', status)
        result = ''
        if status == '200':
            while True:
                try:
                    self.Dsocket.settimeout(1)
                    chunk = self.Dsocket.recv(1024)   # read some chunk
                    if chunk == b'' or not chunk:
                        print('zero length recv') 
                        self.Dsocket.settimeout(0)
                        self.Dsocket.setblocking(True)
                        break
                    else:
                        result += chunk.decode()
                except:
                    #print("Exception: ", e)
                    self.Dsocket.settimeout(0)
                    self.Dsocket.setblocking(True)
                    break
            return result
        else:
            return None

    def receiveFile(self, cmds):
        str_bytes = bytes(cmds,'utf-8')
        self.CSocket.send(str_bytes)
        # receive data from the server 
        status =  self.CSocket.recv(1024).decode('utf-8') 
        print('server response: ', status)
        if status == '200':
            with open('retrfile.txt','w') as fd:
                x = datetime.datetime.now()
                fd.write(x.strftime("%c"))
                fd.write('\n')
                while True:
                    try:
                        self.Dsocket.settimeout(2)
                        chunk = self.Dsocket.recv(1024)   # read some chunk
                        print('recv file line: ', chunk)
                        if chunk == b'' or not chunk:
                            print('zero length recv')
                            self.Dsocket.settimeout(0)
                            self.Dsocket.setblocking(True)
                            break
                        else:
                            fd.write(chunk.decode('utf-8'))
                    except Exception as e:
                        #print("Exception: ", e)
                        self.Dsocket.settimeout(0)
                        self.Dsocket.setblocking(True)
                        break
            print('Done')

    def sendFile(self, filename):
        if not(os.path.isfile(filename)):
            print("file not found")
            return False 
        cmd = "STOR "+filename
        self.CSocket.send(cmd.encode())
        status = self.CSocket.recv(1024).decode('utf-8')
        print('server response: ', status)
        if status != '200':
            print ("server returned :", status)
            return False
        try:
            with open(filename, 'r') as fd:
                for aline in fd:
                    self.Dsocket.send(aline.encode())
            return True
        except Exception as e:  #file not found
            print(e)
            traceback.print_exc()
            return False               

if __name__ == '__main__':
    prompt = clientShell()
    prompt.prompt = '> '
    prompt.cmdloop('Starting Client Shell...')