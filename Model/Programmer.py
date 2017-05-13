# The programmer has a selection of things (channels,groups,faders etc)
# It also has storage of values set by it (e.g. Channel1 @ 10)
from libs.sorted_containers.sortedset import SortedSet

from Model.CommandProgrammer.Command import (SelectCommand, SetCommand, SelectAndSetCommand,
                                              DeleteCommand, RecordCommand)

class Programmer(object):
    def __init__(self):
        self.currentlySelected = SortedSet()
        
    def handleCommand(self, command):
        if isinstance(command, SelectCommand):
            pass
        elif isinstance(command, SetCommand):
            pass
        elif isinstance(command, SelectAndSetCommand):
            pass
        elif isinstance(command, DeleteCommand):
            pass
        elif isinstance(command, RecordCommand):
            pass    
        
    def _doSelect(self, command):
        pass
    
    def _doSet(self, command):
        pass
    
    def _doSelectAndSet(self, command):
        pass
    
    def _doDelete(self, command):
        pass
    
    def _doRecord(self, command):
        pass
    
    def clear(self):
        self.currentlySelected.clear()
        # todo. call model and clear all recorded values.
    
    
if __name__ == '__main__':
    pass
