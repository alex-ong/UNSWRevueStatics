'''
@author: alex-ong
@date 2017-05-07
k'''
import tkinter as tk

def autoString(value):        
    if value is None:
        return ''
    elif value == 100:
        return ('FL')
    else:
        return str(value).zfill(2)

from Model import Channel

from View.Widgets.ChannelWidget import COLOR_DIRECT
from View.Widgets.ChannelWidget import COLOR_GROUP
from View.Widgets.ChannelWidget import COLOR_PLAYBACK
from View.Widgets.ChannelWidget import COLOR_RECORD
from View.Widgets.ChannelWidget import COLOR_NONE 



from View.Widgets.ChannelWidget import typeColourMapping


class GroupWidget(tk.Frame):
    def __init__(self, group, showLabel, *args):
        super().__init__(*args)
        self.group = group
        self.config(bg='black')
        
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)                    
                    
        labelString = group.label        
                    
        label = tk.Label(self, text=str(self.group.number).zfill(2), font=('Consolas', 20), fg='grey', bg='black')
        
        self.finalValue = tk.StringVar()
        self.finalValueLabel = self.createButton(self.finalValue, 'white')
        self.finalValueLabel.config(font=('Consolas', 20))
        
        self.directValue = tk.StringVar()
        directLabel = self.createButton(self.directValue, COLOR_DIRECT)
        
        self.playBackValue = tk.StringVar()
        playbackLabel = self.createButton(self.playBackValue, COLOR_PLAYBACK)
                    
        self.recordValue = tk.StringVar()  # no record label since it overrides everything        
        
        row = 0    
        labelString = labelString[:6]
        subLabel = tk.Label(self, text=self.group.label, font=('Consolas', 10), fg=COLOR_GROUP, bg='black')
        subLabel.grid(row=row, columnspan=2)                      
        row += 1                
        label.grid(row=row, columnspan=2)  
        row += 1
        self.finalValueLabel.grid(row=row, columnspan=2)
        row += 1        
        directLabel.grid(row=row, column=0)
        playbackLabel.grid(row=row, column=1)
        row += 1 #put in black group-label to make this widget line up to channel widget
        groupLabel = self.createButton(None, COLOR_NONE)
        groupLabel.grid(row=row,columnspan=2)
        self.lastValues = []        
        self.refreshDisplay()
        
    def createButton(self, stringVar, colour, size=12):
        return tk.Label(self, textvariable=stringVar, fg=colour, bg='black', font=('Consolas', 6, 'bold'))    
    
    def refreshDisplay(self):    
        direct = self.group.directValue
        playback = self.group.playbackValue        
        record = self.group.recordValue            
        
            # figure out how many actual values we got.
        if [direct, playback, record] != self.lastValues:            
            maxComps = []
            if direct is not None and direct != 0:
                maxComps.append(direct)
            if playback is not None and playback != 0:
                maxComps.append(playback)            
            if record is not None:
                maxComps.append(record)
            
            if len(maxComps) == 0:
                maxComps.append(0)
            
            # only show mini labels if 2 or more values set.
            if len(maxComps) >= 2:
                self.directValue.set(autoString(direct))
                self.playBackValue.set(autoString(playback))        
                self.finalValue.set(autoString(record))
            
            (finalValue, reason) = self.group.getCueValueAndReason() 
            
            self.finalValue.set(autoString(finalValue))
            
            self.finalValueLabel.config(fg=typeColourMapping[reason])
                    
        self.lastValues = [direct, playback, record]        
    
    def clearValues(self):
        self.directValue.set(autoString(None))
        self.playBackValue.set(autoString(None))
        self.finalValue.set(autoString(None))
        