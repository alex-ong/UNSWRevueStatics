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
        
    # called when we receive network input
    def receiveInput(self, msg):
        self.lastInput = json.loads(msg)        
        
    def update(self):  # occurs in main thread/same thread as tkinter
        self.handleInput()        
            
    def handleInput(self):
        if self.lastInput != {}:
            print (self.lastInput)
            for key in self.lastInput:
                if key.startswith('slider'):
                    self.handleSliderInput(key, self.lastInput[key])
                else:
                    self.handleButtonInput(key, self.lastInput[key])
            self.lastInput = {}
            
    def handleSliderInput(self, sliderName, value):
        self.model.handleSliderInput(sliderName,value)
    
    def handleButtonInput(self, buttonName, value):
        pass
