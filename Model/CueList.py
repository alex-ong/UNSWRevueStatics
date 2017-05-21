'''
@author: alex-ong
@date 2017-05-07
'''
from Model.CuePlayer import CuePlayer
from Model.CommandProgrammer.parser import CUE, tryParseInt
import Model.Cue as Cue
import collections
import libs.string_decimal as string_decimal
from libs.sorted_containers.sorteddict import SortedDict 

def fromDict(data, groupValues, channelValues, saveFunc, upDown):
    parsedData = SortedDict()
    for key in data:
        newKey = string_decimal.fromStr(key)
        cueData = data[key]
        parsedData[newKey] = Cue.fromDict(cueData)
    return CueList(parsedData, groupValues, channelValues, saveFunc, upDown)


def alterPivot(listLen, numIndices, index, fromEnd):
    endIndex = index + fromEnd
    startIndex = index - numIndices + fromEnd
    while endIndex > listLen:
        endIndex -= 1
        startIndex -= 1
    while startIndex < 0:
        startIndex += 1
        endIndex += 1
    return (startIndex, endIndex)

NEXT = 'Next'
BACK = 'Back'
RELEASE = 'Release'
PLAYBACK_COMMANDS = [NEXT, BACK, RELEASE]

class CueList(object):
    def __init__(self, sortedDict, groupValues, channelValues, saveFunc, defaultUpDown):
        self.data = sortedDict
        self.player = CuePlayer(groupValues, channelValues)
        self.defaultUpDown = defaultUpDown
        self.currentCue = None
        if len(self.data.keys()) > 0:
            self.currentCue = self.data.keys()[0]        
            
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
                mappings['group' + str(group.number)] = value
                
        for channel in self.channelValues.values.values():
            value, _ = channel.getCueValueAndReason()
            if value > 0:
                mappings[channel.number] = value
        
        cue = Cue.Cue(mappings, self.defaultUpDown)
        cueIndex = cueName.replace(CUE, '')
        cueIndex = string_decimal.fromStr(cueIndex)
        self.data[cueIndex] = cue        
        self.saveFunc(self.toDict())
        if self.currentCue is None:
            self.currentCue = cueIndex
        
    def getCues(self, numCues, fromEnd):
        # return numCues, with current being one from the end.
        if len(self.data) == 0:            
            return [[], None]
        else:
            allKeys = list(self.data.keys())
            # first, collect numCues cues...
            if len(self.data) < numCues:
                resultKeys = allKeys                
            else:
                pivotIndex = allKeys.index(self.currentCue)
                startIndex, endIndex = alterPivot(len(allKeys), numCues, pivotIndex, fromEnd)                 
                resultKeys = allKeys[startIndex:endIndex]
            
            indexCurrent = resultKeys.index(self.currentCue)
            
            finalResult = [[], indexCurrent]
            for key in resultKeys:
                finalResult[0].append([key, self.data[key]])
                
            return finalResult
                    
    def handleCueCommand(self, commandName):        
        if commandName == NEXT:
            self.player.playCue(self.data[self.currentCue])
            allKeys = self.data.keys()
            index = allKeys.index(self.currentCue)            
            self.currentCue = allKeys[min(index + 1, len(allKeys) - 1)]
        elif commandName == BACK:            
            allKeys = self.data.keys()
            index = allKeys.index(self.currentCue)            
            self.currentCue = allKeys[max(index - 1, 0)]
        elif commandName == RELEASE:
            self.player.release()
        else:
            print ('Unhandled Cue command:', commandName)
    
    def update(self, timeDelta):
        updateVals = self.player.update(timeDelta)        
        for binding, value in updateVals.items():
            if tryParseInt(binding):
                channelNumber = int(binding)
                self.channelValues[channelNumber].setPlaybackValue(value)
            else:
                groupNumber = int(binding.replace('group',''))
                self.groupValues[groupNumber].setPlaybackValue(value)
    
    
    def changeUpDown(self, upDown):
        self.defaultUpDown = upDown
        
    def changeCueTiming(self, cueNumber, up, down):
        pass  # TODO
    
    def goto(self, target):
        target = string_decimal.fromStr(target)
        if target in self.data:
            self.currentCue = target
            return 'Successfully jumped to cue: ' + str(target)
        else:
            return 'Error; Cue does not exist: ' + str(target)
    
if __name__ == '__main__':
    for i in range(10):
        print(alterPivot(10, 6, i, 4), i)
    
