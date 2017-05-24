from .parser import (RECORD, THRU, GROUP, CHANNEL, CUE, FADER, AT,
                    PLUS, MINUS, NUMBER, DECIMAL, DELETE, FULL,
                    tryParseInt, subContains)

#for cue up and down time, we just want decimals

def validOperators(program):
    # TODO: complete this...
        
    if len(program) == 0:
        return [NUMBER]
    
    lastSymbol = program[-1]
    if [DECIMAL] not in program:
        return [NUMBER, DECIMAL]
    else:
        return [NUMBER]
    