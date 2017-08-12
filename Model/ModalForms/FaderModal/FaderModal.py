from Model.CommandProgrammer.FaderPatchConsole import validOperators
from Model.ModalForms.BasePatchModal import BasePatchModal
from Model.ModalForms.DMXModal.DMXModal import CHANNEL_MAX
from Model import OptionButtons
from Model.FaderValues import NEXT_FADERS, PREV_FADERS

def faderStringToNumber(string):
    return int(string.replace('Fader', ''))
        
class _FaderMapping(object):
    CHANNEL = 'Channel'
    GROUP = 'Group'
    def __init__(self, stringTarget):        
        self.faderType = None        
        if _FaderMapping.CHANNEL in stringTarget:
            self.faderType = _FaderMapping.CHANNEL
            stringTarget = stringTarget.replace(_FaderMapping.CHANNEL,'')
        else:
            self.faderType = _FaderMapping.GROUP
            stringTarget = stringTarget.replace(_FaderMapping.GROUP,'')

        self.targetNumber = int(stringTarget)
    
    def __str__(self):
        if self.faderType == None:
            return ''
        else:
            return self.faderType + " " + str(self.targetNumber).zfill(2)
    
    def toTextFile(self):
        if self.faderType == None:
            return None
        elif self.faderType == _FaderMapping.CHANNEL:
            return int(self.targetNumber)
        else: #self.faderType == _FaderMapping.GROUP:
            return 'group' + str(self.targetNumber)
        
class FaderModal(BasePatchModal):
    def __init__(self, model):
        super().__init__(model)
        self.currentMappings = None
        self.currentPageNumber = 0        
        
    def handleFaderCommand(self, command):
        print ("handling fader command", command)
        if command == NEXT_FADERS:
            self.currentPageNumber += 1 #todo wrap
            if self.currentPageNumber >= len(self.model.faderBindings):
                self.currentPageNumber = 0
        elif command == PREV_FADERS:
            self.currentPageNumber -= 1 #todo wrap
            if self.currentPageNumber < 0:
                self.currentPageNumber = len(self.model.faderBindings) - 1
                
        
    def optionButtonBindings(self):
        return OptionButtons.FADER_BINDING_STATE
    
    def getFaders(self):
        return self.model.getFaderBindings(self.currentPageNumber)
    
    def basePatchSubclassGetValidOperators(self):
        return validOperators

    def newFaderMapping(self, stringTarget, model):
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
        self.currentMappings = self.newFaderMapping(target, self.model)        
        
    
    def writeFaderMapping(self, pageNumber, faderNumber, mapping):
        self.data[pageNumber][faderNumber] = mapping
        self.updateModel(self.data)

    def HandleRecord(self, command):                
        target = command.target
        faderNumber = faderStringToNumber(target)
        #todo: check faderNumber < 27
        if self.currentMappings is not None:
            self.writeFaderMapping(self.currentPageNumber, faderNumber, 
                                   self.currentMappings.toTextFile())                
    
    def HandleDelete(self, command):
        target = command.target
        faderNumber = faderStringToNumber(target)
        #todo: check faderNumber < 27       
        self.writeFaderMapping(self.currentPageNumber, faderNumber, None)            
        
    def HandleClear(self):
        self.currentMappings = None
