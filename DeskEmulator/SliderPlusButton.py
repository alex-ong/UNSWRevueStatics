import tkinter as tk

class SliderPlusButton(tk.Frame):
    def __init__(self, sliderNum, label, *args):
        self.sliderNum = sliderNum
        super().__init__(*args)
        label = tk.Label(self, text=label)
        label.pack()
        scale = tk.Scale(self, from_=100, to=0, showvalue=0, command=self.refreshValue)
        scale.pack()        
        b = tk.Button(self, text="BAM")
        b.bind("<Button-1>", self.buttonDown)
        b.bind("<ButtonRelease-1>", self.buttonUp) 
        b.pack()
        self.sliderValue = 0
        self.isButtonDown = False
        
    def getValue(self):
        if self.isButtonDown:
            return 100
        else:
            return int(self.sliderValue)
        
    def getState(self):
        return {self.sliderNum: self.getValue()}  
    
    def refreshValue(self, val):
        self.sliderValue = val
        
    def buttonDown(self, *args):
        self.isButtonDown = True
        
    def buttonUp(self, *args):
        self.isButtonDown = False
