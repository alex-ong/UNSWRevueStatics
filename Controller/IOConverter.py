'''
@author alex-ong
@date 2017-05-14
Converts from polling based input to event based input.
'''

import threading

class Event(object):    
    def __init__(self, name):
        self.name = name
        
class SliderEvent(Event):
    def __init__(self, name, newValue):
        super().__init__(name)
        self.value = newValue
        
class ButtonEvent(Event):
    def __init__(self, name, down):
        super().__init__(name)
        self.down = down
        
class IOConverter(object):
    def __init__(self):
        self.lock = threading.Lock()
        self.currentState = {}
        self.unhandledEvents = {}
    
    def getEvents(self):
        self.lock.acquire()
        result = self.unhandledEvents
        self.unhandledEvents = {}
        self.lock.release()
        return result
    
    def handleChange(self, key, newValue):
        if key.startswith('slider'):        
            self.unhandledEvents[key] = SliderEvent(key, newValue)
        else: #button press
            if key in self.unhandledEvents:
                self.unhandledEvents[key].append(ButtonEvent(key,newValue))
            else:
                self.unhandledEvents[key] = [ButtonEvent(key,newValue)]                                            
        
    def addState(self, inputDict):
        self.lock.acquire()
        for key in inputDict:
            if key not in self.currentState:
                self.handleChange(key,inputDict[key])
            elif inputDict[key] != self.currentState[key]: #key is in both dicts                
                self.handleChange(key, inputDict[key])
        self.lock.release()