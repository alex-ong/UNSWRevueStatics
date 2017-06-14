from Model.ModalForms import AbstractModal
from Model.DMXPatchConsole import validOperators
 
class DMXModal(AbstractModal):
    def __init__(self):
        super().__init__()
        self.data = None
        self.updateModel = None
        self.console = Console.Console(self.programmer, validOperators)
        
    def subclassShow(self):
        self.data = self.onShowArguments[0]
        self.updateModel = self.onShowArguments[1]
         
    def handleCommand(self, command):
        pass 
        
class DMXModalProgrammer(object):
    def __init__(self, dmxModal):
        self.dmxModal = dmxModal
        
    def clear(self):
        self.dmxModal.handleClear()
        
    def handleCommand(self, command):
        self.dmxModal.handleCommand(command)