'''
TODO:
name, channels:maxValue bindings.
'''

'''
@author: alex-ong
@date 2017-05-07
'''

# a desk channel. It is directly in control of a single DMX address.
# their name is simply what number they are.
BYTE_MAX = 255
BYTE_MIN = 0

class Group(object):
    def __init__(self, number, label, channelMappings):
        self.number = number
        if label is None:
            label = "Group " + str(self.number)
        self.label = label
        self.perc = 0
        
        self.directValue = 0
        self.playbackValue = 0
        self.recordValue = 0
        
    
        
    def setChannelMappings(self, mappings):
        self.channelMappings = mappings
             
    
    