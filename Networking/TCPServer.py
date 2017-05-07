import socketserver
import threading
import socket
try:
    from Networking.StoppableThread import StoppableThread
except:
    import StoppableThread.StoppableThread as StoppableThread
    
def CreateServer(target, port, onRecvMessage):    
    server = ThreadedServer(target, port, onRecvMessage)
    print('hmm')
    server.start()
    
    return server
    
class ThreadedServer(StoppableThread):
    def __init__(self, target, port, onRecvMessage, *args):
        self.target = target
        self.port = port
        self.onRecvMessage = onRecvMessage
        threading.Thread.__init__(self)    
 
    def run(self):        
        server = socketserver.ThreadingTCPServer((self.target, self.port), MyTCPHandler)
        server.onRecvMessage = self.onRecvMessage
        print (self.isAlive())
        server.serverThreadAlive = self.isAlive
        server.serve_forever()
        
class MyTCPHandler(socketserver.BaseRequestHandler):    
        
    def setup(self):
        # turn off nagles
        self.request.setsockopt(socket.IPPROTO_TCP,
                                   socket.TCP_NODELAY, True)
    def handle(self):                
        while self.server.serverThreadAlive():                       
            data = self.request.recv(1024)    
                
            if not data:
                break  # disconnection 
            
            data = data.decode("utf-8") #change from array of bytes to utf8 string
            if data[0] != '\x00':
                continue
            if data[len(data) - 1] != '\x00':
                continue    
            
            data = data[1:len(data)-1]
            messages = data.split('\x00')
                        
            #only send latest message in case we received multiple
            self.server.onRecvMessage(messages[len(messages)-1])
        
        print ("done handling!")

if __name__ == "__main__":
    CreateServer('localhost', 9999, print)
    
