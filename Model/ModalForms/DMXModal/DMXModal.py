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
            self.onFinish(None, None)
        elif isinstance(command, SelectAndSetCommand):
            self.HandleSelectAndSet(command)    
        else:
            print ("Unsupported command", command)
            
    def HandleSelectAndSet(self, command):
        target = command.target        
        value = command.value
        targetDMX = [i + value for i in range(len(target))]
        targetIndex = [int(target[i].replace('Channel', '')) 
                       for i in range(len(target))]
        pairs = [(targetIndex[i], targetDMX[i]) for i in range(len(targetDMX))]
                        
        # check to see if any of the indices are above 512
        # remove all offending pairs
        for i in range(len(pairs)-1,-1,-1):
            if pairs[i][1] > 512:
                pairs.pop(i); #todo right function call
                            
        # remove everything that has targetDMX
        for key, value in self.data.items():
            if value in targetDMX:
                self.data[key] = None
        # finally, set everything
        for key, value in pairs:
            self.data[key] = value
        self.updateModel(self.data)
        
    def reset(self):
        self.console.reset()
        
class DMXModalProgrammer(object):
    def __init__(self, dmxModal):
        self.dmxModal = dmxModal
        
    def clear(self):
        pass
        
    def handleCommand(self, command):
        self.dmxModal.handleConsoleCommand(command)
