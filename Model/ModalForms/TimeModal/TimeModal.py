from Model import Console
from Model.CommandProgrammer.CueTimeConsole import validOperators
from libs import string_decimal
from Model.Console import BACKSPACE, CLEAR, ENTER

from enum import Enum
from Model.CommandProgrammer.parser import value_token

class TimeState(Enum):
    ENTER_UP = 0
    ENTER_DOWN = 1
     
MAX_COMMAND_LENGTH = 5 #max number of characters we support for time.

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
        
    def currentCommandLength(self):
        fullString = ''.join(self.console.tokens)
        return len(fullString)
    
    # called on any user input when modal is active
    def handleCommand(self, command):
        # pass to console...
        # quickly check length of console. We will not accept any input if it is too long
        
        if (command in [ENTER, BACKSPACE, CLEAR] or 
            self.currentCommandLength() < MAX_COMMAND_LENGTH):
            consoleResult = self.console.parseString(command)
        
        # if consoleResult == CLEAR: #call onFinish
        #    print ("console clear pressed")
        #    return
            
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
        if isinstance(command, int):
            command = string_decimal.fromStr(str(command))
            
        if isinstance(command, string_decimal.string_decimal):
            if self.currentState == TimeState.ENTER_UP:
                self.upTime = str(command)
                self.currentState = TimeState.ENTER_DOWN
            elif self.currentState == TimeState.ENTER_DOWN:
                self.downTime = str(command)
                response = "success"
                data = (self.upTime, self.downTime)
                self.onFinish(response, data)
        else:
            print("Unsupported command:", str(command))
        
class TimeModalProgramer(object):
    def __init__(self, timeModal):
        self.timeModal = timeModal
    
    def clear(self):
        print('clear pressed in programmer')
        
    def handleCommand(self, command):        
        return self.timeModal.handleExecuteCommand(command)
    
