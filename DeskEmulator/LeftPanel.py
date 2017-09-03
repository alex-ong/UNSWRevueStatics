import tkinter as tk
import SliderPlusButton
import CherryButton
import collections

class LeftPanel(tk.Frame):
    def __init__(self, *args):
        super().__init__(*args)
        self.sliders = []
        self.buttons = []
        self.grid_columnconfigure(0, minsize=32)
        self.grid_columnconfigure(1, minsize=16)
        self.grid_columnconfigure(3, minsize=16)  
        
        self.grid_rowconfigure(0, minsize=32)
        self.grid_rowconfigure(1, minsize=5)
        self.grid_rowconfigure(2, minsize=32)
        self.grid_rowconfigure(3, minsize=32)
        self.grid_rowconfigure(4, minsize=5)
        self.grid_rowconfigure(5, minsize=32)                  
        self.initPanel()
        
        
        
    def initPanel(self):
        dbo = CherryButton.CherryButton('DBO', 'DBO',self)
        dbo.grid(row=0, column=0, sticky=tk.NSEW)
        back = CherryButton.CherryButton('Back', 'Back',self)
        back.grid(row=2, column=0, sticky=tk.NSEW)
        rel = CherryButton.CherryButton('Rel', 'Release', self)
        rel.grid(row=3, column=0, sticky=tk.NSEW)
        nxt = CherryButton.CherryButton('Next', 'Next', self)
        nxt.grid(row=5, column=0, sticky=tk.NSEW)
                
        self.buttons = [dbo, back, rel, nxt]
        
        self.grandMaster = SliderPlusButton.SliderPlusButton(-1, "GM", self)
        self.grandMaster.grid(row=0, column=2, rowspan=6)
        for i in range(0, 9):            
            sliderPair = SliderPlusButton.SliderPlusButton(19 + i, 1 + i, self)
            sliderPair.grid(row=0, column=4 + i, rowspan=6)
            self.sliders.append(sliderPair)
             
    
    def getState(self):
        result = collections.OrderedDict()
        for button in self.buttons:
            result.update(button.getState())
        for slider in self.sliders:
            result.update(slider.getState())
        result.update(self.grandMaster.getState())
        return result
