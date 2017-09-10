'''
File that lets you know the bindings for the S1->S4 buttons
'''

RAW_BUTTONS = ['S1', 'S2', 'S3', 'S4']


from Model.CommandProgrammer.parser import DELETE, NAME, SUCK
from Model.FaderValues import NEXT_FADERS, PREV_FADERS
EXIT2 = 'Exit2'

FADER = 'Fader'
MORE_OPTIONS = 'MoreOptions'
enumToNiceText = {DELETE: 'Delete',
                  NEXT_FADERS: 'Next Faders',
                  PREV_FADERS: 'Prev Faders',
                  FADER: 'Fader',
                  NAME: 'Name',
                  EXIT2: 'Cancel', #used for textEntry only
                  MORE_OPTIONS: 'More Options...',
                  SUCK: 'Suck',
                  None: ''                  
                  }



MAIN_STATE =  [PREV_FADERS, NEXT_FADERS, NAME, MORE_OPTIONS]
MAIN_STATE2 = [SUCK, None, None, MORE_OPTIONS]
FADER_BINDING_STATE = [PREV_FADERS, NEXT_FADERS, FADER, None]
TEXT_ENTRY_STATE = [EXIT2, None, None, None]
NO_BINDINGS = [None, None, None, None]
#globals are bad, mmkay?
_instance = None
def getInstance():
    global _instance
    if _instance is None:
        _instance = OptionButtons()
    return _instance

class OptionButtons(object):
    def __init__(self):
        self.currentState = MAIN_STATE
        if _instance is not None:
            raise ValueError("Please use getInstance. Do not directly construct this class")
    
    def setState(self, state):        
        self.currentState = state
            
    def cycleMainState(self):
        if self.currentState == MAIN_STATE:
            self.currentState = MAIN_STATE2
        else:
            self.currentState = MAIN_STATE
            
    def getCommand(self, rawButton):
        index = int(rawButton.replace('S','')) - 1        
        return self.currentState[index]
    
    def getCurrentState(self):
        return self.currentState
    
    def getNiceText(self):        
        result = []
        for item in self.currentState:
            result.append(enumToNiceText[item])            
        return result
        
if __name__ == '__main__':
    ob = OptionButtons()
    print(ob.getCommand('S1'))
    print(ob.getCommand('S2'))
    print(ob.getCommand('S3'))
    print(ob.getCommand('S4'))
    
    print(ob.getNiceText())