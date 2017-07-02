from Model.ModalForms import AbstractModal
from Model.CommandProgrammer.Command import (MenuCommand, SelectAndSetCommand,
                                             DeleteCommand, RecordCommand)

from Model import Console

class BasePatchModal(AbstractModal.AbstractModal):
    def __init__(self, model=None):
        super().__init__()
        self.model = model
        self.data = None
        self.updateModel = None
        self.basePatchSubclassInit()
    
    def basePatchSubclassInit(self):    
        self.programmer = BasePatchModalProgrammer(self)
        self.console = Console.Console(self.programmer, self.basePatchSubclassGetValidOperators())
    
    def basePatchSubclassGetValidOperators(self):
        # override me!
        
        # e.g. 
        #    from Model.CommandProgrammer.DMXPatchConsole import validOperators
        #    return validOperators
        return (lambda x: [])
         
    
    def subclassShow(self):
        self.data = self.onShowArguments[0]
        self.updateModel = self.onShowArguments[1]
         
    # handle raw buttons
    def handleCommand(self, command):
        self.console.parseString(command)
            
    # handle commands caused by a list of raw buttons.
    def handleConsoleCommand(self, command):
        if isinstance(command, MenuCommand):
            self.onFinish(None, None)
        elif isinstance(command, SelectAndSetCommand):
            self.HandleSelectAndSet(command)
        elif isinstance(command, DeleteCommand):
            self.HandleDelete(command)    
        elif isinstance(command, RecordCommand):
            self.HandleRecord(command)
        else:
            print ("Unsupported command", command)
            
    def HandleSelectAndSet(self, command):
        print ("HandleSelectAndSet: Override me!")
                
    def HandleDelete(self, command):
        print("HandleDelete: Override me!")
        
    def HandleRecord(self, command):
        print("HandleRecord: Override me!")
        
    def HandleClear(self):
        pass
        
    def reset(self):
        self.console.reset()
        
class BasePatchModalProgrammer(object):
    def __init__(self, basePatchModal):
        self.basePatchModal = basePatchModal
        
    def clear(self):
        self.basePatchModal.HandleClear()
        
    def handleCommand(self, command):
        self.basePatchModal.handleConsoleCommand(command)
