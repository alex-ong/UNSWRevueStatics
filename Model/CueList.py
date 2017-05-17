'''
@author: alex-ong
@date 2017-05-07
'''
from Model.CuePlayer import CuePlayer
from Model.CommandProgrammer.parser import CUE
import Model.Cue as Cue
import collections
import libs.string_decimal as string_decimal
from libs.sorted_containers.sorteddict import SortedDict 

def fromDict(data, groupValues, channelValues, saveFunc):
    parsedData = SortedDict()
    for key in data:
        newKey = string_decimal.fromStr(key)
        cueData = data[key]
        parsedData[newKey] = Cue.fromDict(cueData)
    return CueList(parsedData, groupValues, channelValues, saveFunc)

class CueList(object):
    def __init__(self, sortedDict, groupValues, channelValues, saveFunc, defaultUpDown = [2.0,0.0]):
        self.data = sortedDict
        self.player = CuePlayer(groupValues, channelValues)
        self.defaultUpDown = defaultUpDown
        if len(self.data.keys()) > 0:
            self.currentCue = self.data.keys()[0]
        else: 
            self.currentCue = None
        self.groupValues = groupValues
        self.channelValues = channelValues 
        self.saveFunc = saveFunc
        
    def toDict(self):
        result = collections.OrderedDict()
        for key in self.data:
            result[str(key)] = self.data[key].toDict()
        return result
            
    def recordCue(self, cueName):
        mappings = collections.OrderedDict()
        for group in self.groupValues.values.values():            
            value, _ = group.getCueValueAndReason()            
            if value > 0:
                mappings['group'+str(group.number)] = value
                
        for channel in self.channelValues.values.values():
            value, _ = channel.getCueValueAndReason()
            if value > 0:
                mappings[channel.number] = value
        
        cue = Cue.Cue(mappings, self.defaultUpDown)
        cueIndex = cueName.replace(CUE,'')
        cueIndex = string_decimal.fromStr(cueIndex)
        self.data[cueIndex] = cue        
        self.saveFunc(self.toDict())
        
