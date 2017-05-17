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

        # todo: handle len(cues) < NUM_CUES
        
        for i in range (NUM_CUES):
            cueName, cue = cues[i]
            self.widgets[i].refreshDisplay(cueName, cue, i == current)
