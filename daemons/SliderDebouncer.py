DEBOUNCE_TIME = 0.050  # fifty milliseconds
# DEBOUNCE_TIME = 1.000
import time
'''
########################################################
# Slider Debouncer stub
########################################################
'''
class SliderDebouncer(object):
    # assumes inputs from 0 to 100
      
    def __init__(self, sliderName, onChange):
        self.sliderName = sliderName
        self.onChange = onChange
        self.lastSliderInputTime = None
        self.lastInput = 0
        self.outputValue = 0        
        
    def update(self, timeStamp):
        if (self.lastSliderInputTime is not None and 
            (timeStamp - DEBOUNCE_TIME) > self.lastSliderInputTime):
            if self.lastInput != self.outputValue:
                self.outputValue = self.lastInput
                self.onChange(self.sliderName, self.outputValue)
                self.lastSliderInputTime = None
    
    # can immediately fire buttonDown
    def receiveInput(self, value, timeStamp):        
        if value == self.outputValue: #tail end of debounce. e.g. 0->1->0 where 1 was noise
            self.lastInput = value
            self.lastSliderInputTime = timeStamp
        else: #value is different to output!
            #this means new != last != output. We will send last and cache new
            if value != self.lastInput and self.lastInput != self.outputValue: 
                toSend = self.lastInput
                self.lastInput = value
                self.outputValue = toSend
                self.lastSliderInputTime = timeStamp            
                self.onChange(self.sliderName, value)
            #this means that new != last but last == output. We will add it to the updateQueue
            elif value != self.lastInput:
                self.lastInput = value                
                self.lastSliderInputTime = timeStamp                            
            else: 
                #this means that new == last but last != output. it could
                #be noise. We leave it to the update() loop to do the confirmation
                pass              
'''            
#######################################################
# Use this if you don't want debouncing enabled
#######################################################
'''
class SliderDebouncerPassthrough(object):
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
        self.onChange(self.sliderName, value)
