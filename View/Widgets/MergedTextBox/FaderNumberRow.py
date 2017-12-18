# Fader frame using merged text boxes. 
import View.ViewStyle as VS
import tkinter as tk

FADER_LABEL_FONT = (VS.FONT, VS.font_size(10))
NUMBER_LABEL_FONT = (VS.FONT, VS.font_size(20))

class FaderNumberRow(tk.Label):
    def __init__(self, channels, layout, *args):
        super().__init__(*args)
        self.config(text=self.determineString(channels, layout))
        self.config(font=NUMBER_LABEL_FONT)
        self.config(fg='grey', bg='black')
        
    def determineString(self, faders, layout):
        result = ''
        i = 0
        for item in layout:
            if item == 'x':
                result += str(faders[i].number).zfill(2)
                i += 1
            elif item == ' ':
                result += ' ' * 4
            elif item == '|':  # group split
                result += ' ' * 4
            elif item == 'm':  # margin
                result += ' ' * 2
                
        return result
