'''
@author: alex-ong
@date 2017-05-07
'''

'''
an array of channels
'''
import Model.Channel as Channel

DMX_PER_UNIVERSE = 512

# an array of channels.
# "playback" will have a copy of this, and "recording" will also have a copy.
# then we can combine the values to get the final channel Values.
# also we can use this array to combine groups with channels.
class ChannelValues(object):
    def __init__(self):
        self.values = [Channel.Channel(i) for i in range(DMX_PER_UNIVERSE)]
                
    def resetValues(self):
        for value in self.values:
            value.setValue(Channel.BYTE_MIN)
            