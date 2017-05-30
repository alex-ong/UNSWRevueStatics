from Model import Console
from Model.CommandProgrammer.CueTimeConsole import validOperators
from libs import string_decimal

from enum import Enum

class TimeState(Enum):
    ENTER_UP = 0
    ENTER_DOWN = 1
     
class TimeModal(object):
    
    def __init__(self):
        self.upTime = None
        self.downTime = None
        self.description = None
        self.programmer = TimeModalProgramer(self)
        self.console = Console.Console(self.programmer, validOperators)
        self.onFinish = None        
        self.currentState = TimeState.ENTER_UP
        
    def show(self, description, onFinish):
        self.reset()
        self.description = description
        self.onFinish = onFinish
        
    def reset(self):
        self.upTime = None
        self.downTime = None
        self.description = None
        self.currentState = TimeState.ENTER_UP
        
    #calld on any user input when modal is active
    def handleCommand(self, command):
        #pass o console...
        consoleResult = self.console.parseString(command)
        #if consoleResult == CLEAR: #call onFinish
        if self.currentState == TimeState.ENTER_UP:
            if len(self.console.tokens) > 0:                
                self.upTime = ''.join(self.console.tokens)
            else:
                self.upTime = None
        elif self.currentState == TimeState.ENTER_DOWN:
            if len(self.console.tokens) > 0:
                self.downTime = ''.join(self.console.tokens)
            else:
                self.downTime = None
        
    
    def handleExecuteCommand(self, command):
        print ('Received', command)
        
        
class TimeModalProgramer(object):
    def __init__(self, timeModal):
        self.timeModal = timeModal
        
    def handleCommand(self, command):
        self.timeModal.handleExecuteCommand(command)