from Model.ModalForms import AbstractModal
from Model.CommandProgrammer.DMXPatchConsole import validOperators
from Model.CommandProgrammer.Command import MenuCommand, SelectAndSetCommand

from Model import Console
class DMXModal(AbstractModal.AbstractModal):
    def __init__(self):
        super().__init__()
        self.data = None
        self.updateModel = None
        self.programmer = DMXModalProgrammer(self)
        self.console = Console.Console(self.programmer, validOperators)
        
    def subclassShow(self):
        self.data = self.onShowArguments[0]
        self.updateModel = self.onShowArguments[1]
         
    # handle raw buttons
    def handleCommand(self, command):
        self.console.parseString(command)
            
    # handle commands caused by a list of raw buttons.
    def handleConsoleCommand(self, command):
        if isinstance(command, MenuCommand):
            self.onFinish(None,None)
        elif isinstance(command, SelectAndSetCommand):
            print ('set and select', command)    
    
    def reset(self):
        self.console.reset()
        
class DMXModalProgrammer(object):
    def __init__(self, dmxModal):
        self.dmxModal = dmxModal
        
    def clear(self):
        pass
        
    def handleCommand(self, command):
        self.dmxModal.handleConsoleCommand(command)