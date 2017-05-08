'''
@author: alex-ong
@date 2017-05-07
'''
from Model import ChannelValues
import Model.Configuration.ConfigReader as ConfigReader




class DeskModel(object):
    def __init__(self):
        self.config = ConfigReader.ConfigReader('config/config.json')
        self.settings = self.config.readGeneralSettings()
        numFaders = self.settings['faders']
        numChannels = self.settings['channels']
        
        self.patching = self.config.readDMXBindings(numChannels)
        self.faderBindings = self.config.readFaderBindings(numFaders, numChannels)
        self.groupBindings = self.config.readGroupBindings(numFaders)
        self.channelValues = ChannelValues.ChannelValues(self.patching)    
        
        self.currentfaderBinding = self.settings['lastFaderPage'] 
    def Reset(self):
        # get configReader to reset everything, then load everything
        pass
         
    def handleSliderInput(self, sliderName, value):
        # get relevant slider
        bindings = self.faderBindings[self.currentfaderBinding]
        # get slider number        
        sliderNumber = int(sliderName.replace('slider', ''))
        
        # change value of group or channel
        toChange = bindings[sliderNumber]
        
        # slider bound to channel
        if isinstance(toChange, int):            
            self.channelValues[toChange].setDirectValue(value)
        
        # slider bound to group
        else:
            pass