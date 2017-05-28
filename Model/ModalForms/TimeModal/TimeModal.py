from Model import Console
from Model.CommandProgrammer.CueTimeConsole import validOperators

class TimeModal(object):
    def __init__(self):
        self.upTime = 0
        self.downTime = 0
        self.description = None
        self.programmer = TimeModalProgramer(self)
        self.console = Console.Console(self.programmer, validOperators)
        self.onFinish = None        
                
    def show(self, description, onFinish):
        self.description = description
        self.onFinish = onFinish
        
    
    def handleCommand(self, command):
        print (command)
        
class TimeModalProgramer(object):
    def __init__(self, timeModal):
        self.timeModal = timeModal
        
    def handleCommand(self, command):
        self.timeModal.handleCommand(command)