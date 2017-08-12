'''
@author: alex-ong
@date 2017-05-10    
'''

'''
an array of Faders
'''
import Model.Fader as Fader
from _collections import OrderedDict


NEXT_FADERS = 'NextFaders'
PREV_FADERS = 'PrevFaders'
FADER_COMMANDS = [NEXT_FADERS, PREV_FADERS]
# an array of Faders

class FaderValues(object):
    def __init__(self, faderConfiguration):              
        self.values = OrderedDict([(key, Fader.Fader(key, value)) for key, value in faderConfiguration.items()])
    
    def __iter__(self):
        return iter(self.values)
    
    def __getitem__(self, i):
        return self.values[i]
    
    def __len__(self):
        return len(self.values)
    
    def resetValues(self):
        for value in self.values:
            value.reset()
            
