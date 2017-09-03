from .parser import (RECORD, THRU, GROUP, CHANNEL, CUE, FADER, AT,
                    PLUS, MINUS, NUMBER, DECIMAL, DELETE, FULL, TIME, NAME,
                    tryParseInt, subContains)

# we could use this function in future to provide auto-complete features...
def validOperators(program):
    # TODO: complete this...
        
    if len(program) == 0:
        return [AT, RECORD, GROUP, CUE, CHANNEL, DELETE, TIME, NAME]
    
    lastSymbol = program[-1]
    
    if program[0] == RECORD:  # program starts with RECORD
        if len(program) == 1:
            return [GROUP, CUE, FADER]
        elif len(program) == 2:            
            return [NUMBER]
        elif program[-2] == CUE:
            return [NUMBER, DECIMAL]
        elif program[-1] == DECIMAL:
            return [NUMBER]
        else:
            return [NUMBER]
    elif program[0] == DELETE:
        if len(program) == 1:
            return [GROUP, CUE]
        elif len(program) == 2:            
            return [NUMBER]
        elif program[-2] == CUE:
            return [NUMBER, DECIMAL]
        elif program[-1] == DECIMAL:
            return [NUMBER]
        else:
            return [NUMBER]
    elif program[0] == TIME:
        return []
    elif program[0] == NAME:
        if len(program) == 1:
            return [CUE, GROUP]
        elif len(program) == 2:            
            return [NUMBER]
        elif program[-2] == CUE:
            return [NUMBER, DECIMAL]
        elif program[-1] == DECIMAL:
            return [NUMBER]
        else:
            return [NUMBER]            
    elif lastSymbol == AT:  # program ends with @
        return [NUMBER, FULL]
    elif AT in program:  # we are at [expression] @ number
        if lastSymbol == FULL:
            return []
        elif tryParseInt(lastSymbol):
            return [NUMBER]
        else:
            return [FULL, NUMBER]
    else:  # assume no @ in program
        if lastSymbol in [GROUP, CHANNEL,CUE]:
            return [NUMBER]
                
        elif tryParseInt(lastSymbol):  # isNumber
            if program[-2] in [GROUP, CHANNEL]:
                result = [NUMBER, PLUS, MINUS, AT]
                # can't have thru if thru was prev operator
                # THRU CHANNEL 1
                #  -3   -2     -1 
                if (len(program) < 3 or 
                    (len(program) >= 3 and program[-3] != THRU)):
                    result.append(THRU)
                return result
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
            
        
