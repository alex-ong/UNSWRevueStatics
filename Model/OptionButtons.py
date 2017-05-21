'''
File that lets you know the bindings for the S1->S4 buttons
'''
RAW_BUTTONS = ['S1', 'S2', 'S3', 'S4']


DELETE = 'Delete'
NEXT_FADERS = 'NextFaders'
PREV_FADERS = 'PrevFaders'

enumToNiceText = {DELETE: 'Delete',
                  NEXT_FADERS: 'Next Faders',
                  PREV_FADERS: 'Prev Faders',
                  None: ''}



MAIN_STATE =   [PREV_FADERS, NEXT_FADERS, DELETE, None]

class OptionButtons(object):
    def __init__(self):
        self.currentState = MAIN_STATE
    
    def setState(self, state):
        self.currentState = state
            
    def getCommand(self, rawButton):
        index = int(rawButton.replace('S','')) - 1        
        return self.currentState[index]
    
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