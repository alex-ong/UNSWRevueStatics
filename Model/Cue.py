'''
@author: alex-ong
@date 2017-05-07
'''

'''
list of all groups and channels + values.
'''
from libs.string_decimal import fromStr
from _collections import OrderedDict
import json

def fromDict(data):
    fadeTimes = data['fadeTimes']    
    fadeTimes = (fromStr(fadeTimes[0]), fromStr(fadeTimes[1]))
    label = None
    if 'label' in data:
        label = data['label']
    return Cue(OrderedDict(data['mappings']), fadeTimes, label)        

class Cue(object):
    def __init__(self, mappings, fadeTimes, label):
        self.mappings = mappings     
        self.upTime = fadeTimes[0]
        self.downTime = fadeTimes[1]
        self.playableCue = None
        self.label = label
    
    def toDict(self):
        result = {}
        result['mappings'] = list(self.mappings.items())
        result['fadeTimes'] = [str(self.upTime), str(self.downTime)]
        if self.label is not None:
            result['label'] = self.label 
        return result
    
    def getValues(self):
        return self.mappings
    
