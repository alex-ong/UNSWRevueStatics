'''
Our tokenizer.
Can receive arbitrary strings, and then attempt to tokenize them and parse them...
'''
from Model.CommandProgrammer.parser import (RECORD, THRU, GROUP, CHANNEL, CUE, FADER, AT,
                                            PLUS, MINUS, NUMBER, DECIMAL, DELETE, FULL,
                                            tryParseInt, subContains)

from Model.CommandProgrammer.parser import safeParse
from Model.CommandProgrammer.Command import AbstractCommand, MenuCommand
from libs.string_decimal import string_decimal

BACKSPACE = '<-'
CLEAR = 'Clear'
ENTER = 'Enter'
MENU = 'Menu'
                    
class Console(object):
    def __init__(self, programmer, validOperators):
        self.tokens = []
        self.programmer = programmer
        self.validOperators = validOperators
        self.lastCommandResult = None
        
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
            self.lastCommandResult = None
            return
        
        if string == CLEAR:
            self.reset()
            return CLEAR
            
        if string == ENTER:
            result = safeParse(self.tokens)
            if isinstance(result, AbstractCommand): 
                result = self.programmer.handleCommand(result)
            elif isinstance(result, string_decimal):
                result = self.programmer.handleCommand(result)
            elif isinstance(result, int):                
                result = self.programmer.handleCommand(result)
            else:
                print ("unknown result:", result)
            self.lastCommandResult = result
            self.tokens = []
            return result
        
        if string == MENU:
            self.reset()
            self.tokens = []
            result = self.programmer.handleCommand(MenuCommand())
            return result
        
        # split into more tokens, or add as a token. or do conversion.
        # have to deal with lack of channel key... When we receive ints,
        # we have to decide whether to combine ints, or add "Channel" in front of it.
        validOps = self.validOperators(self.tokens)
        if self.checkValidOperator(string, validOps):
            if tryParseInt(string) and len(self.tokens) > 0 and tryParseInt(self.tokens[-1]):
                self.tokens[-1] = self.tokens[-1] + string
            else:
                self.tokens.append(string)
        elif len(validOps) > 0: 
            if tryParseInt(string):
                # need to insert channel or group.
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
                      self.validOperators(self.tokens))
        self.lastCommandResult = None     
            
    # called when user hits clear 
    def reset(self):
        self.tokens = []
        self.lastCommandResult = None
        self.programmer.clear()
        
