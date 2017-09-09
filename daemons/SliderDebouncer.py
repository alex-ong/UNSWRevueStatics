DEBOUNCE_TIME = 0.005  # five milliseconds
# DEBOUNCE_TIME = 1.000
import time
'''
########################################################
# Slider Debouncer stub
########################################################
'''
class SliderDebouncer(object):
    def __init__(self, sliderName, onChange):
        self.sliderName = sliderName
        self.onChange = onChange
        self.lastButtonDownTime = None
        self.lastInput = None
        self.outputValue = None
    
    def update(self, timeStamp):
        pass
    
    # can immediately fire buttonDown
    def receiveInput(self, value, timeStamp):            
        self.onChange(value, self.sliderName)            
        