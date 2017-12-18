# Fader frame using merged text boxes. 
import View.ViewStyle as VS
from View.ViewStyle import COLOR_DIRECT, COLOR_PLAYBACK, COLOR_GROUP, COLOR_RECORD, COLOR_NONE      

import tkinter as tk

FADER_LABEL_FONT = (VS.FONT, VS.font_size(10))
from Model import Group

class FaderDescriptionRow(tk.Text):
    def __init__(self, faders, layout, *args):
        super().__init__(*args)                
        self.layout = layout
        self.tag_configure(COLOR_PLAYBACK, foreground=COLOR_PLAYBACK)
        self.tag_configure(COLOR_DIRECT, foreground=COLOR_DIRECT)
        self.tag_configure(COLOR_GROUP, foreground=COLOR_GROUP)
        self.tag_configure(COLOR_RECORD, foreground=COLOR_RECORD)
        self.tag_configure(COLOR_NONE, foreground=COLOR_NONE)
        
        string = self.determineString(faders, layout)
        self.setText(string)        
        self.config(fg='white', bg='black')
        self.config(width=len(string))
        self.config(height=1)
        self.config(borderwidth=0)
        
                
        
        self.config(font=FADER_LABEL_FONT)        
        
        
    def setText(self, value):
        self.configure(state='normal')
        self.delete(1.0, tk.END)
        self.insert('end', value)
        self.configure(state='disabled')
        
    def determineString(self, faders, layout):
        result = ''
        index = 0
        for item in layout:
            if item == 'x':
                faderRef = faders[index].getBinding()
                if isinstance(faderRef, Group.Group):  
                    result += ' Group' + faderRef.label.zfill(2) + ' '
                else:  # isinstance(faderRef, Channel.Channel):
                    result += 'Channel' + faderRef.label.zfill(2)
                index += 1
            elif item == ' ':
                result += ' ' * 4
            elif item == '|':  # group split
                result += ' ' * 4
            elif item == 'm':  # margin
                result += ' '
                
        return result

