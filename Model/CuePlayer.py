'''
class that play a cue
'''

class PlayableCue(object):
    MODE_NONE = -1
    MODE_PLAY = 0
    MODE_STOP = 1
    
    def __init__(self, cue):
        self.target = cue.upTIme
        self.mode = PlayableCue.MODE_NONE
        
    def play(self):
        self.mode = PlayableCue.MODE_PLAY
        self.target = cue.upTIme
        
    def update(self, deltaTime):
        if self.playing:
            self.timer += deltaTime
             
class CuePlayer(object):
    def __init__(self, groupValues, cueValues):
        self.currentCues = []
        
    def playCue(self,cue):
        self.currentCues.append
        
    def update(self, deltaTime):
        pass