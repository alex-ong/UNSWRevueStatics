from Model.ModalForms import AbstractModal
from Model.CommandProgrammer.DMXPatchConsole import validOperators
from Model.CommandProgrammer.Command import MenuCommand, SelectAndSetCommand, DeleteCommand

from Model import Console
from Model.ModalForms.BasePatchModal import BasePatchModal

DMX_MAX = 512
CHANNEL_MAX = 96
class DMXModal(BasePatchModal):
    def __init__(self):
        super().__init__()

    def basePatchSubclassGetValidOperators(self):
        return validOperators
    
    def HandleSelectAndSet(self, command):
        target = command.target        
        value = command.value
        targetDMX = [i + value for i in range(len(target))]
        targetIndex = [int(target[i].replace('Channel', '')) 
                       for i in range(len(target))]
        pairs = [(targetIndex[i], targetDMX[i]) for i in range(len(targetDMX))]
                        
        # check to see if any of the indices are above 512
        # remove all offending pairs
        for i in range(len(pairs) - 1, -1, -1):
            if pairs[i][1] > DMX_MAX:
                pairs.pop(i);  # todo right function call
            elif pairs[i][0] > CHANNEL_MAX:
                pairs.pop(i);
                            
        # remove everything that has targetDMX
        keysToDelete = []
        for key, value in self.data.items():
            if value in targetDMX:
                keysToDelete.append(key)
                
        # do the deleting
        for key in keysToDelete:
            self.data[key] = None
            
        # finally, set everything
        for key, value in pairs:
            self.data[key] = value
        self.updateModel(self.data)
        
    def HandleDelete(self, command):
        target = int(command.target.replace('Channel', ''))
        if target in self.data:
            self.data[target] = None
        self.updateModel(self.data)
