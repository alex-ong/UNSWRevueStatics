from Networking import TCPClient

DMX_TCP_PORT = 9001
class DMXOutputter(object):
    def __init__(self, toSend):
        self.toSend = toSend
        self.sender = TCPClient.CreateClient('localhost', DMX_TCP_PORT)
        self.lastMessage = None
        
    def update(self):
        nextMessage = self.toSend()
        if nextMessage != self.lastMessage:
            self.sender.sendMessage(str(nextMessage))
            self.lastMessage = nextMessage
            
    def stop(self):
        self.sender.stop()            