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
        self.playbackValue = None
        self.groupValue = None
        self.recordValue = None        
        
    def setDMXAddress(self, newAddress):
        self._dmxAddress = newAddress
             
    def setDirectValue(self, value):
        self.directValue = value
        
    # value that gets pushed out to dmx
    def getCueValue(self):
        if self.recordValue is not None:
            return self.recordValue
        else: #todo: scan through direct,playback,group and do HTP 
            return self.directValue
    
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
            if self.groupValue is not None and self.groupValue > 0:
                values.append(self.groupValue)
            
            maxValue = max(values)
            if maxValue == 0:
                return 0, ValueType.NONE            
            elif maxValue == self.directValue:
                return self.directValue, ValueType.DIRECT
            elif maxValue == self.playbackValue:
                return self.playbackValue, ValueType.PLAYBACK
            elif maxValue == self.groupValue:
                return self.groupValue, ValueType.GROUP
            
                        