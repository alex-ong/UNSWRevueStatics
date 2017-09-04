'''
class that _play a cue
'''
import math
from Model.ChannelValues import ChannelValues

def clamp(minimum, maximum, x):
    return max(minimum, min(x, maximum))

def lerp(start, end, perc):
    return start + perc * (end - start)

def tryParseInt(token):
    try:
        int(token)
    except:
        return False
    return True
class PlayableCue(object):
    MODE_NONE = -1
    MODE_PLAY = 0
    MODE_STOP = 1
    
    def __init__(self, cue, currentState, onFinished):
        self.target = None
        self.mode = PlayableCue.MODE_NONE
        self.cue = cue
        self.cue.playableCue = self
        self.startState = self.copyCurrentState(currentState)
        self.onFinished = onFinished
        self.timer = 0.0        
        self._play()
        self.canRemove = False
    
    def copyCurrentState(self, currentState):
        result = {}    
        cueBindings = self.cue.getValues()
        for key in cueBindings:
            try:
                result[key] = currentState[key]
            except Exception as e:
                print(e)
        return result    
                
    def _play(self):
        self.mode = PlayableCue.MODE_PLAY
        self.target = self.cue.upTime.toFloat()    
            
    def stop(self):
        if self.mode != PlayableCue.MODE_STOP:
            self.mode = PlayableCue.MODE_STOP
            newTarget = self.cue.downTime.toFloat()
            startValue = (1.0 - self._perc()) * newTarget
            self.timer = startValue
            self.target = newTarget
            
            self.startState = self.cue.getValues().copy()
            for key, value in self.startState.items():
                self.startState[key] = 0
    
    def instantStop(self):
        self.stop()
        self.timer = self.target
        
    def update(self, deltaTime):
        if self.mode == PlayableCue.MODE_PLAY:            
            self.timer += deltaTime
            self.timer = clamp(0.0, self.target, self.timer)            
        elif self.mode == PlayableCue.MODE_STOP:
            self.timer += deltaTime
            self.timer = clamp(0.0, self.target, self.timer)
            if self._perc() == 1.0:
                self.cue.playableCue = None
                self.canRemove = True
                
    def _perc(self):
        if self.target == 0.0:
            return 1.0
        return self.timer / self.target
    
    def displayPerc(self):
        if self.mode == PlayableCue.MODE_PLAY:
            return self._perc()
        else:
            return 1.0 - self._perc()
        
    def getValues(self):
        result = self.cue.getValues().copy()
        perc = self._perc()
        if self.mode == PlayableCue.MODE_STOP:
            perc = 1.0 - perc
            
        for key, value in result.items():                
            startValue = self.startState[key]                
            result[key] = round(lerp(startValue, result[key], perc))
                 
        return result
    
class CuePlayer(object):
    def __init__(self, groupValues, channelValues):
        self.currentCues = []
        self.groupValues = groupValues
        self.channelValues = channelValues
    
    def _removeCue(self, cue):
        try:
            index = self.currentCues.index(cue)
            del self.currentCues[index] 
        except:
            pass
    
    def clear(self):
        for cue in self.currentCues:
            cue.stop()   
            
    def release(self):
        for cue in self.currentCues:
            cue.instantStop()
    
    def _currentValues(self):
        groupResult = self.groupValues.getCurrentPlaybackValues()
        channelResult = self.channelValues.getCurrentPlaybackValues()
        
        groupResult.update(channelResult)        
        return groupResult
        
    def playCue(self, cue):
        # if cue exists, play it
        exists = False        
        for playableCue in self.currentCues:
            if playableCue.cue == cue:                
                exists = True
                break
        
        if not exists:        
            # stop all existing cues
            # copy state before releasing...
            currentState = self._currentValues()
            self.clear()
            playableCue = PlayableCue(cue, currentState, self._removeCue)
            self.currentCues.append(playableCue)
        
    def update(self, deltaTime):
        # since self.currentCues is ordered, last cue value overrides previous cue values. 
        for cue in self.currentCues:
            cue.update(deltaTime)            
        
        # create group/channel playback dict
        finalValues = { 'group' + str(key):0 for key in self.groupValues.values.keys()}        
        finalValues2 = { key:0 for key in self.channelValues.values.keys()}
        finalValues.update(finalValues2)

        for cue in self.currentCues:
            cueValues = cue.getValues()
            for key, value in cueValues.items():
                if tryParseInt(key):  # handle channels
                    key = int(key)
                
                finalValues[key] = max(finalValues[key], value)
        
        for i in range (len(self.currentCues) - 1, -1, -1):
            if self.currentCues[i].canRemove:
                del self.currentCues[i]
        
        return finalValues
        
    
