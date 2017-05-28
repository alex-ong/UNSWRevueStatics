'''
@author: alex-ong
@date 2017-05-07

Our parser outputs Commands which the Model can interpret
'''
    
class AbstractCommand():
    def __init__(self):
        pass
    
class DecimalCommand(AbstractCommand):
    def __init__(self, decimal):
        self.value = decimal
    def __str__(self):
        return ('set to:', str(decimal))
    
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
        return ('Record current direct values to ' + self.target)

class DeleteCommand(AbstractCommand):
    def __init__(self, target):
        self.target = target 
    def __str__(self):
        return ('Delete ' + self.target)

class TimeCommand(AbstractCommand):
    def __str__(self):
        return ("Set current cue's up/down times")
    
        