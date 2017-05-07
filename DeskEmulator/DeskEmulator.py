import tkinter as tk

import TopPanel
import LeftPanel
import RightPanel

class DeskEmulator(tk.Frame):
    def __init__(self, *args):
        super().__init__(*args)        
        self.grid()        
        
        self.topPanel = TopPanel.TopPanel(self)
        self.topPanel.grid(row=0, columnspan=2)
        
        self.leftPanel = LeftPanel.LeftPanel(self)
        self.leftPanel.grid(row=1)
        
        self.rightPanel = RightPanel.RightPanel(self)
        self.rightPanel.grid(row=1, column=1)
if __name__ == '__main__':
    
    root = tk.Tk()
    de = DeskEmulator(root)
    
    root.mainloop()
