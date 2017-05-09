import tkinter as tk
import SliderPlusButton
import collections


class TopPanel(tk.Frame):
    def __init__(self, *args):
        super().__init__(*args)
        self.sliders = []                    
        self.initTopPanel()
        
        
    def initTopPanel(self):        
        for i in range(1, 19):            
            sliderPair = SliderPlusButton.SliderPlusButton(i, i, self)
            sliderPair.grid(row=0, column=i)
            self.sliders.append(sliderPair)
    
    def getState(self):
        result = collections.OrderedDict()

        for slider in self.sliders:
            result.update(slider.getState())
        
        return result