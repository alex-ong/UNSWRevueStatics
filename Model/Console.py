'''
Our tokenizer.
Can receive arbitrary strings, and then attempt to tokenize them and parse them...
'''
from Model.CommandProgrammer.parser import (RECORD, THRU, GROUP, CHANNEL, CUE, FADER, AT,
                                            PLUS, MINUS, NUMBER, DECIMAL, DELETE, FULL,
                                            tryParseInt, subContains,
    validOperators)
from Model.CommandProgrammer.parser import validOperators

BACKSPACE = '<-'
CLEAR = 'Clear'
                        
class Console(object):
    def __init__(self):
        self.tokens = []
    
    # returns autocomplete, if_error, and a list of strings
    def getTokens(self):
        result = self.tokens.copy()
        autocomplete = validOperators(result)
        if_error = False  # todo call parser and get command or error
        return (result, if_error, autocomplete)
    
    def handleBackspace(self):
        if len(self.tokens) > 0:
            if tryParseInt(self.tokens[-1]):
                newInt = self.tokens[-1][:-1]
                if len(newInt) == 0:
                    self.tokens = self.tokens[:-1]
                else:
                    self.tokens[-1] = newInt
            else:
                self.tokens = self.tokens[:-1]
    def checkValidOperator(self, string, operators):
        if tryParseInt(string) and NUMBER in operators:
            return True
        else:
            return string in operators
        
    def parseString(self, string):        
        if string == BACKSPACE:
            self.handleBackspace()
            return
        
        if string == CLEAR:
            self.tokens = []
            #self.programmer.clear() #todo: implement
            return
            
        # split into more tokens, or add as a token. or do conversion.
        # have to deal with lack of channel key... When we receive ints,
        # we have to decide whether to combine ints, or add "Channel" in front of it.
        if self.checkValidOperator(string,validOperators(self.tokens)):
            if tryParseInt(string) and tryParseInt(self.tokens[-1]):
                self.tokens[-1] = self.tokens[-1] + string
            else:
                self.tokens.append(string)
        else: 
            if tryParseInt(string):
                #need to insert channel or group.
                if len(self.tokens) == 0:
                    self.tokens.append(CHANNEL)
                    self.tokens.append(string)
                elif self.tokens[-1] == THRU:
                    self.tokens.append(self.tokens[-3])
                    self.tokens.append(string)
                elif self.tokens[-1] in [PLUS, MINUS]:
                    self.tokens.append(CHANNEL)
                    self.tokens.append(string)
            else:
                print('Tried to enter ', string, 
                      'but valid operators are:', 
                      validOperators(self.tokens))
             
            
    # called when user hits clear 
    def reset(self):
        self.tokens = []
        
