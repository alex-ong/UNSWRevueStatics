import socket
import threading
import time
import sys
import queue  # threadsafe
try:
    import Networking.StoppableThread as StoppableThread
except:
    import StoppableThread as StoppableThread

HOST, PORT = "localhost", 9999
data = " ".join(sys.argv[1:])


def CreateClient(target, port):    
    client = ThreadedClient(target, port)    
    client.start()
    
    return client
    
class ThreadedClient(StoppableThread.StoppableThread):
    def __init__(self, target, port, *args):
        self.target = target
        self.port = port
        self.messageQueue = queue.Queue()
        super().__init__(*args)    
        
    def sendMessage(self, message):        
        self.messageQueue.put(message)
        
    def run(self):        
        # Create a socket (SOCK_STREAM means a TCP socket)
        while not self.stopped():
            try:
                with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
                    # Connect to server and send data    
                    sock.connect((self.target, self.port))
                    while not self.stopped():
                        try:
                            item = self.messageQueue.get_nowait()
                        except queue.Empty:
                            time.sleep(0.01)
                            continue
                        sock.sendall(bytes('\x00' + item + '\x00', "utf-8"))    
            except: #reconnect on any error
                pass
if __name__ == '__main__':
    client = CreateClient('localhost', 9999)
    import random
    try:
        for i in range(200):
            client.sendMessage('asdf'+str(random.random()))
            time.sleep(0.2)
    except KeyboardInterrupt:
        client.stop()