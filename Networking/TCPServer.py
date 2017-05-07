import socketserver
import threading
import socket

def CreateServer(target, port):
    HOST, PORT = target, port
    
    server = socketserver.ThreadingTCPServer((HOST, PORT), MyTCPHandler)

    # Activate the server; this will keep running until you
    # interrupt the program with Ctrl-C
    server.serve_forever()
    print('hmm')
    
class MyTCPHandler(socketserver.BaseRequestHandler):
    """
    The request handler class for our server.

    It is instantiated once per connection to the server, and must
    override the handle() method to implement communication to the
    client.
    """
    def setup(self):
        self.request.setsockopt(socket.IPPROTO_TCP,
                                   socket.TCP_NODELAY, True)
    def handle(self):
        # self.request is the TCP socket connected to the client
        try:
            while True:
                self.data = self.request.recv(1024).strip()
                if not self.data:
                    break #disconnection 
                print("{} wrote:".format(self.client_address[0]))
                print(self.data)
                # just send back the same data, but upper-cased
                self.request.sendall(self.data.upper())
        except:
            pass
        print ("done handling!")

if __name__ == "__main__":
    CreateServer('localhost', 9999)
    