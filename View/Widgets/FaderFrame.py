import tkinter as tk
import View.Widgets.FaderWidget as FaderWidget

class FaderFrame(tk.Frame):
    def __init__(self, faderValues, faderLayout, *args):
        super().__init__(*args)     
        self.configure(bg='black')
        self.widgets = {}
        
        # setup layout. Groups of 6 with gaps between elements,
        # double gaps between groups.
        layout = []
        
        for row in faderLayout:
            layout.append(' '.join('x' for i in range(row)))
                                
        faderIndex = 0
        col = 0
        row = 0
        
        for i in range (len(layout[0])):
            self.grid_columnconfigure(i, weight=0,minsize=16)                                     
             
        faderValues = list(faderValues.values.values())    
                
        while faderIndex < len(faderValues):        
            if col >= len(layout[row]):
                col = 0
                row += 1
                        
            layoutItem = layout[row][col]
            
            if layoutItem == 'x':
                channel = faderValues[faderIndex]
                faderIndex += 1
                cw = FaderWidget.FaderWidget(channel, self)
                cw.grid(row=row, column=col)
                self.widgets[faderIndex] = cw
            col += 1
                
    def refreshDisplay(self):
        for widget in self.widgets.values():
            widget.refreshDisplay()
    
        