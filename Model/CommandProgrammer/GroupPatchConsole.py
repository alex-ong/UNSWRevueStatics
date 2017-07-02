from .parser import (RECORD, THRU, GROUP, CHANNEL, CUE, FADER, AT,
                    PLUS, MINUS, NUMBER, DECIMAL, DELETE, FULL,
                    tryParseInt, subContains)

# supported commands
# Record Group x
# Delete Group x

# Channel x @ z
# - ability to support +, -, THRU commands

def validOperators(program):      
    if len(program) == 0:
        return [CHANNEL, RECORD, DELETE]
    elif (RECORD in program) or (DELETE in program):
        if (GROUP not in program):
            return [GROUP]
        else:
            return [NUMBER]
    else: #len program >= 1
        lastSymbol = program[-1]
        if AT in program:
            return [NUMBER]
        else: #no at in program yet
            if lastSymbol == CHANNEL:
                return [NUMBER]
            elif tryParseInt(lastSymbol):
                result = [NUMBER, PLUS, MINUS, AT]
                # can't have thru if thru was prev operator
                # THRU CHANNEL 1
                #  -3   -2     -1 
                if (len(program) < 3 or 
                    (len(program) >= 3 and program[-3] != THRU)):
                    result.append(THRU)
                return result
            elif (lastSymbol == PLUS or 
                  lastSymbol == MINUS or 
                  lastSymbol == THRU):                
                return [CHANNEL]
            