'''
@author: alex-ong
@date 2017-05-07
'''

'''
list of all groups and channels + values.
'''
from libs.string_decimal import fromStr

def fromDict(data):
    fadeTimes = data['fadeTimes']    
    fadeTimes = (fromStr(fadeTimes[0]), fromStr(fadeTimes[1])) 
    return Cue(data['mappings'], fadeTimes)        

class Cue(object):
    def __init__(self, mappings, fadeTimes):
        self.mappings = mappings     
        self.upTime = fadeTimes[0]
        self.downTime = fadeTimes[1]
        self.playableCue = None
                
    def toDict(self):
        return {'mappings': self.mappings, 'fadeTimes': [str(self.upTime), str(self.downTime)]}
    
    def getValues(self):
        return self.mappings
    
