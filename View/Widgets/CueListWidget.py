'''
A bunch of cueWidgets...
'''
import tkinter as tk
NUM_CUES = 6
FROM_END = 2

from View.Widgets.CueWidget import CueWidget 

class CueListWidget(tk.Frame):
    def __init__(self, cueList, *args):
        self.cueList = cueList
        super().__init__(*args)
        self.widgets = []
                
        for i in range(NUM_CUES):
            self.rowconfigure(i, weight=1)
            widget = CueWidget(self)
            self.widgets.append(widget)
            widget.grid(sticky=tk.NSEW)
            
    def refreshDisplay(self):
        # get list of NUM_CUES current cues        
        cues, current = self.cueList.getCues(NUM_CUES, FROM_END)
        
        i = 0        
        while i < len(cues): #can't use forLoop since end value for i is too low
            cueName, cue = cues[i]
            self.widgets[i].refreshDisplay(cueName, cue, i == current)
            i += 1
        
        #if we didn't get enough cues we have to hide a few widgets            
        while i < NUM_CUES:            
            self.widgets[i].hide()
            i += 1
            