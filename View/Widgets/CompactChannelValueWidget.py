'''
@author: alex-ong
@date 2017-07-31
'''
import tkinter as tk
from math import ceil

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

NUM_COLS = 12

class CompactChannelValueWidget(tk.Frame):
    def __init__(self, channelValues, *args):
        super().__init__(*args)
        self.channelValues = channelValues
        self.config(bg='red')
        
        #todo add heading
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)            
                
        self.label = tk.Label(self, text='', font=('Consolas', 12), fg='white', bg='black')                
        self.label.grid(sticky=tk.NSEW)
        self.refreshDisplay()

    def finalPatchString(self, substrings):
        result = []
        
        split = ceil(len(substrings) / NUM_COLS)
        i = 0
        while len(substrings) > 0:
            end = min(NUM_COLS, len(substrings))  # find end index safely
            lineArray = substrings[0:end]  # get subArray
            line = '   '.join(lineArray)  # generate...
            result.append(line)  # and store line
            substrings = substrings[end:]  # chop front of array
            
        result = '\n'.join(result)
        return result
    
    def refreshDisplay(self):
        items = []
        for key, value in self.channelValues.items():
            if value != 0:
                items.append([key, value])
        strings = []
        
        for item in items:            
            strings.append("Chan" + str(item[0]).zfill(2) + " @ " + autoString(item[1]))
        
        finalString = self.finalPatchString(strings)
        self.label.config(text=finalString)
        
