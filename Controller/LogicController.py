import sys

import Networking.TCPServer as TCPServer
import json

class LogicController(object):
    def __init__(self, model, view, host='localhost', port=9999):
        self.model = model
        self.view = view
    
        self.view.setupChannels(model.channelValues)
        self.sliderInput = TCPServer.CreateServer(host, port, self.receiveInput)
        
        self.lastInput = {}
    def receiveInput(self, msg):
        self.lastInput = json.loads(msg)        
        
    def update(self): #occurs in main thread/same thread as tkinter
        if self.lastInput != {}:            
            self.view.handleInput(self.lastInput)
            self.lastInput = {}
            
            
    
        # use this function to poll the midi controller etc.
