import sys

import Networking.TCPServer as TCPServer
import json
import collections
from Controller.IOConverter import IOConverter

class LogicController(object):
    def __init__(self, model, view, host='localhost', port=9999):
        self.model = model
        self.view = view
        
        self.view.setupChannels(model.channelValues)
        #self.view.setupGroups(model.groupValues)
        self.view.setupFaders(model.faderValues)
        self.view.setupConsole(model.console)
        self.view.setupCueList(model.cueList)
        self.sliderInput = TCPServer.CreateServer(host, port, self.receiveInput)
        
        self.inputEventMaster = IOConverter()
        
        
    # called when we receive network input
    def receiveInput(self, msg):             
        msg = json.loads(msg)         
        self.inputEventMaster.addState(msg)
        
    def update(self):  # occurs in main thread/same thread as tkinter
        self.handleInput()        
            
    def handleInput(self):
        inputEvents = self.inputEventMaster.getEvents()
        if inputEvents != {}:
            for key in inputEvents:
                if key.startswith('slider'):
                    self.handleSliderInput(key, inputEvents[key].value)
                else:
                    buttonEvents = inputEvents[key]
                    for buttonEvent in buttonEvents:
                        self.handleButtonInput(key, buttonEvent.down)
        
            self.view.refreshDisplay()
            
    def handleSliderInput(self, sliderName, value):
        self.model.handleSliderInput(sliderName, value)
    
    def handleButtonInput(self, buttonName, value):
        self.model.handleButtonInput(buttonName, value)
