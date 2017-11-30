import View.ViewStyle as VS

import tkinter as tk


COLOR_DIRECT = 'yellow'
COLOR_PLAYBACK = 'cyan'
COLOR_GROUP = '#00ff00'
COLOR_RECORD = 'red'
COLOR_NONE = 'black'

GROUP = 'Group'
CHANNEL = 'Channel'

FADER_LABEL_FONT = (VS.FONT, VS.font_size(10))
NUMBER_LABEL_FONT = (VS.FONT, VS.font_size(20))

def autoString(value, reason=None):        
    if value is None:
        return '00'    
    elif value == 100:
        return ('FL')
    elif value == 0:
        return '00'
    else:
        return str(value).zfill(2)
    
class indexStorer(object):
    def __init__(self, channelIndex, stringIndex, reason):
        self.channelIndex = channelIndex
        self.stringIndex = stringIndex
        self.prevReason = reason
        
    def endStringIndex(self):
        return self.stringIndex + 2
    
    def modifyString(self, string, newValue):
        return string[:self.stringIndex] + newValue + string[self.endStringIndex():]
    
    def getCurrentValue(self, string):
        return string[self.stringIndex:self.endStringIndex()]
    
    def setReason(self, reason):
        self.prevReason = reason
    
    def enforceReason(self, tkLabel):
        color = VS.typeColourMapping[self.prevReason]        
        tkLabel.tag_add(color, "1." + str(self.stringIndex), "1." + str(self.endStringIndex()))
    
    def valueChanged(self, newValue, fullString):
        oldValue = self.getCurrentValue(fullString)
        return oldValue != newValue
    
    def reasonChanged(self, newReason):
        return self.prevReason != newReason  
        
class ChannelFinalValueRow(tk.Text):
    def __init__(self, channels, layout, *args):
        super().__init__(*args)
        self.indices = []
        self.channels = channels
        self.prevString = ''
        self.initialize(layout)
                
        self.tag_configure(COLOR_PLAYBACK, foreground=COLOR_PLAYBACK)
        self.tag_configure(COLOR_DIRECT, foreground=COLOR_DIRECT)
        self.tag_configure(COLOR_GROUP, foreground=COLOR_GROUP)
        self.tag_configure(COLOR_RECORD, foreground=COLOR_RECORD)
        self.tag_configure(COLOR_NONE, foreground=COLOR_NONE)
                
        self.setText(self.prevString)
        self.config(font=NUMBER_LABEL_FONT)
        self.config(fg='black', bg='black')
        self.config(width=len(self.prevString))
        self.config(height=1)
        self.config(borderwidth=0)    
        
        
    def setText(self, value):
        self.configure(state='normal')
        self.delete(1.0, tk.END)
        self.insert('end', value)
        self.configure(state='disabled')
        
    def initialize(self, layout):
        totalString = ''    
        i = 0
        stringIndex = 0
        
        for item in layout:
            if item == 'x':
                (displayValue, reason) = self.channels[i].getDisplayValueAndReason() 
                self.indices.append(indexStorer(i, stringIndex, reason))
                displayValue = autoString(displayValue, reason)
                stringIndex += len(displayValue)
                totalString += displayValue                 
                i += 1            
            else:
                totalString += '  '
                stringIndex += 2

        self.prevString = totalString
    
    '''
    Sets the colours. Necessary everytime we reset our string as well
    '''
    def enforceReasons(self):
        for index in self.indices:
            index.enforceReason(self)
            
    def refreshDisplay(self):
        stringChanges = False
        reasonChanges = False
        for (i, channel) in enumerate(self.channels):
            value, reason = channel.getDisplayValueAndReason()
            value = autoString(value, reason)
            indexStorer = self.indices[i]            
            if(indexStorer.valueChanged(value, self.prevString)):
                stringChanges = True
                self.prevString = indexStorer.modifyString(self.prevString, value)
            if(indexStorer.reasonChanged(reason)):
                reasonChanges = True
                indexStorer.setReason(reason)
            
        if stringChanges:
            self.setText(self.prevString)
            self.enforceReasons()
        elif reasonChanges:
            self.enforceReasons()

            
    
        
        
