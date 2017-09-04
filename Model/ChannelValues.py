'''
@author: alex-ong
@date 2017-05-07
'''
from _collections import OrderedDict

'''
an array of channels
'''
import Model.Channel as Channel

# an array of channels.
# then we can combine the values to get the final channel Values.
# also we can use this array to combine groups with channels.
class ChannelValues(object):
    def __init__(self, patching):                        
        self.values = OrderedDict([(key,Channel.Channel(key, value)) for
                                    key, value in patching.items()])
    
    def __iter__(self):
        return iter(self.values)
        
    def __getitem__(self, i):
        return self.values[i]
    
    def __len__(self):
        return len(self.values)
    
    def resetValues(self):
        for value in self.values:
            value.setValue(Channel.BYTE_MIN)
                        
    def clearPlayback(self):
        for value in self.values.values():
            value.clearPlayback()
                
    def clearRecord(self):
        for value in self.values.values():
            value.clearRecord()
    
    def getCurrentPlaybackValues(self):
        result = {}
        for channelNumber, value in self.values.items():
            result[channelNumber] = value.playbackValue
        return result
    