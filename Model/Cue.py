'''
@author: alex-ong
@date 2017-05-07
'''

'''
list of all groups and channels + values.
'''

def fromDict(data):
    return Cue(data['mappings'],data['fadeTimes'])    
    
class Cue(object):
    def __init__(self, mappings, fadeTimes):
        self.mappings = {}        
        self.upTime = fadeTimes[0]
        self.downTime = fadeTimes[1]
        
    def toDict(self):
        return {'mappings': self.mappings,  'fadeTimes': [self.upTime,self.downTime]}
    
    def getValues(self):
        return self.mappings