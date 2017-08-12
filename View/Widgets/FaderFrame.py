import tkinter as tk
import View.Widgets.FaderWidget as FaderWidget


class FaderFrame(tk.Frame):
    def __init__(self, getFaderFunc, numFaders, faderLayout, *args):
        super().__init__(*args)     
        self.configure(bg='black')
        self.widgets = {}
        self.getFaderFunc = getFaderFunc
        self.numFaders = numFaders
        # setup layout. Groups of 6 with gaps between elements,
        # double gaps between groups.
        layout = []
        
        for row in faderLayout:
            rowLayout = ' '.join('x' for i in range(row))            
            layout.append(' ' + rowLayout + ' ')
                                    
        faderIndex = 0
        col = 0
        row = 0
        
        for i in range (len(layout[0])):
            self.grid_columnconfigure(i, weight=1, minsize=16)                                     
        
        # title bar
        title = tk.Label(self, text='Faders', bg='grey', font=('consolas', 16, 'bold'))
        title.grid(row=row, columnspan=len(layout[0]), sticky=tk.NSEW)        
        
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
                cw = FaderWidget.FaderWidget(channel, self)
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
    
        
