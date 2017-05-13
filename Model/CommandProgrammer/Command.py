'''
@author: alex-ong
@date 2017-05-07

Our parser outputs Commands which the Model can interpret
'''

from enum import Enum
class CommandType(Enum):
    SET_SELECTION = 1 #set channels or groups selected
    SET_VALUE = 2 #set currently selected channels/groups to value
    SET_SELECTION_AND_VALUE = 3 #do SET_SELECTION followed by SET_VALUE
    RECORD = 3 #record cue, bind group to fader, bind channel to group
    
class AbstractCommand():
    def __init__(self):
        pass
    
class SelectCommand(AbstractCommand):
    def __init__(self, target):
        # list of channels/groups to select
        self.target = list(target) 
    def __str__(self):
        return ('select ' + str(self.target))
                        
class SetCommand(AbstractCommand):
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return ('set currently selected to ' + 
                str(self.value))
            
class SelectAndSetCommand(AbstractCommand):
    def __init__(self, target, value):
        self.target = list(target)
        self.value = value
    def __str__(self):
        return ('select ' + str(self.target) +
                ' and then set to ' + str(self.value))
        
#e.g. record fader, record group, record cue 
class RecordCommand(AbstractCommand):
    def __init__(self, target):
        self.target = target
    def __str__(self):
        return ('Record current direct values to ' + 
                str(self.target[0]))
        
        