from cmd import Cmd

myc = None

class MyPrompt(Cmd):

    def parse_args(self, args):
        if len(args) == 0:
            nn = None
            nnlen = 0
        else:
            nn = args.split()
            nnlen = len(nn)
        return nn,nnlen

    def do_connect(self, args):
        """connect to ftp server. connect <ip> <port>"""
        # default parameters
        global myc
        port = 1121
        ip = '127.0.0.1'

        # print('args: ',args)
        nn, nnlen = self.parse_args(args)
        if nnlen > 0:
            ip = nn[0]
            if nnlen == 2:
                port = int(nn[1])  # not many error checking
        
        myc = MyConnection(ip, port)
        if myc.connect():
            print ("Connection to ", ip, ':', port, ' SUCCESSFUL')
        else:
            print("Connection failure")

    def do_ls(self, args):
        """ls - list the contents of current directory: ls """
        global myc
        results = myc.send_cmd('LIST')
        # figure how to display results


    def do_quit(self, args):
        """Quits the program."""
        print ("Quitting.")
        raise SystemExit

import socket
OK = '200'
OK_bytes = bytes(OK,'utf-8')

class MyConnection():

    def __init__(self, ip, port):
        self.controlsocket = None
        self.datasocket = None
        self.ip = ip
        self.controlport = port
        self.dataport = 12345
        self.listensocket = None

    def send_cmd(self, command):
        aline_bytes = bytes(command, 'utf-8')
         
        self.controlsocket.send(aline_bytes)

        # not a good way 
        status = self.controlsocket.recv(100)
        print('control response : ', status.decode('utf-8'))
        # should check for status but for now ignore
        results = self.datasocket.recv(1024)  # clearly I should be getting the whole thing with 
                                            # multiple recv
        print('data results: ', results.decode('utf-8'))
        return results

    def connect(self):
        self.controlsocket = socket.socket()
        self.controlsocket.connect((self.ip, self.controlport))

        # set up the data port
        self.listensocket = socket.socket()
        self.listensocket.bind(('', self.dataport))
        self.listensocket.listen(1)

        port_cmd = 'PORT ' +  str(self.dataport)
        self.controlsocket.send(bytes(port_cmd,'utf-8'))

        self.datasocket, (ipd, portx) = self.listensocket.accept()

        print('accept connection from ',ipd, ' at port ', portx)

        self.controlsocket.send(OK_bytes)

        return True



if __name__ == '__main__':
    prompt = MyPrompt()
    prompt.prompt = 'ftp> '
    prompt.cmdloop('Starting ftp client ...')