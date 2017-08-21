'''
File that lets you know the bindings for the S1->S4 buttons
'''

RAW_BUTTONS = ['S1', 'S2', 'S3', 'S4']


from Model.CommandProgrammer.parser import DELETE
from Model.FaderValues import NEXT_FADERS, PREV_FADERS
FADER = 'Fader'
enumToNiceText = {DELETE: 'Delete',
                  NEXT_FADERS: 'Next Faders',
                  PREV_FADERS: 'Prev Faders',
                  FADER: 'Fader',
                  None: ''
                  }



MAIN_STATE =   [PREV_FADERS, NEXT_FADERS, None, None]
FADER_BINDING_STATE = [PREV_FADERS, NEXT_FADERS, FADER, None]
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
        print ("Setting optionButtonBindings to", state)
        self.currentState = state
            
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