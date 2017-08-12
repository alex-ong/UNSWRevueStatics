from .parser import (RECORD, THRU, GROUP, CHANNEL, CUE, FADER, AT,
                    PLUS, MINUS, NUMBER, DECIMAL, DELETE, FULL,
                    tryParseInt, subContains)

# supported commands
# Record Fader x
# Delete Fader x
# Channel x
# Group x

#example usage:
# Channel 1
# Record Fader 1


def validOperators(program):      
    if len(program) == 0:
        return [CHANNEL, GROUP, RECORD, DELETE]
    elif (RECORD in program) or (DELETE in program):
        if (FADER not in program):
            return [FADER]
        else:
            return [NUMBER]
    else:
        return [NUMBER]