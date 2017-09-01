# to change dmxSender implementation, replace the first line in dmxSender/dmxSender
from dmxSender.dmxSender import DmxSender

import sys
import time
import json

try:
    sys.path.append('../Networking')  # hack to run locally
    import TCPServer  # run locally
except ImportError:
    sys.path.append('Networking')
    import TCPServer  # run from UNSWRevueStatics folder


# class that transfers packets from UNSWRevueStatics to the DMXKing
class DMXNetworkDaemon(object):
    def __init__(self, comPort):
        self.comPort = comPort
        try:
            self.sender = DmxSender(comPort)
        except Exception as e:
            print (e)
            self.sender = None
        self.listener = TCPServer.CreateServer('localhost', 9001, self.receiveInput)
    
    # called when we receive network input
    def receiveInput(self, msg):             
        msg = json.loads(msg)   
        print(msg)
        if self.sender is not None:
            for i in range(512):
                print(i+1, msg[i])
                self.sender.setChannel(i+1, msg[i])
            print("Sending")
            self.sender.render()                

if __name__ == '__main__':
    if len(sys.argv) < 2:
        print ("Usage: python dmx-daemon.py COM_PORT")
        print ("COM_PORT can be a number or linux com port string")
        print ("press enter to exit")
        _ = input()
        sys.exit()
        
    daemon = DMXNetworkDaemon(sys.argv[1])
    
    print ("Use control+c to exit!")
    try:
        while True:
            time.sleep(0.01)    
    except KeyboardInterrupt:   
        daemon.listener.kill_server()
        daemon.listener.stop()
        time.sleep(0.5)