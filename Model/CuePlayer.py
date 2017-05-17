'''
class that play a cue
'''
import math
from Model.ChannelValues import ChannelValues

def clamp(minimum, maximum, x):
    return max(minimum, min(x, maximum))

class PlayableCue(object):
    MODE_NONE = -1
    MODE_PLAY = 0
    MODE_STOP = 1
    
    def __init__(self, cue, onFinished):
        self.target = cue.upTime
        self.mode = PlayableCue.MODE_NONE
        self.cue = cue
        self.onFinished = onFinished
        self.timer = 0.0
        
    def play(self):
        self.mode = PlayableCue.MODE_PLAY
        self.target = self.cue.upTime
        
    def stop(self):
        self.mode = PlayableCue.MODE_STOP
        newTarget = self.cue.downTime
        startValue = (1.0 - self._perc()) * newTarget
        self.timer = startValue
        self.target = newTarget
          
    def update(self, deltaTime):
        if self.mode == PlayableCue.MODE_PLAY:
            self.timer += deltaTime
            self.timer = clamp(0.0, self.target, self.timer)
        elif self.mode == PlayableCue.MODE_STOP:
            self.timer += deltaTime
            self.timer = clamp(0.0, self.target, self.timer)
            if self._perc() == 1.0:
                self.onFinished(self)
                
    def _perc(self):
        return self.timer / self.target
    
    def getValues(self):
        result = self.cue.getValues()
        multiplier = self._perc()
        if self.mode == PlayableCue.MODE_STOP:
            multiplier = 1.0 - multiplier
        for key, value in result.items():
            result[key] = round(value * multiplier) 
        return result
    
class CuePlayer(object):
    def __init__(self, groupValues, channelValues):
        self.currentCues = []
        self.groupValues = groupValues
        self.channelvalues = channelValues
    def removeCue(self, cue):
        try:
            index = self.currentCues.index(cue)
            del self.currentCues[index] 
        except:
            pass
        
    def playCue(self, cue):
        self.currentCues.append(PlayableCue(cue, self.removeCue))
        
    def update(self, deltaTime):
        for cue in self.currentCues:
            cue.update(deltaTime)
        
        # create group/channel playback dict
        finalValues = { key:0 for key in self.groupValues.values.keys()}
        finalValues2 = { key:0 for key in self.channelValues.values.keys()}
        finalValues.update(finalValues2)
        for cue in self.currentCues:
            cueValues = cue.getValues()
            for key, value in cueValues.items():
                finalValues[key] = max(finalValues[key], value)
        
        return finalValues
        
        
                        
