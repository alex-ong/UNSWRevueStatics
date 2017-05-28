# The programmer has a selection of things (channels,groups,faders etc)
# It also has storage of values set by it (e.g. Channel1 @ 10)
from libs.sorted_containers.sortedset import SortedSet

from Model.CommandProgrammer.Command import (SelectCommand, SetCommand, SelectAndSetCommand,
                                              DeleteCommand, RecordCommand, DecimalCommand, TimeCommand)
from Model.CommandProgrammer.parser import  CUE, CHANNEL, GROUP

from Model.ModalContainer import TIME_MODAL

class Programmer(object):
    def __init__(self, cueList, faderValues, groupValues, channelValues, modals):
        self.currentlySelected = SortedSet()
        self.cueList = cueList
        self.faderValues = faderValues
        self.groupValues = groupValues
        self.channelValues = channelValues
        self.modals = modals
        
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
        elif isinstance(command, DecimalCommand):  # should never reach this
            return ("Entering a decimal number isn't a command.")
        elif isinstance(command, TimeCommand):
            self.modals.addToStack(TIME_MODAL)
            cueLabel = str(self.cueList.currentCue)
            self.modals.peekStack().show(cueLabel, self.finishTimeModal)
            return None
        
    def finishTimeModal(self, response, data):
        if data is None:
            return response
        else:
            print (response, data)
        self.modals.pop()
        
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
                            item = self.groupValues[groupNum] 
                        elif CHANNEL in string:
                            chanNum = int(string.replace(CHANNEL, ''))
                            item = self.channelValues[chanNum]
                        item.setRecordValue(command.value)
                    except Exception as e:
                        print (e)
                    
    
    def _doSelectAndSet(self, command):
        select = SelectCommand(command.target)
        setValue = SetCommand(command.value)        
        try:
            self._doSelect(select)            
        except:
            return "Error when selecting items"
        
        try:
            self._doSet(setValue)
            return "Selected then set to: ", +str(setValue.value)
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
        else:  # todo record groups, faders
            print ("unhandled Command", command)
            
    def clear(self):
        self.groupValues.clearRecord()
        self.channelValues.clearRecord()        
    
if __name__ == '__main__':
    pass
