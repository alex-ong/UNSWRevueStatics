import socketserver
import threading
import socket
try:
    from Networking.StoppableThread import StoppableThread
except:
    import StoppableThread.StoppableThread as StoppableThread

START_TOKEN = '\x00'    
END_TOKEN = '\x01'
def CreateServer(target, port, onRecvMessage):    
    server = ThreadedServer(target, port, onRecvMessage)    
    server.start()
    print('TCP server started')
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
        
        server.serverThreadAlive = self.isAlive
        server.serve_forever()
        
class MyTCPHandler(socketserver.BaseRequestHandler):    
        
    def setup(self):
        # turn off nagles
        self.request.setsockopt(socket.IPPROTO_TCP,
                                   socket.TCP_NODELAY, True)
    def handle(self):                
        # todo: proper packet segmentation.
        # find \x00's and split on them.
        # make sure we always start with \x00, otherwise discard packet
        dataBuffer = ''
        while self.server.serverThreadAlive():                       
            data = self.request.recv(10)    
                
            if not data:
                break  # disconnection 
            
            data = data.decode("utf-8")  # change from array of bytes to utf8 string
            dataBuffer += data
            while END_TOKEN in dataBuffer:
                endIndex = dataBuffer.index(END_TOKEN)
                # check for buffer index of start...
                try:
                    startIndex = dataBuffer.index(START_TOKEN)
                except:  # malformed packet
                    print ("TCPServerRecv: Malformed packet, no start_token")
                    self.dataBuffer = self.dataBuffer[endIndex + 1:]
                    continue
                
                if startIndex > endIndex:  # malformed packet. Delete everyting including endIndex
                    dataBuffer = self.dataBuffer[endIndex + 1:]
                    continue
                
                # by this point we have good packet structure.
                if startIndex != 0:
                    print ('Unhandled exception, flushing dataBuffer...')
                    dataBuffer = ''
                    continue
                
                message = dataBuffer[1:endIndex]
                self.server.onRecvMessage(message)
                dataBuffer = dataBuffer[endIndex+1:]
        
        print ("done handling!")

if __name__ == "__main__":
    CreateServer('localhost', 9999, print)
    
