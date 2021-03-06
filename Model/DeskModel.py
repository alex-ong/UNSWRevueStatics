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
from . import GrandMaster
from . import SliderRemapper
from _collections import OrderedDict

from .CueList import PLAYBACK_COMMANDS
from Model.ModalForms.ModalFormConsts import MENU_MODAL

# validOperators for main console
from Model.CommandProgrammer.MainConsole import validOperators 
from Model.FaderValues import FADER_COMMANDS, NEXT_FADERS, PREV_FADERS
from Model.OptionButtons import MORE_OPTIONS
META_COMMANDS = [OptionButtons.MORE_OPTIONS]

class DeskModel(object):
    def __init__(self):
        self.notifyControllerReset = None
        self.Reset()
    
    def bindNotifyControllerReset(self, func):
        self.notifyControllerReset = func
            
    def Reset(self):
        self.config = ConfigReader.ConfigReader('config/config.json')
        self.settings = self.config.readGeneralSettings()
        numFaders = self.getNumFaders()
        defaultChannels = self.getDefaultChannels()
        
        self.patching = self.config.readDMXBindings(defaultChannels)
        self.faderBindings = self.config.readFaderBindings(numFaders, defaultChannels)
        self.groupBindings = self.config.readGroupBindings(numFaders * 2)
        self.channelValues = ChannelValues.ChannelValues(self.patching)    
        self.groupValues = GroupValues.GroupValues(self.groupBindings, self.channelValues)
        
        self.currentfaderBinding = self.settings['lastFaderPage'] 
        self.faderValues = FaderValues.FaderValues(self.getFaderBindings())
        cueListData = self.config.readCueList()
        
        try:
            upDown = self.settings['upDown']
        except KeyError:
            upDown = ["2", "0"]
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
                                                self.modals,
                                                self)
        
        self.console = Console.Console(self.programmer, validOperators)        
        
        self.grandMaster = GrandMaster.GrandMaster()
        self.finalDMXOutput = DMXOutput.DMXOutput(self) 
    
    ###############################################################
    # Model input handler - passes it to current modal if necessary
    ###############################################################         
    def handleSliderInput(self, sliderName, value):
        #first, rebind
        sliderName = SliderRemapper.instance().getSliderName(sliderName)                
        if not (self.modals.isEmpty()):
            self.modals.handleSliderInput(sliderName, value)
        else:
            # get relevant slider
            bindings = self.faderBindings[self.currentfaderBinding]
            # get slider number         
            try:
                sliderNumber = int(sliderName.replace('slider', ''))
            except ValueError:
                print ("Unknown slider:", sliderName)
                return
            if (sliderNumber == GrandMaster.SLIDER_NUMBER):
                self.grandMaster.setPerc(value)
                
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
        if faderNumber == GrandMaster.SLIDER_NUMBER:
            self.grandMaster.setFlash(buttonPressed)
        elif faderNumber in bindings:
            toChange = bindings[faderNumber]        
            value = 100 if buttonPressed else 0        
                
            if isinstance(toChange, int):  # slider bound to channel            
                self.channelValues[toChange].setDirectFlashValue(value)                
            else:  # slider bound to group
                groupNumber = int(toChange.replace('group', ''))
                self.groupValues[groupNumber].setDirectFlashValue(value)
    
    def handleRawButtonInput(self, rawButtonName, buttonPressed):
        if not self.modals.isEmpty():
            self.modals.handleRawButtonInput(rawButtonName, buttonPressed)
        
    def handleButtonInput(self, buttonName, buttonPressed):        
        # first, we remap virtual S1-S4 keys to current binding.                
        if buttonName in OptionButtons.RAW_BUTTONS:
            buttonName = OptionButtons.getInstance().getCommand(buttonName)
            if buttonName is None:  # catch if we bound to nothing
                return
        
        if buttonName == 'DBO' and buttonPressed:
            self.grandMaster.toggleDBO()            
            return
        
        if not self.modals.isEmpty():
            self.modals.handleInput(buttonName, buttonPressed)
        else:
            if 'b_slider' in buttonName:  # todo check programmer state first.
                #first, we want to remap sliders.
                buttonName = SliderRemapper.instance().getSliderName(buttonName)
                try:
                    faderNumber = int(buttonName.replace('b_slider', ''))
                except ValueError:
                    print ("Unknown button:", buttonName)
                    return
                self.handleFlash(faderNumber, buttonPressed)
            elif buttonPressed:  # we only care about keyDown
                # now, if it's a playback command handle it
                if buttonName in META_COMMANDS:
                    self.handleMetaCommand(buttonName)
                elif buttonName in PLAYBACK_COMMANDS:
                    self.handlePlaybackCommand(buttonName)
                elif buttonName in FADER_COMMANDS:
                    self.handleFaderCommand(buttonName)                
                else:  # otherwise we add the command to console
                    self.handleConsoleInput(buttonName)
    
    def handleMetaCommand(self, buttonName):
        if buttonName == MORE_OPTIONS:
            OptionButtons.getInstance().cycleMainState()
        else:
            print ("unknown Meta command", buttonName)
            
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
        self.faderValues.resetValues()
        self.currentfaderBinding += 1
        if self.currentfaderBinding >= len(self.faderBindings):
            self.currentfaderBinding = 0
        self.refreshFaderBindings()
    
    def prevFaderBindings(self):
        self.faderValues.resetValues()
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
    # refresh bindings from file
    ##################################
    def refreshGroupBindings(self):
        self.groupBindings = self.config.readGroupBindings(self.getNumFaders() * 2) 
        self.groupValues.refreshGroupBindings(self.groupBindings, self.channelValues)
    
    def refreshFaderBindings(self):
        self.faderBindings = self.config.readFaderBindings(self.getNumFaders(), self.getDefaultChannels())
        self.faderValues = FaderValues.FaderValues(self.getFaderBindings())
    
    def getFaderValues(self):
        return self.faderValues
    
    #################################    
    # Get desk properties from file
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

    def saveSettings(self):
        self.config.writeGeneralSettings(self.settings)
        
    # delete binding files
    def resetBindings(self):
        self.config.resetPatch()
        self.Reset()
        if self.notifyControllerReset:
            self.notifyControllerReset()
        
    # delete config files    
    def totalReset(self):        
        self.config.resetAll()
        self.Reset()
        if self.notifyControllerReset:
            self.notifyControllerReset()
    # backup show
    def backupShow(self):
        self.config.writeBackup()
    
    # restore show
    def restoreShow(self):
        self.config.restoreBackup()
        self.Reset()
        if self.notifyControllerReset:
            self.notifyControllerReset()
    
    # records current state into a group. Saves to file.
    def recordGroup(self, groupName):
        try:
            groupNumber = int(groupName.replace('Group',''))            
        except:
            return "Nonexistent group!"
        if groupNumber not in self.groupBindings:
            return "Nonexistent group!"
        
        bindings = []
        channelValues = self.channelValues.values        
        for channelNum, channel in channelValues.items():
            percValue = channel.getDisplayValueAndReason()[0]
            if percValue > 0:
                bindings.append([channelNum, percValue])
        
        self.groupBindings[groupNumber]["channels"] = bindings
        self.groupValues.refreshGroupBindings(self.groupBindings, self.channelValues)
        self.config.writeGroupBindings(self.groupBindings)
        
        return "Recorded current state into group"
    
    def changeGroupLabel(self, groupName, label):
        number = int(groupName.replace('Group',''))
        self.groupBindings[number]['name'] = label
        self.groupValues.changeLabel(groupName, label)
        self.config.writeGroupBindings(self.groupBindings)
    
    ##############################################
    # Get Final Universe Output
    ##############################################
    def getDMXOutput(self):
        return self.finalDMXOutput.getOutput()
    
