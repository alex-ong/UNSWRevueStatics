from .parser import (RECORD, THRU, GROUP, CHANNEL, CUE, FADER, AT,
                    PLUS, MINUS, NUMBER, DECIMAL, DELETE, FULL,
                    tryParseInt, subContains)

#we just want channel @ dmx

def validOperators(program):      
    if len(program) == 0:
        return [CHANNEL]    
    elif len(program) == 1:
        return [AT]
    else:
        return [NUMBER]
        
    