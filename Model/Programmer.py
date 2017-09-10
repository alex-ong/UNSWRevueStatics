# The programmer has a selection of things (channels,groups,faders etc)
# It also has storage of values set by it (e.g. Channel1 @ 10)
from libs.sorted_containers.sortedset import SortedSet

from Model.CommandProgrammer.Command import (SelectCommand, SetCommand, SelectAndSetCommand,
                                              DeleteCommand, RecordCommand, DecimalCommand, TimeCommand,
                                              MenuCommand, NameCommand, SuckCommand)
from Model.CommandProgrammer.parser import  CUE, CHANNEL, GROUP

from Model.ModalContainer import TIME_MODAL, MENU_MODAL, TEXT_ENTRY_MODAL
from libs.string_decimal import string_decimal

class Programmer(object):
    def __init__(self, cueList, faderValues, groupValues, channelValues, modals, deskModel):
        self.currentlySelected = SortedSet()
        self.cueList = cueList
        self.faderValues = faderValues
        self.groupValues = groupValues
        self.channelValues = channelValues
        self.modals = modals
        self.deskModel = deskModel
        
    def handleCommand(self, command):
        if isinstance(command, SelectCommand):
            return self._doSelect(command)            
        elif isinstance(command, SetCommand):
            return self._doSet(command)
        elif isinstance(command, SelectAndSetCommand):
            return self._doSelectAndSet(command)
        elif isinstance(command, DeleteCommand):
            return self._doDelete(command)
        elif isinstance(command, RecordCommand):
            return self._doRecord(command)
        elif isinstance(command, NameCommand):
            return self._doName(command)
        elif isinstance(command, DecimalCommand):  # should never reach this
            return ("Entering a decimal number isn't a command.")
        elif isinstance(command, TimeCommand):
            return self._doTime()
        elif isinstance(command, MenuCommand):
            return self._doMenu()       
        elif isinstance(command, SuckCommand): 
            self._doSuckDick()
        else:
            return "Command not recognized"
        
    def _doMenu(self):
        self.modals.addToStack(MENU_MODAL)
        # Todo: forward all data required...
        self.modals.peekStack().show(None, self._finishMenuModal)
        return None
    
    def _finishMenuModal(self, response, data):
        # we ignore the response and data.
        self.modals.popStack()
        
    def _doTime(self):
        if (self.cueList.currentCue is not None):
            self.modals.addToStack(TIME_MODAL)
            cueLabel = str(self.cueList.currentCue)
            self.modals.peekStack().show("Set time for cue " + cueLabel, self._finishTimeModal)
            return None
        else:
            return ("Error: No Cues. Can't modify time")
        
    def _doSuckDick(self): #hehe. Should be _doSuck        
        for group in self.groupValues.values.values():            
            value, _ = group.getCueValueAndReason()            
            if value > 0:
                self.groupValues[group.number].setRecordValue(value)
                
        for channel in self.channelValues.values.values():
            value, _ = channel.getCueValueAndReason()
            if value > 0:
                self.channelValues[channel.number].setRecordValue(value)
        return ("Set active values into programmer")
        
    def _finishTimeModal(self, response, data):
        if data is None:  # user cancelled.
            pass
        else:
            self.cueList.changeCueTime(data[0], data[1])            
        self.modals.popStack()
        
    def _doSelect(self, command):
        if len(command.target) > 0:
            if CUE in command.target[0]:
                cueTarget = command.target[0].replace(CUE, '')                
                return self.cueList.goto(cueTarget)
            else:  # select group and or channel
                self.currentlySelected = SortedSet(command.target)
                return 'Selected:' + str(command.target)
        else:
            return 'No targets selected'
    
    def _doSet(self, command):
        if len(self.currentlySelected) == 0:
            return 'No items to set'
        else:
            if CUE in self.currentlySelected[0]:
                return 'Unable to perform this command on a cue'
            else:
                for string in self.currentlySelected:
                    item = None
                    try:
                        if GROUP in string:
                            groupNum = int(string.replace(GROUP, ''))
                            if groupNum in self.groupValues:
                                item = self.groupValues[groupNum] 
                        elif CHANNEL in string:
                            chanNum = int(string.replace(CHANNEL, ''))
                            if chanNum in self.channelValues:
                                item = self.channelValues[chanNum]
                        if item is not None:
                            item.setRecordValue(command.value)
                    except Exception as e:
                        print (e)
                return ("Set selected items to " + str(command.value)) 
                    
    
    def _doSelectAndSet(self, command):
        select = SelectCommand(command.target)
        setValue = SetCommand(command.value)        
        try:
            self._doSelect(select)            
        except:
            return "Error when selecting items"
        
        try:
            self._doSet(setValue)            
            return ("Selected then set to: " + str(command.value))
        except:
            return "Error when setting items"  
        
    def _doDelete(self, command):
        if CUE in command.target:
            return self.cueList.deleteCue(command.target)
        else:  # todo delete groups
            print ("unhandled Command", command)
            
    def _doRecord(self, command):
        if CUE in command.target:
            return self.cueList.recordCue(command.target)
        elif GROUP in command.target:
            return self.deskModel.recordGroup(command.target)         
        
    def _doName(self, command):
        # auto-target if no target given.
        if command.target is None:
            command.target = self.cueList.currentCue
            if command.target is None:
                return("No target selected for naming")
            else:
                command.target = CUE + str(self.cueList.currentCue)
        if CUE in command.target:
            # quick validation before bringing up modal
            if (self.cueList.hasCue(command.target)):
                self._doNameModal(command.target)
            else:
                return("Cue doesn't exist")
        elif GROUP in command.target:        
            # quick validation before bringing up modal
            try:
                target = int(command.target.replace(GROUP, ''))
            except:
                return("Invalid Group:", str(command.target))
            if target in self.groupValues:
                self._doNameModal(command.target)        

    def _doNameModal(self, target):        
        self.modals.addToStack(TEXT_ENTRY_MODAL)        
        self.modals.peekStack().show("Set label for " + target,
                                     lambda response, data: self._finishNameModal(target, response, data))
        
    
    def _finishNameModal(self, target, response, data):
        if data is None:  # user cancelled.
            pass
        else:            
            if CUE in target:
                self.cueList.changeLabel(target, data)
            elif GROUP in target:               
                self.deskModel.changeGroupLabel(target, data)            
        self.modals.popStack()

    def clear(self):
        self.groupValues.clearRecord()
        self.channelValues.clearRecord()        
    
if __name__ == '__main__':
    pass
