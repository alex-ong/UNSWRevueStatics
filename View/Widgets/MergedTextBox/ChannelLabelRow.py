import View.ViewStyle as VS
import tkinter as tk

NUMBER_LABEL_FONT = (VS.FONT, VS.font_size(20))

class ChannelLabelRow(tk.Label):
    def __init__(self, channels, layout, *args):
        super().__init__(*args)        
        self.config(text=self.determineString(channels, layout))
        self.config(font=NUMBER_LABEL_FONT)
        self.config(borderwidth=0)       
        self.config(highlightthickness=0) #required for *nix 
        self.config(fg='grey', bg='black')
        
    def getLayoutSpacing(self):
        return {' ' : ' ',  # space between two elements
                '|' : ' ' * 4,  # group spacing
                'm' : ' '}  # margin
        
    def getLabel(self, data):
        return data.label.zfill(2)    
    
    def determineString(self, channelNames, layout):
        result = ''
        i = 0
        for item in layout:
            if item == 'x':                
                result += self.getLabel(channelNames[i])
                i += 1
            else:
                result += self.getLayoutSpacing()[item]
            
                
        return result
