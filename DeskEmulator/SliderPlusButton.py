import tkinter as tk
import CherryButton

class SliderPlusButton(tk.Frame):
    def __init__(self, sliderNum, label, *args):
        self.sliderNum = sliderNum
        super().__init__(*args)
        label = tk.Label(self, text=label)
        label.pack()
        scale = tk.Scale(self, from_=100, to=0, showvalue=0, command=self.refreshValue)
        scale.pack()        
        self.b = CherryButton.CherryButton("BAM", None, self)		        
        self.b.pack()
        self.sliderValue = 0
        
        
    def getValue(self):        
        return int(self.sliderValue)
        
    def getState(self):
        return {'slider'+str(self.sliderNum): self.getValue(),
                'b_slider'+str(self.sliderNum): self.b.isButtonDown}  
    
    def refreshValue(self, val):
        self.sliderValue = val
        
