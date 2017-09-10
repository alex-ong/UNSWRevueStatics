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
        self.label = label
        self.setLabel(label)        
        
        self.directValue = 0
        self.directFlashValue = 0
        self.playbackValue = 0
        self.recordValue = None
        self.channelMappings = channelMappings
        
    def setLabel(self, label):
        if label is None:
            label = "Group " + str(self.number).zfill(2)
        self.label = label        
        
    def setDirectValue(self, value):
        self.directValue = value
        self.propagateValue()
    
    def getDirectValue(self):
        return max(self.directValue,self.directFlashValue)
    
    def setRecordValue(self, value):
        self.recordValue = value
        self.propagateValue()
        
    def setDirectFlashValue(self, value):
        self.directFlashValue = value
        self.propagateValue()
    
    def setPlaybackValue(self, value):
        self.playbackValue = value
        self.propagateValue()
        
    def propagateValue(self):
        value = self.getDisplayValueAndReason()[0]
        for channel, proportion in self.channelMappings:
            channel.setGroupValue(self.number, round(value*proportion/100)) #TODO THIS
        
    def setChannelMappings(self, mappings):
        self.channelMappings = mappings
    
    def resetDirect(self):
        self.directValue = 0

    def reset(self):
        self.directValue = 0
        self.directFlashValue = 0
        self.playbackValue = 0
        self.recordValue = None
    
    def clearPlayback(self):                
        self.playbackValue = 0
                
    def clearRecord(self):
        self.recordValue = None
        
    def getDisplayValueAndReason(self):
        # returns the value and either "direct", "playback", "group" or "record"
        if self.recordValue != None:
            return self.recordValue, ValueType.RECORD
        else:
            values = [0]
            if self.getDirectValue() > 0:
                values.append(self.getDirectValue())
            if self.playbackValue is not None and self.playbackValue > 0:
                values.append(self.playbackValue)
            
            maxValue = max(values)
            if maxValue == 0:
                return 0, ValueType.NONE            
            elif maxValue == self.getDirectValue():
                return self.directValue, ValueType.DIRECT
            elif maxValue == self.playbackValue:
                return self.playbackValue, ValueType.PLAYBACK 
    
    def getCueValueAndReason(self):
        return self.getDisplayValueAndReason()    
            
    