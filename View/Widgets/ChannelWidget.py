'''
@author: alex-ong
@date 2017-05-07
'''
import tkinter as tk

def autoString(value, reason=None):        
    if value is None:
        return ''    
    elif value == 100:
        return ('FL')
    elif value == 0:
        if reason == Channel.ValueType.RECORD:
            return '00'
        else:
            return ''
    else:
        return str(value).zfill(2)

from Model import Channel

COLOR_DIRECT = 'yellow'
COLOR_PLAYBACK = 'cyan'
COLOR_GROUP = '#00ff00'
COLOR_RECORD = 'red'
COLOR_NONE = 'black'

typeColourMapping = { Channel.ValueType.DIRECT : COLOR_DIRECT,
                     Channel.ValueType.PLAYBACK : COLOR_PLAYBACK,
                     Channel.ValueType.GROUP : COLOR_GROUP,
                     Channel.ValueType.RECORD : COLOR_RECORD,
                     Channel.ValueType.NONE: COLOR_NONE}

class ChannelWidget(tk.Frame):
    def __init__(self, channel, showLabel, *args):
        super().__init__(*args)
        self.channel = channel
        self.config(bg='black')
        
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)    
                
        label = tk.Label(self, text=str(self.channel.number).zfill(2), font=('Consolas', 20), fg='grey', bg='black')        
        
        self.finalValue = tk.StringVar()
        self.finalValueLabel = self.createButton(self.finalValue, 'white')
        self.finalValueLabel.config(font=('Consolas', 20))
        
        self.directValue = tk.StringVar()
        directLabel = self.createButton(self.directValue, COLOR_DIRECT)
        
        self.playBackValue = tk.StringVar()
        playbackLabel = self.createButton(self.playBackValue, COLOR_PLAYBACK)
        
        self.groupValue = tk.StringVar()
        groupLabel = self.createButton(self.groupValue, COLOR_GROUP)
        
        self.recordValue = tk.StringVar()  # no record label since it overrides everything        
        
        row = 0
        if showLabel:
            labelString = 'Ch' + self.channel.label.zfill(2)
            subLabel = tk.Label(self, text=labelString, font=('Consolas', 10), fg=COLOR_DIRECT, bg='black')
            subLabel.grid(row=row, columnspan=2)        
            row += 1
        label.grid(row=row, columnspan=2)        
        row += 1
        
        self.finalValueLabel.grid(row=row, columnspan=2)
        row += 1        
        directLabel.grid(row=row, column=0)
        playbackLabel.grid(row=row, column=1)
        row += 1        
        groupLabel.grid(row=row, columnspan=2)
        self.lastValues = []        
        self.refreshDisplay()
        
    def createButton(self, stringVar, colour):
        return tk.Label(self, textvariable=stringVar, fg=colour, bg='black', font=('Consolas', 8, 'bold'))
    
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
        direct = self.channel.getDirectValue()
        playback = self.channel.playbackValue
        group = self.channel.getGroupValue()
        record = self.channel.recordValue            
        
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
                        
            (finalValue, reason) = self.channel.getCueValueAndReason() 
            
            self.finalValue.set(autoString(finalValue, reason))
            
            self.finalValueLabel.config(fg=typeColourMapping[reason])
                    
        self.lastValues = [direct, playback, group, record]        
    
    def clearValues(self):
        self.directValue.set(autoString(None))
        self.playBackValue.set(autoString(None))
        self.groupValue.set(autoString(None))
        self.finalValue.set(autoString(None))
        
