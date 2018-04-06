import View.ViewStyle as VS
from View.ViewStyle import COLOR_DIRECT, COLOR_PLAYBACK, COLOR_GROUP, COLOR_RECORD, COLOR_NONE      

import tkinter as tk

GROUP = 'Group'
CHANNEL = 'Channel'

NUMBER_LABEL_FONT = (VS.FONT, VS.font_size(8))


def autoString(value, reason=None):        
    if value is None:
        return '  '    
    elif value == 100:
        return 'FL'
    elif value == 0:
        return '  '
    else:
        return str(value).zfill(2)


# play, direct, group, record
class indexStorer(object):
    SEG_LEN = 2

    # string comes in format [direct group play]
    def __init__(self, channelIndex, stringIndex):
        self.channelIndex = channelIndex
        self.stringIndex = stringIndex        
        
    def endStringIndex(self):
        return self.stringIndex + 6  # 6, because 3 * SEG_LEN
    
    def modifyString(self, string, newValue):
        return string[:self.stringIndex] + newValue + string[self.endStringIndex():]
    
    def getCurrentValue(self, string):
        return string[self.stringIndex:self.endStringIndex()]
    
    def setReason(self, reason):
        self.prevReason = reason
    
    def indexString(self, index):
        return "1." + str(index)
    
    def addTag(self, tkLabel, color, start, end):
        tkLabel.tag_add(color, self.indexString(start), self.indexString(end))
        
    def enforceReason(self, tkLabel):        
        directIndices = self.stringIndex
        groupIndices = directIndices + indexStorer.SEG_LEN 
        playbackIndices = groupIndices + indexStorer.SEG_LEN
        endIndex = playbackIndices + indexStorer.SEG_LEN
        
        self.addTag(tkLabel, COLOR_DIRECT, directIndices, groupIndices)
        self.addTag(tkLabel, COLOR_GROUP, groupIndices, playbackIndices)
        self.addTag(tkLabel, COLOR_PLAYBACK, playbackIndices, endIndex)
    
    def valueChanged(self, newValue, fullString):
        oldValue = self.getCurrentValue(fullString)
        return oldValue != newValue
    
    def reasonChanged(self, newReason):
        return self.prevReason != newReason  

        
class IntermediaryChannelValueRow(tk.Text):

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
        self.config(fg='white', bg='black')
        self.config(width=len(self.prevString))
        self.config(height=1)
        self.config(borderwidth=-1)
        self.config(highlightthickness=0)  # required for *nix
    
    def getValues(self, channel):
        return (channel.getDirectValue(),
                channel.getGroupValue(),
                channel.playbackValue,
                channel.recordValue)
        
    def getTextString(self, channel):
        direct, group, playback, record = self.getValues(channel)
            
        nonZero = 0
        if direct != 0:
            nonZero += 1
        if group != 0:
            nonZero += 1
        if playback != 0:
            nonZero += 1
        if record != None:
            nonZero += 1
        
        if nonZero > 1:
            result = [autoString(direct),
                      autoString(group),
                      autoString(playback)]
            result = "".join(result)
        else:
            result = " " * 6
            
        return result  
    
    def setText(self, value):
        self.configure(state='normal')
        self.delete(1.0, tk.END)
        self.insert('end', value)
        self.configure(state='disabled')
    
    def getLayoutSpacing(self):
        return {' ': ' ' * 2,
                '|' : ' ' * 9,
                'm' : ' '}    
        
    def initialize(self, layout):
        totalString = ''    
        i = 0
        stringIndex = 0
        
        for item in layout:
            if item == 'x':
                stringValue = self.getTextString(self.channels[i])                
                self.indices.append(indexStorer(i, stringIndex))                
                stringIndex += len(stringValue)
                totalString += stringValue              
                i += 1            
            elif item in self.getLayoutSpacing():
                result = self.getLayoutSpacing()[item]
                totalString += result
                stringIndex += len(result)

        self.prevString = totalString
    
    '''
    Sets the colours. Necessary everytime we reset our string as well
    '''

    def enforceReasons(self):
        for index in self.indices:
            index.enforceReason(self)
            
    def refreshDisplay(self):
        stringChanges = False
        for (i, channel) in enumerate(self.channels):
            value = self.getTextString(channel)            
            indexStorer = self.indices[i]            
            if(indexStorer.valueChanged(value, self.prevString)):
                stringChanges = True
                self.prevString = indexStorer.modifyString(self.prevString, value)
                            
        if stringChanges:
            self.setText(self.prevString)
            self.enforceReasons()
        
        return stringChanges
