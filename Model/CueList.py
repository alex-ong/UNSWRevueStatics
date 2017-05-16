'''
@author: alex-ong
@date 2017-05-07
'''
from Model.CuePlayer import CuePlayer
import Model.Cue as Cue

import libs.string_decimal as string_decimal
from libs.sorted_containers.sorteddict import SortedDict 
def fromDict(data, groupValues, cueValues):
    parsedData = SortedDict()
    for key in data:
        newKey = string_decimal.fromStr(key)
        cueData = data[key]
        parsedData[newKey] = Cue.fromDict(cueData)
    return CueList(parsedData,groupValues,cueValues)

class CueList(object):
    def __init__(self, sortedDict, groupValues, cueValues):
        self.data = sortedDict
        self.player = CuePlayer(groupValues, cueValues)
        self.currentCue = self.data.keys()[0]
        
    def toDict(self):
        result = collections.OrderedDict()
        for key in self.data:
            result[str(key)] = self.data[key]
        return result
            