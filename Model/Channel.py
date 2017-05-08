'''
@author: alex-ong
@date 2017-05-07
'''

# a desk channel. It is directly in control of a single DMX address.
# their name is simply what number they are.
BYTE_MAX = 255
BYTE_MIN = 0

class Channel(object):
    def __init__(self, number, dmxAddress):
        self.number = number
        self._dmxAddress = dmxAddress
        
        self.directValue = 0
        self.playbackValue = None
        self.groupValue = None
        self.recordValue = None        
        
    def setDMXAddress(self, newAddress):
        self._dmxAddress = newAddress
             
    def setDirectValue(self, value):
        self.directValue = value
                
    def getCueValue(self):
        pass
            