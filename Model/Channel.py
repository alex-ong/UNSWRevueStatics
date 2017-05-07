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
        self._dmxValue = 0 #byte value from 0->255
        self._dmxAddress = dmxAddress
        
    def setDMXAddress(self, newAddress):
        self._dmxAddress = newAddress
        
    def setValueHTP(self, newValue):
        value = max(newValue, self._dmxValue)
        self.setValue(value)
         
    #sets the value immediately.        
    def setValue(self, dmxValue):
        dmxValue = max (dmxValue, BYTE_MIN)
        dmxValue = min (dmxValue, BYTE_MAX)
        self._dmxValue = dmxValue
    
    # perc is a _dmxValue from 0.0 to 1.0
    def setPerc(self, perc):
        self.setValue(int(perc * BYTE_MAX))

    # returns a _dmxValue from 0.0 to 1.0          
    def getPerc(self):
        return self._dmxValue / float(BYTE_MAX)
    