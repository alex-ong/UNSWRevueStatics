'''
@author: alex-ong
@date 2017-05-07
Note: we don't have a tokenizer in our command programmer since we tokenize as we go.

inspired by:
http://effbot.org/zone/simple-top-down-parsing.htm
'''

from libs.sorted_containers.sortedset import SortedSet
from test.test_typechecks import Integer
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

    

class value_token:
    def __init__(self, value):
        self.value = value        
    def nud(self):
        return self.value
    
class collection_token:
    def __init__(self, value):
        self.value = SortedSet([value])        
    def nud(self):
        return self.value
                    
class operator_add_token:
    lbp = 20
    def led(self, left):
        right = expression(10)
        return left | right
    
class operator_sub_token:
    lbp = 20
    def led(self, left):
        right = expression(10)
        return left.difference(right)
    
class operator_thru_token:
    lbp = 30
    def led(self, left):
        right = expression(20)
        return evaluate_thru_value(left, right)
    
class operator_at_token:
    lbp = 10
    def led(self, left):
        right = expression(5)
        return evaluate_at_value(left, right)
    
    def nud(self):
        right = expression(5)
        return evaluate_at_value(None, right) 

class operator_record_token:
    lbp = 5        
    def nud(self):
        right = expression(5)
        return evaluate_record_value(right)
        
def splitLabelAndNumber(string):
    items = re.split('(\d+)', string)  # splits 'word123' into ['word','123','']
    return items[0], items[1]

def evaluate_thru_value(lo, hi):
    lo = lo[0]
    hi = hi[0]
    loType, loNum = splitLabelAndNumber(lo)
    hiType, hiNum = splitLabelAndNumber(hi)    
    
    if loType != hiType:
        raise ValueError('When using Thru, both sides must be the same type!')
    
    loNum = int(loNum)
    hiNum = int(hiNum)
    # make sure lo/hi are right way round
    loNum, hiNum = min(loNum, hiNum), max(loNum, hiNum) 
        
    result = SortedSet([(loType + str(num)) for num in range(loNum, hiNum + 1)])
    return result

def evaluate_at_value(left, right):
    # TODO: Unary operator.
    if left is None:
        return Command.SetCommand(right)
    else:
        return Command.SelectAndSetCommand(left, right)

def evaluate_record_value(right):    
    if isinstance(right, SortedSet):
        if len(right) > 1:
            raise ValueError('Record expects a SINGLE cue, group or fader!')
        else:
            return Command.RecordCommand(right)
    else:
        raise ValueError('Expected a cue, group or fader!')
        
class end_token:
    lbp = 0
    
def tryParseInt(token):
    try:
        int(token)
    except:
        return False
    return True

    
# tokenizer. Convert from list of strings to tokens
def tokenize(program):
    for token in program:
        if '+' == token:
            yield operator_add_token()
        elif '-' == token:
            yield operator_sub_token()
        elif '@' == token:
            yield operator_at_token()
        elif 'record' == token:
            yield operator_record_token()
        elif 'thru' == token:
            yield operator_thru_token()
        elif 'Group' in token:
            yield collection_token(token)
        elif 'Chan' in token:
            yield collection_token(token)
        elif tryParseInt(token):
            yield value_token(token)
        else:        
            raise SyntaxError("unknown operator")
    yield end_token()

def parse(program):
    global token, tokenGenerator
    tokenGenerator = tokenize(program)
    token = next(tokenGenerator)
    return expression()

def safeParse(program):
    try:
        printout = parse(program)
        return printout
    except Exception as e:        
        return str(e)
        
if __name__ == '__main__':
    program = ['Chan13', '+', 'Chan12', '@', '13']    
    print(safeParse(program))
    program = ['@', '10']    
    print(safeParse(program))
    program = ['record', 'Chan13']    
    print(safeParse(program))
    program = ['record', '1']    
    print(safeParse(program))
    
