from Model.ModalForms import AbstractModal
#from Model.CommandProgrammer.GroupConsole import validOperators
from Model.CommandProgrammer.Command import MenuCommand, SelectAndSetCommand, DeleteCommand 

from Model import Console

class GroupModal(AbstractModal.AbstractModal):
    def __init__(self):
        super().__init__()
        self.data = None
        self.updateModel = None
        self.programmer = GroupModalProgrammer(self)
        self.console = Console.Console(self.programmer, validOperators)
        
    def subclassShow(self):
        self.data = self.onShowArguments[0]
        self.updateModel= self.onShowArguments[1]
    
    def handleCommand(self, command):
        self.console.parseString(command)
        
    def handleConsoleCommand(self, command):
        if isinstance(command, MenuCommand):
            self.onFinish(None, None)
        elif isinstance(command, SelectAndSetCommand):
            self.HandleSelectAndSet(command)
        elif isinstance(command, DeleteCommand):
            self.HandleDelete(command)    
        else:
            print ("Unsupported command", command)
        
    def reset(self):
        self.console.reset()
        
        
class GroupModalProgrammer(object):
    def __init__(self, dmxModal):
        self.dmxModal = dmxModal
        
    def clear(self):
        pass
        
    def handleCommand(self, command):
        self.dmxModal.handleConsoleCommand(command)
