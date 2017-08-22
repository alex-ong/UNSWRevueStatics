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
from . import DMXOutput
from _collections import OrderedDict

from .CueList import PLAYBACK_COMMANDS
from Model.ModalForms.ModalFormConsts import MENU_MODAL

#validOperators for main console
from Model.CommandProgrammer.MainConsole import validOperators 
from Model.FaderValues import FADER_COMMANDS, NEXT_FADERS, PREV_FADERS


class DeskModel(object):
    def __init__(self):
        self.config = ConfigReader.ConfigReader('config/config.json')
        self.settings = self.config.readGeneralSettings()
        numFaders = self.getNumFaders()
        defaultChannels = self.getDefaultChannels()
        
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
        
        self.finalDMXOutput = DMXOutput.DMXOutput(self) 
    
    def saveSettings(self):
        self.config.writeGeneralSettings(self.settings)
        
    def Reset(self):
        # get configReader to reset everything, then load everything
        pass
    
    ###############################################################
    # Model input handler - passes it to current modal if necessary
    ###############################################################         
    def handleSliderInput(self, sliderName, value):        
        if not (self.modals.isEmpty()):
            self.modals.handleSliderInput(sliderName, value)
        else:
            # get relevant slider
            bindings = self.faderBindings[self.currentfaderBinding]
            # get slider number        
            sliderNumber = int(sliderName.replace('slider', ''))
            
            # change value of group or channel, but only if binding isn't empty
            if sliderNumber in bindings:
                toChange = bindings[sliderNumber]                    
                if isinstance(toChange, int):  # slider bound to channel            
                    self.channelValues[toChange].setDirectValue(value)                
                else:  # slider bound to group
                    groupNumber = int(toChange.replace('group', ''))
                    self.groupValues[groupNumber].setDirectValue(value)
            
    def handleFlash(self, faderNumber, buttonPressed):
        bindings = self.faderBindings[self.currentfaderBinding]
        if faderNumber in bindings:
            toChange = bindings[faderNumber]        
            value = 100 if buttonPressed else 0        
                
            if isinstance(toChange, int):  # slider bound to channel            
                self.channelValues[toChange].setDirectFlashValue(value)                
            else:  # slider bound to group
                groupNumber = int(toChange.replace('group', ''))
                self.groupValues[groupNumber].setDirectFlashValue(value)

    def handleButtonInput(self, buttonName, buttonPressed):        
        # first, we remap virtual S1-S4 keys to current binding.        
        if buttonName in OptionButtons.RAW_BUTTONS:
            buttonName = OptionButtons.getInstance().getCommand(buttonName)
            if buttonName is None: #catch if we bound to nothing
                return
        
        if not self.modals.isEmpty():
            self.modals.handleInput(buttonName, buttonPressed)
        else:
            if 'b_slider' in buttonName:  # todo check programmer state first.
                faderNumber = int(buttonName.replace('b_slider', ''))
                self.handleFlash(faderNumber, buttonPressed)
            elif buttonPressed:  # we only care about keyDown
                #now, if it's a playback command handle it
                if buttonName in PLAYBACK_COMMANDS:
                    self.handlePlaybackCommand(buttonName)
                elif buttonName in FADER_COMMANDS:
                    self.handleFaderCommand(buttonName)                
                else: #otherwise we add the command to console
                    self.handleConsoleInput(buttonName)
    def handleFaderCommand(self, buttonName):
        if buttonName == NEXT_FADERS:
            self.nextFaderBindings()
        elif buttonName == PREV_FADERS:
            self.prevFaderBindings()
        else:
            print ("Unrecognized Fader Command", buttonName)         
    def handleConsoleInput(self, stringInput):
        result = self.console.parseString(stringInput)
        return result
        
    def handlePlaybackCommand(self, buttonName):
        self.cueList.handleCueCommand(buttonName)
                
    ################################
    # Change fader bindings
    ################################
    def nextFaderBindings(self):
        self.currentfaderBinding += 1
        if self.currentfaderBinding >= len(self.faderBindings):
            self.currentfaderBinding = 0
        self.refreshFaderBindings()
    
    def prevFaderBindings(self):
        self.currentfaderBinding -= 1
        if self.currentfaderBinding < 0:
            self.currentfaderBinding = len(self.faderBindings) - 1
        self.refreshFaderBindings()
        
    def getFaderBindings(self, pageNumber=None):
        if pageNumber is None:
            pageNumber = self.currentfaderBinding
                    
        bindings = self.faderBindings[pageNumber]
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
    
    ##################################
    #refresh bindings from file
    ##################################
    def refreshGroupBindings(self):
        self.groupBindings = self.config.readGroupBindings(self.getNumFaders()*2) 
        self.groupValues.refreshGroupBindings(self.groupBindings, self.channelValues)
    
    def refreshFaderBindings(self):
        self.faderBindings = self.config.readFaderBindings(self.getNumFaders(),self.getDefaultChannels())
        self.faderValues = FaderValues.FaderValues(self.getFaderBindings())
    
    def getFaderValues(self):
        return self.faderValues
    
    #################################    
    #Get desk properties from file
    #################################
    def getNumFaders(self):
        return self.settings['faders']
    
    def getDefaultChannels(self):
        return self.settings['defaultChannels']
    
    #################################
    # Update loop (called every 1/60s)
    #################################
    def update(self, timeDelta):
        self.cueList.update(timeDelta)
        
    #################################################
    # Add/remove current focus to another modal form
    ################################################
    def popModalStack(self, modal):
        self.modalStack.pop()
        
    def addModalToStack(self, modal):
        self.modalStack.append(modal)
        
    ###############################################
    # Main Menu command callbacks
    ###############################################
    def updateFadeTimes(self, up, down):                
        upDown = [up, down]
        self.settings['upDown'] = upDown
        self.saveSettings()
        self.cueList.changeDefaultCueTime(upDown)
    
    def deleteAllCues(self):
        self.cueList.deleteAllCues()
    
    ##############################################
    # Get Final Universe Output
    ##############################################
    def getDMXOutput(self):
        return self.finalDMXOutput.getOutput()
    