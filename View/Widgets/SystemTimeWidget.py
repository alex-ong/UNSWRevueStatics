import tkinter as tk
import time

import View.ViewStyle as VS
BG = '#000000'
FONT = (VS.FONT, VS.font_size(20))
FG = VS.COLOR_DIRECT

TIME_FORMAT = "%H:%M %p"
class SystemTimeWidget(tk.Frame):
    def __init__(self, *args):
        super().__init__(*args)
        self.config(bg=BG)
        self.columnconfigure(0, weight=1)        
        self.rowconfigure(0, weight=1)                
        self.timeVar = tk.StringVar()
        self.timeVar.set(time.strftime(TIME_FORMAT))
        label = tk.Label(self, textvariable=self.timeVar, 
                         bg=BG, fg=FG, font=FONT)
        label.grid(sticky=tk.NSEW)
        self.lastTimeString = time.strftime(TIME_FORMAT)
        
    def refreshDisplay(self):
        newStr = time.strftime(TIME_FORMAT)
        if newStr != self.lastTimeString:
            self.timeVar.set(newStr)
            self.lastTimeString = newStr
            
if __name__ == '__main__':
    root = tk.Tk()    
    widget = SystemTimeWidget(root)
    widget.grid()
    root.mainloop() 
