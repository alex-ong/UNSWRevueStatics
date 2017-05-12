'''
@author: alex-ong
@date 2017-05-07
Note: we don't have a tokenizer in our command programmer since we tokenize as we go.

inspired by:
http://effbot.org/zone/simple-top-down-parsing.htm
'''

token = None
next = None
   
def expression(rbp=0):
    global token
    t = token
    token = next()
    left = t.nud()
    while rbp < token.lbp:
        t = token
        token = next()
        left = t.led(left)
    return left

class literal_token:
    def __init__(self, value):
        self.value = int(value)
    def nud(self):
        return self.value
    
class operator_add_token:
    lbp = 10
    def led(self, left):
        right = expression(10)
        return left + right
    
class end_token:
    lbp = 0
    
#tokenizer. Convert from list of strings to tokens
def tokenize(program):
    for token in program:
        if token == '+':
            yield operator_add_token()
        else:
            yield literal_token(token)        
        #raise SyntaxError("unknown operator")
    yield end_token()

def parse(program):
    global token, next
    next = tokenize(program).__next__
    token = next()
    return expression()

if __name__ == '__main__':
    program = ['1','+','1']    
    print(parse(program))
    