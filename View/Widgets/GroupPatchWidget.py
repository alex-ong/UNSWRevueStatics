'''
@author: alex-ong
@date 2017-05-07
k'''
import tkinter as tk
from libs.sorted_containers.sorteddict import SortedDict

def autoString(value):        
    if value is None:
        return ''
    elif value == 100:
        return ('FL')
    else:
        return str(value).zfill(2)

from Model import Channel
from View.ViewStyle import COLOR_DIRECT, COLOR_GROUP, COLOR_PLAYBACK, COLOR_RECORD, COLOR_NONE
from View.Widgets.ChannelWidget import typeColourMapping


class GroupPatchWidget(tk.Frame):
    def __init__(self, group, *args):
        super().__init__(*args)
        self.group = group
        self.config(bg='black')
        
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)                    
                    
        self.groupNumberLabel = tk.Label(self, text=str(self.group.number))
        
        self.label = tk.Label(self, text=str(self.group.number).zfill(2), font=('Consolas', 20), fg='white', bg='black')
        self.groupNumberLabel.grid()
        self.label.grid()
        self.lastValue = SortedDict()
        
    def patchString(self, items):
        result = []
        for item in items:
            chan, val = item
            result.append("Chan" + str(chan).zfill(2) + " @ " + autoString(val))
        if len(result) > 10:
            result = result[:10]
            result.append('...')
        return result
    
    def finalPatchString(self, substrings):
        result = []
        split = len(substrings)/2
        for i in range(len(substrings)/2):
            lhs = substring[i]
            rhs = ""
            if i+split < len(substrings):
                rhs = substring[i+split]
            result.append(lhs + "   " + rhs)
        result = '\n'.join(result)
        return result

    def refreshDisplay(self):    
        items = self.group.channelMappings.copy()
        if self.lastValue != items:
            finalString = self.finalPatchString(self.patchString(items))
            self.label.config(text=finalString)
        
    
    def clearValues(self):
        self.label.config(text='')
