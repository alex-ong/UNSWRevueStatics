'''
a class for representing numbers like
1.111 perfectly

when sorted, 1.1 and 1.10 are different,with 1.10 > 1.9 > 1.1

@author alex-ong
@date 2017-05-14
'''
def fromStr(string):
    pairs = string.split('.')
    if len(pairs) > 1:
        return string_decimal(int(pairs[0]),int(pairs[1]))
    else:
        return string_decimal(int(pairs[0]),0)
        
    
# when sorting these (e.g. for cues), 1.10 > 1.9
class string_decimal(object):
    def __init__(self, base, mantissa):        
        self.base = base
        self.mantissa = mantissa        
    
    # when sorting, 1.10 is bigger than 1.1 and 1.9
    def __lt__(self, other):
        if other.base == self.base:
            return self.mantissa < other.mantissa
        else:
            return self.base < other.base
    
    def __gt__(self, other):
        if other.base == self.base:
            return self.mantissa > other.mantissa
        else:
            return self.base > other.base
        
    def __eq__(self, other):
        try:
            if isinstance(other, string_decimal):
                if (self.base == other.base and 
                    self.mantissa == other.mantissa):
                    return True
        except:
            pass
        return False
    
    def __ne__(self, other):
        return not self.__eq__(other)
    
    def __hash__(self):
        return hash((self.base,self.mantissa))
    
    def __str__(self):
        return str(self.base) + '.' + str(self.mantissa)