import tkinter as tk
import View.Widgets.FaderWidget as FaderWidget

class FaderFrame(tk.Frame):
    def __init__(self, faderValues, *args):
        super().__init__(*args)     
        self.configure(bg='black')
        self.channelWidgets = {}
        
        # setup layout. Groups of 6 with gaps between elements,
        # double gaps between groups.
        layout = [('x x x x x x') for i in range(4)]
        layout = "  ".join(layout)
        layout = ' ' + layout + ' '                
        
        channelIndex = 0
        layoutIndex = 0
        
        for i in range (len(layout)):
            self.grid_columnconfigure(i, weight=0,minsize=16)                                     
             
        faderValues = list(faderValues.values.values())    
        
        while channelIndex < len(faderValues):        
            col = layoutIndex % len(layout)
            row = layoutIndex // len(layout)
            layoutItem = layout[col]
            
            if layoutItem == 'x':
                channel = faderValues[channelIndex]
                channelIndex += 1
                cw = FaderWidget.FaderWidget(channel, self)
                cw.grid(row=row, column=col)
                self.channelWidgets[channelIndex] = cw
            layoutIndex += 1
                
    def refreshDisplay(self):
        for widget in self.channelWidgets.values():
            widget.refreshDisplay()
    
        