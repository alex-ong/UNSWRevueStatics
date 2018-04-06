'''
@author: alex-ong
@date 2017-05-07
'''

# a fader. Bound to a group or channel

class Fader(object):
    def __init__(self, number, binding):
        self.number = number
        self._binding = binding  # points to a channel or group
                    
    def getBinding(self):
        return self._binding
    
    def reset(self):
        self._binding.resetDirect()
