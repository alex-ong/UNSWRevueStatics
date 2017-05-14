'''
Our tokenizer.
Can receive arbitrary strings, and then attempt to tokenize them and parse them...
'''
from Model.CommandProgrammer.parser import (RECORD,THRU,GROUP,CHANNEL,CUE,FADER,AT,PLUS,MINUS,NUMBER,DECIMAL,DELETE,
    tryParseInt, subContains)
from Model.CommandProgrammer.parser import validOperators


class Console(object):
    def __init__(self):
        self.tokens = []
    
    #returns autocomplete, if_error, and a list of strings
    def getTokens(self):
        result = self.tokens.copy()
        autocomplete = validOperators(result)
        if_error = False #todo call parser and get command or error
        return (result,if_error,autocomplete)
    
    def parseString(self, string):
        #split into more tokens, or add as a token. or do conversion.
        # have to deal with lack of channel key... When we receive ints,
        # we have to decide whether to combine ints, or add "Channel" in front of it.
        if len(self.tokens) == 0:            
            if tryParseInt(string):
                self.tokens.append(CHANNEL)
                self.tokens.append(string)
            else:
                self.tokens.append(string)
        elif AT in self.tokens: #all number references can't be to channel
            pass
        else: #no at symbol yet
            if tryParseInt(string):
                if tryParseInt(self.tokens[-1]):
                    self.tokens[-1] = self.tokens[-1] + string
                elif self.tokens[-1] == DECIMAL:
                    self.tokens.append(string)
                elif subContains(string,[GROUP,CHANNEL,CUE,FADER]):
                    self.tokens.append(string)
                else:
                    self.tokens.append(CHANNEL)
                    self.tokens.append(string)                    
            else:
                self.tokens.append(string)
             
            
    #called when user hits clear 
    def reset(self):
        self.tokens = []
        