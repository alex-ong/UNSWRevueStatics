'''
ChannelGroupWidget
@author alex-ong

A widget that implements both channel widget and group widget functionalities
'''

import tkinter as tk
import Model
from View.ViewStyle import COLOR_DIRECT, COLOR_GROUP, COLOR_PLAYBACK, COLOR_RECORD, COLOR_NONE, CHANNEL, GROUP
from View.ViewStyle import typeColourMapping

def autoString(value, reason=None):        
    if value is None:
        return ''    
    elif value == 100:
        return ('FL')
    elif value == 0:
        if reason == Model.Channel.ValueType.RECORD:
            return '00'
        else:
            return ''
    else:
        return str(value).zfill(2)
    
def bindingIsChannel(binding):
    return isinstance(binding, Model.Channel.Channel)

def bindingIsGroup(binding):
    return isinstance(binding, Model.Group.Group)

import View.ViewStyle as VS
FADER_LABEL_FONT = (VS.FONT, VS.font_size(10))
NUMBER_LABEL_FONT = (VS.FONT, VS.font_size(20))
class ChannelGroupWidget(tk.Frame):            
    def __init__(self, channelOrGroup, faderNumber, showFaderLabel, *args):
        super().__init__(*args)
        self.showFaderLabel = showFaderLabel
        self.data = channelOrGroup
        self.dataType = self.calculateDataType()
        self.faderNumber = faderNumber

        self.config(bg='black')
        
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)                    
                            
        # Fader label (e.g. Pool1, Group1, Chan01 etc)        
        row = 0
        if (showFaderLabel):            
            faderLabelString = self.getFaderLabelString()        
            self.faderLabel = tk.Label(self, text=faderLabelString, font=FADER_LABEL_FONT, 
                                       fg=typeColourMapping[self.dataType], bg='black')
            self.faderLabel.grid(row=row,columnspan=2)
            row += 1
        else:
            self.faderLabel = None
            
        # Actual group or channel number ("00" to "99")
        self.numberLabel = tk.Label(self, text=str(self.faderNumber).zfill(2), 
                                    font=NUMBER_LABEL_FONT, fg='grey', bg='black')
        self.numberLabel.grid(row=row,columnspan=2)
        row += 1
        
        # Final value label        
        self.finalValue = tk.StringVar()
        self.finalValueLabel = self.createButton(self.finalValue, 'white')
        self.finalValueLabel.config(font=NUMBER_LABEL_FONT)
        self.finalValueLabel.grid(row=row, columnspan=2)
        row += 1
                
        ######################
        # 2x2 grid of values #
        # DIRECT | PLAYBACK  #
        # -------+---------  #
        #       GROUP        #
        ######################k
        self.directValue = tk.StringVar()
        directLabel = self.createButton(self.directValue, COLOR_DIRECT)
        directLabel.grid(row=row, column=0)        
        self.playBackValue = tk.StringVar()
        playbackLabel = self.createButton(self.playBackValue, COLOR_PLAYBACK)
        playbackLabel.grid(row=row,column=1)
        row += 1
        
        self.groupValue = tk.StringVar()
        groupLabel = self.createButton(self.groupValue, COLOR_GROUP)
        groupLabel.grid(row=row,columnspan=2)                
        self.recordValue = tk.StringVar()  # no record label since it overrides everything        
          
        self.lastValues = []        
        self.refreshDisplay()
        
    def calculateDataType(self):
        if bindingIsChannel(self.data):
            return CHANNEL
        elif bindingIsGroup(self.data):
            return GROUP
        else:            
            return None      
          
    def createButton(self, stringVar, colour, size=8):
        return tk.Label(self, textvariable=stringVar, fg=colour, bg='black', 
                        font=(VS.FONT, VS.font_size(size), 'bold'))    
    
    def getGroupValue(self):
        if self.dataType == CHANNEL:
            return self.data.getGroupValue()
        else:
            return 0
    
    def getNonZeroCount(self, direct, playback, group, record):
        # figure out how many actual values we got.
        maxComps = []
        if direct is not None and direct != 0:
            maxComps.append(direct)
        if playback is not None and playback != 0:
            maxComps.append(playback)
        if group != 0:
            maxComps.append(group)
        
        return len(maxComps)
    
    def refreshDisplay(self):
        if self.data is None:
            return
        direct = self.data.getDirectValue()
        playback = self.data.playbackValue
        group = self.getGroupValue()
        record = self.data.recordValue            
        
        if [direct, playback, group, record] != self.lastValues:
            self.clearValues()
            if record is not None:  # show any non-zeroes if record isn't None                 
                self.directValue.set(autoString(direct))
                self.groupValue.set(autoString(group))
                self.playBackValue.set(autoString(playback))                
            elif self.getNonZeroCount(direct, playback, group, record) >= 2: 
                # show if there are at least two non-zeroes
                self.directValue.set(autoString(direct))
                self.groupValue.set(autoString(group))
                self.playBackValue.set(autoString(playback))                
                        
            (finalValue, reason) = self.data.getDisplayValueAndReason() 
            
            self.finalValue.set(autoString(finalValue, reason))            
            self.finalValueLabel.config(fg=typeColourMapping[reason])
                    
        self.lastValues = [direct, playback, group, record]        
    
    def clearValues(self):
        self.directValue.set(autoString(None))
        self.playBackValue.set(autoString(None))
        self.groupValue.set(autoString(None))
        self.finalValue.set(autoString(None))
    
    def getNumberLabel(self):        
        return str(self.data.number).zfill(2)
    
    def getFaderLabelString(self):
        if self.dataType == CHANNEL:
            faderLabelString = 'Chan' + str(self.data.number).zfill(2) + '\n'
        elif self.dataType == GROUP:
            faderLabelString = 'Group' + str(self.data.number).zfill(2)
            if faderLabelString != self.data.label:
                faderLabelString += '\n' + self.data.label
            else:
                faderLabelString += '\n'     
        else:
            faderLabelString = '\n'
        return faderLabelString  
    
    def changeFader(self, channelOrGroup):
        #change which channel or group we point to.
        self.data = channelOrGroup
        self.dataType = self.calculateDataType()
        
        #refresh faderLabel if it is shown
        if (self.showFaderLabel):            
            faderLabelString = self.getFaderLabelString()
            self.faderLabel.config(text=faderLabelString, fg=typeColourMapping[self.dataType])     
        
        self.clearValues()   
