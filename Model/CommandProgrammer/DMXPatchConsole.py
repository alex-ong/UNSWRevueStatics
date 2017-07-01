from .parser import (RECORD, THRU, GROUP, CHANNEL, CUE, FADER, AT,
                    PLUS, MINUS, NUMBER, DECIMAL, DELETE, FULL,
                    tryParseInt, subContains)

# we just want channel @ dmx

# support Channel x @ y
# support Channel x THRU y @ z
# support Delete Channel x

def validOperators(program):      
    if len(program) == 0:
        return [CHANNEL, DELETE]
    elif len(program) == 1 and program[0] == DELETE:
        return [CHANNEL]
    elif program[0] == DELETE and len(program) >= 2:
        return [NUMBER]     
    elif len(program) == 2:
        return [NUMBER, AT, THRU]    
    elif program[-1] == THRU:
        return [CHANNEL]
    elif program[-1] == AT:
        return [NUMBER]    
    elif program[-1] == CHANNEL:
        return [NUMBER] 
    elif tryParseInt(program[-1]):
        if len(program) == 5:
            return [AT, NUMBER]
        else:
            return [NUMBER]    
    else:
        print ("WTF", program, len(program))
        return None
        
        
    
