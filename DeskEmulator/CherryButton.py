import tkinter as tk

class CherryButton(tk.Frame):
    def __init__(self, label, *args):
        
        super().__init__(*args,height=32,width=32)        
        self.configure(bg='black')
        self.button = tk.Button(self, fg='white', bg='black', text=label)        
        self.button.pack(fill='both',expand=True)
