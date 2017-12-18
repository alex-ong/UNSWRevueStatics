# Fader frame using merged text boxes. 
import View.ViewStyle as VS
from View.ViewStyle import COLOR_DIRECT, COLOR_GROUP, COLOR_NONE      

import tkinter as tk

FADER_LABEL_FONT = (VS.FONT, VS.font_size(12))
from Model import Group

class FaderDescriptionRow(tk.Text):
    def __init__(self, faders, layout, *args):
        super().__init__(*args)                   
        self.tag_configure(COLOR_DIRECT, foreground=COLOR_DIRECT)
        self.tag_configure(COLOR_GROUP, foreground=COLOR_GROUP)        
        self.tag_configure(COLOR_NONE, foreground=COLOR_NONE)
        self.layout = layout
        
        self.stringLength = 0
        self.rebuild(faders)        
        self.config(fg='white', bg='black')        
        self.config(height=1)
        self.config(borderwidth=0)        
        self.config(font=FADER_LABEL_FONT)        
        
        
    def addText(self, toAdd, tag=None):
        if tag is not None:
            startIndex = self.stringLength
            
        self.stringLength += len(toAdd)
        self.insert('end', toAdd)
        
        if tag is not None:
            endIndex = self.stringLength
            self.tag_add(tag, "1."+str(startIndex),"1."+str(endIndex))
            
        
    def rebuild(self, faders):
        self.configure(state='normal')
        self.delete(1.0, tk.END)
        faderIndex = 0
        self.stringLength = 0
        for item in self.layout:
            if item == 'x':
                try:
                    faderRef = faders[faderIndex].getBinding()
                    if isinstance(faderRef, Group.Group):                    
                        self.addText('Grp' + str(faderRef.number).zfill(2), COLOR_GROUP)                    
                    else:  # isinstance(faderRef, Channel.Channel):                    
                        self.addText('Chn' + faderRef.label.zfill(2), COLOR_DIRECT)
                except IndexError: #no fader in fader list
                    self.addText(' '* 5, COLOR_NONE)
                    
                faderIndex += 1
            elif item == ' ':
                self.addText(' ' * 5)
            elif item == '|':  # group split
                self.addText(' ' * 4)
            elif item == 'm':  # margin
                self.addText(' ' * 3)
        
        #reconfigure textbox width
        self.configure(width=len(self.get("1.0",tk.END)))        
        self.configure(state='disabled')
    
    def refreshDisplay(self):
        pass
