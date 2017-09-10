'''
@author: alex-ong
@date 2017-05-07
'''

# a desk channel. It is directly in control of a single DMX address.
# their name is simply what number they are.
BYTE_MAX = 255
BYTE_MIN = 0

from enum import Enum

class ValueType(Enum):
    DIRECT = 0
    PLAYBACK = 1
    GROUP = 2
    RECORD = 3
    NONE = 4
    
class Channel(object):
    def __init__(self, number, dmxAddress):
        self.number = number
        self.label = str(number)
        self._dmxAddress = dmxAddress
        
        self.directValue = 0
        self.directFlashValue = 0
        self.playbackValue = 0
        self._groupValue = {}
        self.recordValue = None        
    
    def setDMXAddress(self, newAddress):
        self._dmxAddress = newAddress
             
    def resetDirect(self):
        self.directValue = 0
        
    def setDirectValue(self, value):
        self.directValue = value
        
    def setDirectFlashValue(self, value):
        self.directFlashValue = value
    
    def setGroupValue(self, groupNumber, value):
        if value == 0:
            try:
                del self._groupValue[groupNumber]
            except:
                pass
        else:
            self._groupValue[groupNumber] = value
            
    def getDirectValue(self):
        return max(self.directValue, self.directFlashValue)
    
    def setRecordValue(self, value):
        self.recordValue = value
        
    def getGroupValue(self):
        if self._groupValue == {}:
            return 0
        else:
            values = self._groupValue.values()
            return max(values)                    
    
    def setPlaybackValue(self, value):
        self.playbackValue = value
        
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
            groupValue = self.getGroupValue() 
            if groupValue > 0:
                values.append(groupValue)
            
            maxValue = max(values)
            if maxValue == 0:
                return 0, ValueType.NONE            
            elif maxValue == self.getDirectValue():
                return self.getDirectValue(), ValueType.DIRECT
            elif maxValue == self.playbackValue:
                return self.playbackValue, ValueType.PLAYBACK
            elif maxValue == groupValue:
                return groupValue, ValueType.GROUP
    
    #same as above but we don't use groupValue
    def getCueValueAndReason(self):
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
                return self.getDirectValue(), ValueType.DIRECT
            elif maxValue == self.playbackValue:
                return self.playbackValue, ValueType.PLAYBACK
                                      
    def clearPlayback(self):                
        self.playbackValue = 0
                
    def clearRecord(self):
        self.recordValue = None            
