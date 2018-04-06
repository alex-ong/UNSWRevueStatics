DEBOUNCE_TIME = 0.005 # five milliseconds
# DEBOUNCE_TIME = 1.000
import time
'''
########################################################
# Button Debouncer - will lag-lessly send buttonDown, 
# but will have a debounced buttonUp
########################################################
'''
class ButtonDebouncer(object):
    def __init__(self, buttonName, onChange):
        self.buttonName = buttonName
        self.onChange = onChange
        self.lastButtonDownTime = None
        self.lastInput = None
        self.outputValue = None
    
    def update(self, timeStamp):
        # updates are used purely for buttonUp events
        if (self.lastButtonDownTime is not None and 
            (timeStamp - DEBOUNCE_TIME) > self.lastButtonDownTime):
            if self.lastInput == False and self.outputValue != False:
                self.outputValue = False
                self.onChange(self.buttonName, self.outputValue)
    
    # can immediately fire buttonDown
    def receiveInput(self, value, timeStamp):        
        if (value):  # received buttonDown
            if self.outputValue is None or self.outputValue == False:
                self.outputValue = True
                self.lastInput = True
                self.lastButtonDownTime = timeStamp
                self.onChange(self.buttonName, value)
            else:
                self.lastInput = value
        else:  # received buttonUp
            self.lastInput = False
            
                
def _testPrint(buttonName, value):
    print ("EVENT:", buttonName, value, time.time())
    
def _testKey(debouncer, value):
    # print ('Raw:', debouncer.buttonName, value)
    debouncer.receiveInput(value, time.time())
    
    
if __name__ == '__main__':
    # change DEBOUNCE_TIME to 1 or 2 seconds!    
    import tkinter as tk
    root = tk.Tk()
    buttonDebouncer = ButtonDebouncer('a', _testPrint)    
    root.bind("<KeyPress-a>", lambda e: _testKey(buttonDebouncer, True))
    root.bind("<KeyRelease-a>", lambda e: _testKey(buttonDebouncer, False))
    while True:
        buttonDebouncer.update(time.time())
        root.update_idletasks()
        root.update()
