from Model.CommandProgrammer.FaderPatchConsole import validOperators
from Model.ModalForms.BasePatchModal import BasePatchModal
from Model.ModalForms.DMXModal.DMXModal import CHANNEL_MAX

def faderStringToNumber(string):
    return int(string.replace('Fader', ''))
        
class _FaderMapping(object):
    CHANNEL = 'Channel'
    GROUP = 'Group'
    def __init__(self, stringTarget):        
        self.faderType = None        
        if CHANNEL in stringTarget:
            self.faderType = CHANNEL
            stringTarget = stringTarget.replace(CHANNEL,'')
        else:
            self.faderType = GROUP
            stringTarget = stringTarget.replace(GROUP,'')

        self.targetNumber = int(stringTarget)
         
class FaderModal(BasePatchModal):
    def __init__(self, model):
        super().__init__(model)
        self.currentMappings = None
        self.currentPageNumber = 0
        
    def basePatchSubclassGetValidOperators(self):
        return validOperators

    def newFaderMapping(stringTarget, model):
        result = _FaderMapping(stringTarget)
        
        # quick check for max Channel/Group Number
        if (result.faderType == _FaderMapping.CHANNEL and
            result.targetNumber > len(model.channelValues) + 1):
            return None
        elif (result.faderType == _FaderMapping.GROUP and
            result.targetNumber > len(model.groupValues) + 1):
            return None    
        return result
    
    def HandleSelect(self, command):
        target = command.target[0]                
        self.currentMappings = newFaderMapping(target, self.model)        
        
    
    def writeFaderMapping(self, pageNumber, faderNumber, mapping):
        pass
        #todo!!
        #self.data[groupNumber]["channels"] = mapping
        #self.updateModel(self.data)

    def HandleRecord(self, command):
        target = command.target
        faderNumber = faderStringToNumber(target)
        self.writeFaderMapping(pageNumber, faderNumber, self.currentMappings)                
    
    def HandleDelete(self, command):
        target = command.target
        faderNumber = faderStringToNumber(target)        
        self.writeGroupMapping(pageNumber, faderNumber, None)            
        
    def HandleClear(self):
        self.currentMappings = None
