import tkinter as tk

class CherryButton(tk.Frame):
    def __init__(self, label, sendLabel, *args):
        
        super().__init__(*args, height=32, width=32)        
        self.configure(bg='black')
        self.button = tk.Button(self, fg='white', bg='black', text=label)        
        self.button.pack(fill='both', expand=True)
        self.label = label
        self.button.bind("<Button-1>", self.buttonDown)
        self.button.bind("<ButtonRelease-1>", self.buttonUp)
        self.isButtonDown = False
        self.sendLabel = sendLabel
    
    def getState(self):
        return {self.sendLabel: self.isButtonDown}
    
    def buttonDown(self, *args):
        self.isButtonDown = True
        
    def buttonUp(self, *args):
        self.isButtonDown = False
