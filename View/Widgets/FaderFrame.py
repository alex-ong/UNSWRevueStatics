import tkinter as tk
import View.Widgets.FaderWidget as FaderWidget

import View.ViewStyle as VS
HEADING_FONT = (VS.FONT, VS.font_size(16), 'bold')

class FaderFrame(tk.Frame):
    def __init__(self, getFaderFunc, numFaders, faderLayout, *args):
        super().__init__(*args)     
        self.configure(bg='black')
        self.widgets = {}
        self.getFaderFunc = getFaderFunc
        self.numFaders = numFaders
        
        layout = []
        
        for row in faderLayout:
            rowLayout = ' '.join('x' for i in range(row))            
            layout.append(' ' + rowLayout + ' ')
                                    
        faderIndex = 0
        col = 0
        row = 0
        
        #get widest layout:
        lengths =[len(layout[x]) for x in range(len(layout))]
        
        width = max(lengths)            
        for i in range(width):
            self.grid_columnconfigure(i, weight=1, minsize=VS.pixel_size(16))

        
        # title bar
        title = tk.Label(self, text='Faders', bg='grey', font=HEADING_FONT)
        title.grid(row=row, columnspan=width, sticky=tk.NSEW)        
        
        faderValues = list(getFaderFunc().values.values())    

        while faderIndex < self.numFaders:        
            if col >= len(layout[row]):
                col = 0
                row += 1
                        
            layoutItem = layout[row][col]
            
            if layoutItem == 'x':
                channel = None
                if faderIndex < len(faderValues):
                    channel = faderValues[faderIndex] 
                faderIndex += 1
                cw = FaderWidget.FaderWidget(channel, faderIndex, self)
                cw.grid(row=row + 1, column=col)
                self.widgets[faderIndex] = cw
            col += 1
        self.lastFaderValues = self.getFaderFunc()
    
    # done everytime use presses next/prev fader
    def rebuild(self, faderValues):
        faderIndex = 0
        for faderIndex in range(self.numFaders):
            channel = None
            if faderIndex < len(faderValues):
                channel = faderValues[faderIndex]
            self.widgets[faderIndex + 1].changeFader(channel)
    
    def refreshDisplay(self):    
        # check for if user changed page    
        if self.lastFaderValues != self.getFaderFunc():            
            self.lastFaderValues = self.getFaderFunc()
            faderValues = list(self.getFaderFunc().values.values())    
            self.rebuild(faderValues)
            
        for widget in self.widgets.values():
            widget.refreshDisplay()
    
        
