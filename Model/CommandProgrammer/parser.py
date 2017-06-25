'''
@author: alex-ong
@date 2017-05-07
Note: we don't have a tokenizer in our command programmer since we tokenize as we go.

inspired by:
http://effbot.org/zone/simple-top-down-parsing.htm
'''

from Model.CommandProgrammer.Command import SelectCommand
from libs.string_decimal import string_decimal

token = None
tokenGenerator = None
import re

import Model.CommandProgrammer.Command as Command

def expression(rbp=0):
    global token, tokenGenerator
    t = token
    
    token = next(tokenGenerator)
    
    left = t.nud()
    while rbp < token.lbp:
        t = token
        token = next(tokenGenerator)
        left = t.led(left)
    return left


class time_token:  # just time by itself is a command
    def nud(self):
        return Command.TimeCommand()     
    
class value_token:  # basically just numbers
    def __init__(self, value):
        if value == FULL:
            self.value = 100
        else:
            self.value = int(value)
                
    def nud(self):        
        return self.value    
    
class abstract_operator_cgf_token:  # Channel/Group/Fader
    lbp = 90
    def getStartString(self):
        return ''    
    def nud(self):
        right = expression(90)
        if self.validateRight(right):
            return [self.getStartString() + str(right)]    
    def validateRight(self, value):        
        if tryParseInt(value):        
            return True
        raise ValueError('Expected integer after ' + self.getStartString())
    
class operator_channel_token(abstract_operator_cgf_token):
    def getStartString(self):
        return CHANNEL

class operator_group_token(abstract_operator_cgf_token):
    def getStartString(self):
        return GROUP    

class operator_fader_token(abstract_operator_cgf_token):
    def getStartString(self):
        return FADER        

class operator_cue_token():
    def getStartString(self):
        return CUE
    def nud(self):
        right = expression(90)    
        if (isinstance(right, int) or 
            isinstance(right, string_decimal)):
            return [self.getStartString() + str(right)]        

class collection_token:
    def __init__(self, value):
        self.value = [value]        
    def nud(self):
        return self.value
                    
class operator_add_token:
    lbp = 20
    def led(self, left):
        right = expression(10)
        result = left[:]
        for item in right:
            if item not in left:
                result.append(item)
        return result
    
class operator_sub_token:
    lbp = 20
    def led(self, left):
        right = expression(10)
        result = left[:]
        for item in right:
            if item in left:
                left.popitem(item)
        return result
    
class operator_thru_token:
    lbp = 30
    def led(self, left):
        right = expression(20)
        return evaluate_thru_value(left, right)

class operator_decimal_token:
    lbp = 100
    def led(self, left):
        if isinstance(left, int):
            right = expression(5)
            if isinstance(right, int):                
                return string_decimal(left, right)        
        raise ValueError('Decimal point only applicable with numbers!')
     
class operator_at_token:
    lbp = 10
    def led(self, left):
        # you an only use left if you are selecting groups/channels
        if isinstance(left, list):
            if not subContainsList(left, [FADER, CUE]):
                right = expression(5)
                return evaluate_at_value(left, right)       
        raise ValueError('@ can only be called with Channels and Groups!')
    def nud(self):
        right = expression(5)
        return evaluate_at_value(None, right) 

class operator_record_token:
    lbp = 5        
    def nud(self):
        right = expression(5)
        return evaluate_record_value(right)

class operator_delete_token:
    lbp = 5
    def nud(self):
        right = expression(5)
        return evaluate_delete_value(right)
    
def splitLabelAndNumber(string):
    items = re.split('(\d+)', string)  # splits 'word123' into ['word','123','']
    return items[0], items[1]

def evaluate_thru_value(lo, hi):
    applicable_thru = [GROUP, CHANNEL]
    lo = lo[0]
    hi = hi[0]
    loType, loNum = splitLabelAndNumber(lo)
    hiType, hiNum = splitLabelAndNumber(hi)    
    
    if loType != hiType:
        raise ValueError('When using Thru, both sides must be the same type!')
    if loType not in applicable_thru:
        raise ValueError('Thru can only be usd with Group or Chan!')
    loNum = int(loNum)
    hiNum = int(hiNum)
    # make sure lo/hi are right way round
    loNum, hiNum = min(loNum, hiNum), max(loNum, hiNum) 
        
    result = [(loType + str(num)) for num in range(loNum, hiNum + 1)]
    return result

def evaluate_at_value(left, right):
    # TODO: Unary operator.
    if left is None:        
        return Command.SetCommand(right)
    else:
        return Command.SelectAndSetCommand(left, right)

def evaluate_record_value(right):    
    if isinstance(right, list):
        if len(right) > 1:
            raise ValueError('Record expects a SINGLE cue, group or fader!')
        else:
            return Command.RecordCommand(right[0])
    else:
        raise ValueError('Record expects a Cue, Group, or Fader')

def evaluate_delete_value(right):
    if isinstance(right, list):
        if len(right) > 1:
            raise ValueError('Record expects a SINGLE cue, group or fader!')
        else:
            return Command.DeleteCommand(right[0])
    else:
        raise ValueError('Record expects a Cue, Group, or Fader')
class end_token:
    lbp = 0
    
def tryParseInt(token):
    try:
        int(token)
    except:
        return False
    return True

RECORD = 'Record'
THRU = 'Thru'
GROUP = 'Group'
CHANNEL = 'Channel'
CUE = 'Cue'
FADER = 'Fader'
AT = '@'
PLUS = '+'
MINUS = '-'
NUMBER = 'Number'
DECIMAL = '.'
DELETE = 'Delete'
FULL = 'Full'
TIME = 'Time'
    
# tokenizer. Convert from list of strings to tokens
def tokenize(program):
    for token in program:
        if PLUS == token:
            yield operator_add_token()
        elif MINUS == token:
            yield operator_sub_token()
        elif AT == token:
            yield operator_at_token()
        elif RECORD == token:
            yield operator_record_token()
        elif THRU == token:
            yield operator_thru_token()
        elif GROUP in token:
            yield operator_group_token()
        elif CHANNEL in token:
            yield operator_channel_token()
        elif CUE in token:
            yield operator_cue_token()
        elif FADER in token:
            yield operator_fader_token()
        elif DECIMAL == token:
            yield operator_decimal_token()
        elif DELETE == token:
            yield operator_delete_token()
        elif tryParseInt(token):
            yield value_token(token)
        elif FULL == token:
            yield value_token(token)
        elif TIME == token:
            yield time_token()
        else:        
            raise SyntaxError("unknown token")
    yield end_token()

def parse(program):
    global token, tokenGenerator
    tokenGenerator = tokenize(program)
    token = next(tokenGenerator)
    result = expression()
    # final check. If it's a set, we issue a selection
    if isinstance(result, list):
        return SelectCommand(result)
    else:
        return result

def safeParse(program):
    try:
        printout = parse(program)
        return printout
    except StopIteration:
        return 'Expression not finished'
    except Exception as e:        
        return str(e)
    

        
    
# e.g. checks if options('GROUP','FADER') are inside ['GROUP1','GROUP2'] etcc
def subContainsList(items, options):
    for item in items:
        result = subContains(item, options)
        if result is not None:
            return result
    return None

# e.g. checks if options('GROUP','FADER') are inside 'GROUP1' etc        
def subContains(item, options):
    for option in options:
        if option in item:
            return option
    return None
if __name__ == '__main__':
    program = [CHANNEL, '13', '+', CHANNEL, '14', '@', '13']    
    print(parse(program))
    program = ['@', '10']    
    print(parse(program))
    program = [RECORD, CHANNEL, '13']    
    print(parse(program))
    program = [RECORD, CHANNEL, '13', '.', '1']    
    print(safeParse(program))
    program = [RECORD, CHANNEL, '100', '.']
    print(safeParse(program))
    program = [RECORD, GROUP, '1', THRU, GROUP, '10']    
    print(safeParse(program))
    program = [RECORD, CUE, '1']   
    print(parse(program))
    program = [RECORD, CUE, '1', '.', '10']   
    print(parse(program))
    program = [CHANNEL, '5', THRU, CHANNEL, '1', AT, '10']
    print(parse(program))
    program = [CHANNEL, '20']
    print(parse(program))
    program = [CUE, '1', '.', '100']
    print(parse(program))
    program = [DELETE, CUE, '1', '.', '100']
    print(parse(program))
    program = [CUE, '1', AT, '100']
    print(safeParse(program))
