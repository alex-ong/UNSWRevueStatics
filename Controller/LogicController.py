import sys

import Networking.TCPServer as TCPServer
import json
import collections
from Controller.IOConverter import IOConverter
from Controller.DMXOutputter import DMXOutputter

import Model.OptionButtons as OptionButtons
 
class LogicController(object):
    
            
    def __init__(self, model, view, host='localhost', port=9999):
        self.model = model
        self.model.bindNotifyControllerReset(self.OnModelReset)
        
        self.view = view
        
        self.dmxSender = None
        self.setupView()
        self.setupOutput()
    
        self.sliderInput = TCPServer.CreateServer(host, port, self.receiveInput)    
        self.inputEventMaster = IOConverter()
            
    def setupView(self):
        model = self.model
        self.view.setupTopBar((model.grandMaster.getSliderPerc, model.grandMaster.getDBO))
        self.view.setupChannels(model.channelValues)        
        self.view.setupFaders(model.getFaderValues, model.getNumFaders()) 
        self.view.setupConsole(model.console)
        self.view.setupCueList(model.cueList)
        self.view.setupModalForms(model.modals)
        self.view.setupFunctionButtons(OptionButtons.getInstance().getCurrentState)
        self.view.focus_force()
    
    def setupOutput(self):
        model = self.model
        if self.dmxSender is not None:
            self.dmxSender.stop()
            self.dmxSender = None
        self.dmxSender = DMXOutputter(self.model.getDMXOutput)
    
    # model calls this whenenevr model is Reset
    def OnModelReset(self):            
        self.view.reset()  # destroy as much view things as possible.
        self.setupView()        
        self.setupOutput()
                
    # called when we receive network input
    def receiveInput(self, msg):             
        msg = json.loads(msg)         
        self.inputEventMaster.addState(msg)
        
    def update(self, timeDelta):  # occurs in main thread/same thread as tkinter        
        self.handleInput()  # controller update        
        self.model.update(timeDelta)  # model update        
        self.view.refreshDisplay()  # view update                
        self.handleOutput()
        
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
    
    def handleOutput(self):
        self.dmxSender.update()
            
    def handleSliderInput(self, sliderName, value):
        self.model.handleSliderInput(sliderName, value)
    
    def handleButtonInput(self, buttonName, value):
        if buttonName.startswith('raw'):
            self.model.handleRawButtonInput(buttonName, value)
        else:
            self.model.handleButtonInput(buttonName, value)
        