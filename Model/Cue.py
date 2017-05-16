'''
@author: alex-ong
@date 2017-05-07
'''

'''
list of all groups and channels + values.

remember we use HTP,
that means group 1 = channel 1 + channel 3,

we can record group 1 = 100%, everything else 0%, and "evaluate" state to be channel 1 = 100%, channel 3 = 0%
 
Group + value

functions include

list of groups,
list of channels,
fade up
fade down
cueName
(cue number? or store in cue list?)

fromJson()
toJson()
'''

def fromDict(data):
    #return Cue(data['mappings'],data['fadeTimes'],data['name'])
    return None #todo!
    
class Cue(object):
    def __init__(self, mappings, fadeTimes, name = None):
        self.mappings = {}
        self.name = name
        self.upTIme = fadeTimes[0]
        self.downTime = fadeTimes[1]
        
    def toDict(self):
        pass
    