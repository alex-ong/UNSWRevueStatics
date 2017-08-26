import tkinter as tk

from . import SystemTimeWidget
from . import DBOWidget

import View.ViewStyle as VS
BG = '#000000'
FONT = (VS.FONT, VS.font_size(20))
FG = VS.COLOR_DIRECT

class TopBar(tk.Frame):
    def __init__(self, getPerc, *args):
        super().__init__(*args)
        self.config(bg=BG)
        
        for i in range(3):
            self.columnconfigure(i, weight=1,minsize=VS.pixel_size(640))    
        
        self.rowconfigure(0, weight=1)
        
        self.dboWidget = DBOWidget.DBOWidget(getPerc[0], getPerc[1], self)
        self.timeWidget = SystemTimeWidget.SystemTimeWidget(self)
        
        self.dboWidget.grid(row=0, column=0, sticky=tk.W)
        self.timeWidget.grid(row=0, column=1, sticky=tk.NSEW)
        
    def refreshDisplay(self):
        self.dboWidget.refreshDisplay()
        self.timeWidget.refreshDisplay()
