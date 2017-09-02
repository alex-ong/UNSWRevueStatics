import tkinter as tk

def ChannelLayout():
    layout = [('x x x x x x') for i in range(4)]
    layout = "  ".join(layout)
    layout = ' ' + layout + ' '
    return layout

def GroupLayout():
    layout = ' '.join(('x') for i in range(20))
    layout = ' ' + layout + ' ' 
    return layout

from View.Widgets.ChannelGroupWidget import ChannelGroupWidget
from View.ViewStyle import CHANNEL, GROUP
import View.ViewStyle as VS

class ChannelGroupFrame(tk.Frame):
    def __init__(self, values, layoutType, *args):
        super().__init__(*args)     
        self.configure(bg='black')
        self.widgets = {}
        
        # setup layout. Groups of 6 with gaps between elements,
        # double gaps between groups.
        
        if layoutType == GROUP:
            layout = GroupLayout()
        elif layoutType == CHANNEL:
            layout = ChannelLayout() 
        
        itemIndex = 0
        layoutIndex = 0
        
        for i in range (len(layout)):
            self.grid_columnconfigure(i, weight=1, minsize=VS.pixel_size(16))        
                                               
        values = list(values.values.values())
        
        # title bar
        title = tk.Label(self, text='Channels', bg='grey', 
                         font=(VS.FONT, VS.font_size(16), 'bold'))
        title.grid(row=0, columnspan=len(layout), sticky=tk.NSEW)
        maxRow = 0
        while itemIndex < len(values):        
            col = layoutIndex % len(layout)
            row = layoutIndex // len(layout)
            maxRow = row
            layoutItem = layout[col]
            
            if layoutItem == 'x':
                value = values[itemIndex]
                itemIndex += 1
                cw = ChannelGroupWidget(value, itemIndex, False, self)
                cw.grid(row=row + 1, column=col, sticky=tk.NSEW)
                self.widgets[itemIndex] = cw
            layoutIndex += 1
        for i in range(maxRow):
            self.rowconfigure(i, weight=1)
    def refreshDisplay(self):
        for widget in self.widgets.values():
            widget.refreshDisplay()
    
        