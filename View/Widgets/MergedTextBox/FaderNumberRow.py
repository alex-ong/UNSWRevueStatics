# Fader frame using merged text boxes. 
import View.ViewStyle as VS
import tkinter as tk
from .ChannelLabelRow import ChannelLabelRow
class FaderNumberRow(ChannelLabelRow):
    
    def getLayoutSpacing(self):
        return {' ' : ' ' * 4,  # space between two elements
                '|' : ' ' * 4,  # group spacing
                'm' : ' ' * 2}  # margin
        
    def getLabel(self, data):
        return str(data.number).zfill(2)          
    
    def determineString(self, faders, layout):
        result = ''
        i = 0
        for item in layout:
            if item == 'x':
                result += self.getLabel(faders[i]) 
                i += 1
            else: 
                result += self.getLayoutSpacing()[item]
                
        return result
