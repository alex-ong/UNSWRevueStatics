'''
@author: alex-ong
@date 2017-05-07
'''
from Model import ChannelValues
from Model import GroupValues
from Model import FaderValues

import Model.Configuration.ConfigReader as ConfigReader
from Model import Programmer
from Model import Console

from _collections import OrderedDict

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
        self.groupValues = GroupValues.GroupValues(self.groupBindings, self.channelValues)
        
        self.currentfaderBinding = self.settings['lastFaderPage'] 
        self.faderValues = FaderValues.FaderValues(self.getFaderBindings())
        self.programmer = Programmer.Programmer()
        self.console = Console.Console()
            
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
                
        if isinstance(toChange, int):  # slider bound to channel            
            self.channelValues[toChange].setDirectValue(value)                
        else:  # slider bound to group
            groupNumber = int(toChange.replace('group', ''))
            self.groupValues[groupNumber].setDirectValue(value)
            
    
    def getFaderBindings(self):
        bindings = self.faderBindings[self.currentfaderBinding]
        result = OrderedDict()       
        
        for key, value in bindings.items():  # assume ordered dict.            
            if isinstance(value, int):
                result[key] = self.channelValues[value]
            elif 'group' in value:  # bind the group
                groupNumber = int(value.replace('group', ''))  
                result[key] = self.groupValues[groupNumber]
            else:
                print ("Error with fader bindings...")
                
        return result
    
    def handleConsoleInput(self, stringInput):
        self.console.parseString(stringInput)
        