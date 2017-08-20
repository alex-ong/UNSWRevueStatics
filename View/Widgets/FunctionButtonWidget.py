'''
@author: alex-ong
@date 2017-08-20
'''
import tkinter as tk
from math import ceil


from Model import Channel

NUM_COLS = 12
import View.ViewStyle as VS
LABEL_FONT = (VS.FONT, VS.font_size(10))

NUM_BUTTONS = 4 
BG = 'grey'
border = 'red'

class FunctionButtonFrame(tk.Frame):
    def __init__(self, stringGetter, *args):
        super().__init__(*args)        
        self.stringGetter = stringGetter
        self.widgets = []
        
        self.columnconfigure(0, weight=1)
        for i in range (NUM_BUTTONS):
            self.rowconfigure(i, weight=1)
            
        for i in range(NUM_BUTTONS):
            self.widgets.append(FunctionButtonWidget(self))            
            self.widgets[i].grid(sticky=tk.NSEW)
            
        self.prevStrings = []
        self.refreshDisplay()
        
    def refreshStrings(self, newStrings):
        for i in range(NUM_BUTTONS):
            self.widgets[i].refresh(newStrings[i])
        self.prevStrings = newStrings.copy()
                
    def refreshDisplay(self):
        newStrings = self.stringGetter()
        if self.prevStrings != newStrings:            
            self.refreshStrings(newStrings)
                    
class FunctionButtonWidget(tk.Frame):
    def __init__(self, *args):
        super().__init__(*args)
        self.configure(highlightbackground='red',highlightcolor='red', bd=VS.pixel_size(5), bg='black')
        self.stringVar = tk.StringVar()
        self.columnconfigure(0,weight=1,minsize=VS.pixel_size(70))
        self.rowconfigure(0,weight=1,minsize=VS.pixel_size(30))
        
        label = tk.Label(self, textvariable=self.stringVar,
                         font=LABEL_FONT, fg='white', bg=BG, anchor=tk.W)
        #label.pack()                
        label.grid(sticky=tk.NSEW)

    def refresh(self, newString):
        self.stringVar.set(newString)

def _testFunc():
    return ['S1: Delete', 'S2: Cue', 'S3: jahre', 'qsdf']
        
if __name__ == '__main__':
    root = tk.Tk()
    fbw = FunctionButtonFrame(_testFunc, root)
    fbw.pack()
    root.mainloop()
