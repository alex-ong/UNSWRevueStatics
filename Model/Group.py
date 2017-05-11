'''
TODO:
name, channels:maxValue bindings.
'''

'''
@author: alex-ong
@date 2017-05-07
'''

# a group. A mapping for some number of channels and their max value.

from Model.Channel import ValueType
import math

class Group(object):
    def __init__(self, number, label, channelMappings):
        self.number = number        
        if label is None:
            label = "Group " + str(self.number)
        self.label = label        
        
        self.directValue = 0
        self.playbackValue = None
        self.recordValue = None
        self.channelMappings = channelMappings
    
        
    def setDirectValue(self, value):
        self.directValue = value
        self.propagateValue()
    
    def propagateValue(self):
        value = self.getCueValueAndReason()[0]
        for channel, proportion in self.channelMappings:
            channel.setGroupValue(self.number, round(value*proportion/100)) #TODO THIS
        
    def setChannelMappings(self, mappings):
        self.channelMappings = mappings
    
    def reset(self):
        self.directValue = 0
        self.playbackValue = 0
        self.recordValue = 0 
    
    def getCueValueAndReason(self):
        # returns the value and either "direct", "playback", "group" or "record"
        if self.recordValue != None:
            return self.recordValue, ValueType.RECORD
        else:
            values = [0]
            if self.directValue > 0:
                values.append(self.directValue)
            if self.playbackValue is not None and self.playbackValue > 0:
                values.append(self.playbackValue)
            
            maxValue = max(values)
            if maxValue == 0:
                return 0, ValueType.NONE            
            elif maxValue == self.directValue:
                return self.directValue, ValueType.DIRECT
            elif maxValue == self.playbackValue:
                return self.playbackValue, ValueType.PLAYBACK        