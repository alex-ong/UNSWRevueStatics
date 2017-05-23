from .parser import (RECORD, THRU, GROUP, CHANNEL, CUE, FADER, AT,
                    PLUS, MINUS, NUMBER, DECIMAL, DELETE, FULL,
                    tryParseInt, subContains)

# we could use this function in future to provide auto-complete features...
def validOperators(program):
    # TODO: complete this...
        
    if len(program) == 0:
        return [AT, RECORD, GROUP, CUE, CHANNEL, DELETE]
    
    lastSymbol = program[-1]
    
    if program[0] == RECORD:  # program starts with RECORD
        if len(program) == 1:
            return [GROUP, CUE, FADER]
        elif len(program) == 2:            
            return [NUMBER]
        elif program[-2] == CUE:
            return [NUMBER,DECIMAL]
        elif program[-1] == DECIMAL:
            return [NUMBER]
        else:
            return [NUMBER]
    elif program[0] == DELETE:
        if len(program) == 1:
            return [GROUP, CUE, FADER]
        elif len(program) == 2:            
            return [NUMBER]
        elif program[-2] == CUE:
            return [NUMBER,DECIMAL]
        elif program[-1] == DECIMAL:
            return [NUMBER]
        else:
            return [NUMBER]
        
    elif lastSymbol == AT:  # program ends with @
        return [NUMBER, FULL]
    elif AT in program:  # we are at [expression] @ number
        if lastSymbol == FULL:
            return []
        else:
            return [NUMBER]
    else:  # assume no @ in program
        if lastSymbol in [GROUP, CUE, CHANNEL]:
            return [NUMBER]
        elif tryParseInt(lastSymbol):  # isNumber
            if program[-2] in [GROUP, CHANNEL]:
                return [NUMBER, THRU, PLUS, MINUS, AT]
            elif program[-2] == CUE:
                return [NUMBER, DECIMAL]
            else:
                return [NUMBER]           
        elif lastSymbol == THRU:
            return [program[-3]]
        elif lastSymbol == PLUS:
            return [GROUP, CHANNEL]
        elif lastSymbol == MINUS:
            return [GROUP, CHANNEL]
        elif lastSymbol == DECIMAL:
            return [NUMBER]
    print ("Please fix me. unhandled lastOperator situation:", program)
            
        