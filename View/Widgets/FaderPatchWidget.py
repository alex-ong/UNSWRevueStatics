'''
FaderPatchFrame

Shows what the fader is patched to.
@author: alex-ong
@date 2017-08-13
'''

from View.ViewStyle import COLOR_DIRECT, COLOR_GROUP, COLOR_PLAYBACK, COLOR_RECORD, COLOR_NONE, CHANNEL, GROUP
from View.ViewStyle import typeColourMapping
from View.Widgets.ChannelGroupWidget import bindingIsChannel, bindingIsGroup
HEADING_FONT = ('Consolas', 20)
FONT = ('Consolas', 8)
import tkinter as tk

class FaderPatchWidget(tk.Frame):
    def __init__(self, num, binding,  *args):
        super().__init__(*args)
        
        self.config(bg='black')
        self.number = num
        self.binding = binding        
        
        bindingType = self.getBindingType()
        
        self.columnconfigure(0, weight=0, minsize=100)                        
        self.rowconfigure(1, weight=0, minsize=100)
                
        self.headingLabel = tk.Label(self, text=str(self.number).zfill(2), 
                                     font=HEADING_FONT, fg='grey', bg='black')
        self.patchLabel = tk.Label(self, text=self.getFaderLabelString(), font=FONT, 
                                   fg=typeColourMapping[bindingType], bg='black')
        self.headingLabel.grid(sticky=tk.NSEW)
        self.patchLabel.grid(sticky=tk.NSEW)
        
    def getBindingType(self):        
        bindingType = None
        if bindingIsChannel(self.binding):
            bindingType = CHANNEL
        elif bindingIsGroup(self.binding):
            bindingType = GROUP
        
        return bindingType
    
    def getFaderLabelString(self):
        binding = self.binding
        dataType = self.getBindingType()
        if dataType == CHANNEL:
            faderLabelString = 'Chan' + str(binding.number).zfill(2)
        elif dataType == GROUP:
            #todo: also get group label and '\n'
            faderLabelString = 'Group' + str(binding.number).zfill(2) + '\n' + binding.label
        else: #dataType == None
            faderLabelString = ''
        return faderLabelString
            
    def rebuildWidget(self):
        bindingType = self.getBindingType()
        self.patchLabel.config(text=self.getFaderLabelString(),fg=typeColourMapping[bindingType])
    
    def refreshDisplay(self, newBinding):    
        if self.binding != newBinding:
            self.binding = newBinding         
            self.rebuildWidget()
        
