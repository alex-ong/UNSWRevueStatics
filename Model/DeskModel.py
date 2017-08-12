'''
@author: alex-ong
@date 2017-05-07
'''
from . import ChannelValues
from . import GroupValues
from . import FaderValues

import Model.Configuration.ConfigReader as ConfigReader
from . import Programmer
from . import Console
from . import CueList
from . import OptionButtons
from . import ModalContainer
from _collections import OrderedDict

from .CueList import PLAYBACK_COMMANDS
from Model.ModalForms.ModalFormConsts import MENU_MODAL

#validOperators for main console
from Model.CommandProgrammer.MainConsole import validOperators 

class DeskModel(object):
    def refreshGroupBindings(self):
        self.groupBindings = self.config.readGroupBindings(self.settings['faders']*2) 
        self.groupValues.refreshGroupBindings(self.groupBindings, self.channelValues)
        
    def __init__(self):
        self.config = ConfigReader.ConfigReader('config/config.json')
        self.settings = self.config.readGeneralSettings()
        numFaders = self.settings['faders']
        defaultChannels = self.settings['defaultChannels']
        
        self.patching = self.config.readDMXBindings(defaultChannels)
        self.faderBindings = self.config.readFaderBindings(numFaders, defaultChannels)
        self.groupBindings = self.config.readGroupBindings(numFaders*2)
        self.channelValues = ChannelValues.ChannelValues(self.patching)    
        self.groupValues = GroupValues.GroupValues(self.groupBindings, self.channelValues)
        
        self.currentfaderBinding = self.settings['lastFaderPage'] 
        self.faderValues = FaderValues.FaderValues(self.getFaderBindings())
        cueListData = self.config.readCueList()
        
        try:
            upDown = self.settings['upDown']
        except KeyError:
            upDown = ["2", "1"]
            self.settings['upDown'] = upDown
            self.saveSettings()
            
        self.cueList = CueList.fromDict(cueListData, self.groupValues,
                                        self.channelValues, self.config.writeCueList,
                                        upDown)
       
        self.modals = ModalContainer.ModalList(self)     
        
        self.programmer = Programmer.Programmer(self.cueList,
                                                self.faderValues,
                                                self.groupValues,
                                                self.channelValues,
                                                self.modals)
        
        self.console = Console.Console(self.programmer, validOperators)
        self.optionButtons = OptionButtons.OptionButtons()
        
        
    
    def saveSettings(self):
        self.config.writeGeneralSettings(self.settings)
        
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
            
    def handleButtonInput(self, buttonName, buttonPressed):
        if not self.modals.isEmpty():
            if buttonPressed:
                self.modals.handleInput(buttonName)
        else:
            if 'b_slider' in buttonName:  # todo check programmer state first.
                faderNumber = int(buttonName.replace('b_slider', ''))
                bindings = self.faderBindings[self.currentfaderBinding]
                toChange = bindings[faderNumber]
                
                if buttonPressed: 
                    value = 100
                else:
                    value = 0
                    
                if isinstance(toChange, int):  # slider bound to channel            
                    self.channelValues[toChange].setDirectFlashValue(value)                
                else:  # slider bound to group
                    groupNumber = int(toChange.replace('group', ''))
                    self.groupValues[groupNumber].setDirectFlashValue(value)
                           
            elif buttonPressed:  # we only care about keyDown
                #first, switch S1->S4 to proper names
                if buttonName in OptionButtons.RAW_BUTTONS:
                    buttonName = self.optionButtons.getCommand(buttonName)
                
                #now, if it's a playback command handle it
                if buttonName in PLAYBACK_COMMANDS:
                    self.handlePlaybackCommand(buttonName)
                elif buttonName in FADER_COMMANDS:
                    pass #todo add fader commands                
                else: #otherwise we add the command to console
                    self.handleConsoleInput(buttonName)                    
            
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
        result = self.console.parseString(stringInput)
        return result
        
    def handlePlaybackCommand(self, buttonName):
        self.cueList.handleCueCommand(buttonName)
    
    def update(self, timeDelta):
        self.cueList.update(timeDelta)
        
    def popModalStack(self, modal):
        self.modalStack.pop()
        
    def addModalToStack(self, modal):
        self.modalStack.append(modal)
        
    #assumes up and down times as strings
    def updateFadeTimes(self, up, down):                
        upDown = [up, down]
        self.settings['upDown'] = upDown
        self.saveSettings()
        self.cueList.changeDefaultCueTime(upDown)
    
    def deleteAllCues(self):
        self.cueList.deleteAllCues()