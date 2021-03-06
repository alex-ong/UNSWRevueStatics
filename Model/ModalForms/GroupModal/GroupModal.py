from Model.CommandProgrammer.GroupPatchConsole import validOperators
from Model.ModalForms.BasePatchModal import BasePatchModal
from Model.ModalForms.DMXModal.DMXModal import CHANNEL_MAX

class GroupModal(BasePatchModal):
    def __init__(self, model):
        super().__init__(model)
        self.currentMappings = { x:0 for x in range(1,CHANNEL_MAX+1)}
    
    def getModelGroups(self):
        return self.model.groupValues
    
    def basePatchSubclassGetValidOperators(self):
        return validOperators
    
    def HandleSelectAndSet(self, command):
        targets = command.target
        indices = []
        # quick data validation        
        for target in targets:
            if 'Channel' in target:
                target = int(target.replace('Channel',''))
                if target > 0 and target < CHANNEL_MAX:
                    indices.append(target)
                else:
                    print ("Warning - tried to select Channel", target)
            else:
                print ("Warning - following was selected:" + target)
        value = command.value
        value = min(100,value) #cap value at 100
        for target in indices:
             self.currentMappings[target] = value
        
    def getCurrentMapping(self):
        result = []
        for key, value in self.currentMappings.items():
            if value != 0:
                result.append([key,value])
        return result
    
    def writeGroupMapping(self, groupNumber, mapping):
        self.data[groupNumber]["channels"] = mapping
        self.updateModel(self.data)
        
    def writeGroupLabel(self, groupNumber, label = None):
        if label is None:
            label = "Group" + str(groupNumber)
        self.data[groupNumber]["name"] = label
        self.updateModel(self.data)
        
    def HandleRecord(self, command):
        target = command.target
        groupNumber = int(target.replace('Group',''))
        self.writeGroupMapping(groupNumber, self.getCurrentMapping())                
    
    def HandleDelete(self, command):
        target = command.target
        groupNumber = int(target.replace('Group',''))   
        
        self.writeGroupMapping(groupNumber, [])
        self.writeGroupLabel(groupNumber, None)        
        
    def HandleClear(self):
        for index in self.currentMappings.keys():
            self.currentMappings[index] = 0
