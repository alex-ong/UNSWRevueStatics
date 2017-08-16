'''
@author: alex-ong
@date 2017-05-07
'''
import tkinter as tk
from libs.sorted_containers.sorteddict import SortedDict
from math import ceil

def autoString(value):        
    if value is None:
        return ''
    elif value == 100:
        return ('FL')
    else:
        return str(value).zfill(2)

from Model import Channel
from View.ViewStyle import COLOR_DIRECT, COLOR_GROUP, COLOR_PLAYBACK, COLOR_RECORD, COLOR_NONE
from View.ViewStyle import typeColourMapping

import View.ViewStyle as VS
HEADING_FONT = (VS.FONT, VS.font_size(10))
FONT = (VS.FONT, VS.font_size(8))

class GroupPatchWidget(tk.Frame):
    def __init__(self, groupNumber, *args):
        super().__init__(*args)
        
        self.config(bg='black')
        
        self.columnconfigure(0, weight=0, minsize=VS.pixel_size(100))
        self.columnconfigure(1, weight=0, minsize=VS.pixel_size(100))                    
        self.rowconfigure(1, weight=0, minsize=VS.pixel_size(100))
        
        self.groupNumberLabel = tk.Label(self, text=str(groupNumber).zfill(2),
                                         fg='black', bg='white', font=HEADING_FONT)
        self.groupLabel = tk.Label(self, text=str("Group1"),
                                   fg='black', bg='white', font=HEADING_FONT)
        # patching string
        self.label = tk.Label(self, text="",
                              fg='white', bg='black', font=FONT)
        self.groupNumberLabel.grid(row=0, column=0, sticky='nsew')        
        self.groupLabel.grid(row=0, column=1, sticky='nsew')
        self.label.grid(row=1, columnspan=2, sticky=tk.NSEW)
        self.lastValue = []
        self.lastLabel = ""
        
    def patchString(self, items):
        if len(items) == 0:
            return []
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
        
        split = ceil(len(substrings) / 2)
        i = 0
        while len(substrings) > 0:
            end = min(2, len(substrings))  # find end index safely
            lineArray = substrings[0:end]  # get subArray
            line = '   '.join(lineArray)  # generate...
            result.append(line)  # and store line
            substrings = substrings[end:]  # chop front of array
            
        result = '\n'.join(result)
        return result

    def refreshDisplay(self, newPatch, newLabel):    
        items = newPatch.copy()
        if self.lastValue != items:            
            self.lastValue = items
            finalString = self.finalPatchString(self.patchString(items))
            self.label.config(text=finalString)
        
        if self.lastLabel != newLabel:
            self.groupLabel.config(text=newLabel)
            self.lastLabel = newLabel
            
    def clearValues(self):
        self.label.config(text='')
