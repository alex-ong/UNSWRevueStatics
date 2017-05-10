'''
@author: alex-ong
@date 2017-05-07
'''
import tkinter as tk

def autoString(value):        
    if value is None:
        return ''
    elif value == 100:
        return ('FL')
    else:
        return str(value).zfill(2)

from Model import Channel

COLOR_DIRECT = 'yellow'
COLOR_PLAYBACK = 'green'
COLOR_GROUP = 'cyan'
COLOR_RECORD = 'red'
COLOR_NONE = 'black'

typeColourMapping = { Channel.ValueType.DIRECT : COLOR_DIRECT,
                     Channel.ValueType.PLAYBACK : COLOR_PLAYBACK,
                     Channel.ValueType.GROUP : COLOR_GROUP,
                     Channel.ValueType.RECORD : COLOR_RECORD,
                     Channel.ValueType.NONE: COLOR_NONE}

class FaderWidget(tk.Frame):
    def __init__(self, fader, *args):
        super().__init__(*args)
        self.fader = fader
        self.config(bg='black')
        
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)    
                
        
        label = tk.Label(self, text=str(self.fader.number).zfill(2), font=('Consolas', 20), fg='grey', bg='black')
        
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
        
    def createButton(self, stringVar, colour, size=12):
        return tk.Label(self, textvariable=stringVar, fg=colour, bg='black', font=('Consolas', 6, 'bold'))
    
    def refreshDisplay(self):
        return
        direct = self.channel.directValue
        playback = self.channel.playbackValue
        group = self.channel.groupValue
        record = self.channel.recordValue            
        
        if [direct,playback,group,record] != self.lastValues:            
            # figure out how many actual values we got.
            maxComps = []
            if direct is not None and direct != 0:
                maxComps.append(direct)
            if playback is not None and playback != 0:
                maxComps.append(playback)
            if group is not None and group != 0:
                maxComps.append(group)
            if record is not None:
                maxComps.append(record)
            
            if len(maxComps) == 0:
                maxComps.append(0)
            
            # only show mini labels if 2 or more values set.
            if len(maxComps) >= 2:
                self.directValue.set(autoString(direct))
                self.playBackValue.set(autoString(playback))
                self.groupValue.set(autoString(group))
                self.finalValue.set(autoString(record))
            
            (finalValue, reason) = self.channel.getCueValueAndReason() 
            
            self.finalValue.set(autoString(finalValue))
            
            self.finalValueLabel.config(fg=typeColourMapping[reason])
                    
        self.lastValues = [direct, playback, group, record]        
    
    def clearValues(self):
        self.directValue.set(autoString(None))
        self.playBackValue.set(autoString(None))
        self.groupValue.set(autoString(None))
        self.finalValue.set(autoString(None))
        
