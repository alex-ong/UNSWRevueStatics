import tkinter as tk

# todo: abstractmodal to inherit from
from View.ViewStyle import COLOR_NONE
from View.ViewStyle import COLOR_DIRECT as TITLE
from View.Widgets.CueWidget import UP_ARROW, DOWN_ARROW
from . import AbstractModal
from Model.ModalForms.TimeModal.TimeModal import TimeState

FG = 'white'
FONT = ('Consolas', 28)

    
class ConfirmationModal(AbstractModal.AbstractModal):
    def __init__(self, data, *args):
        super().__init__(data, *args)
    
    def subClassSetup(self):        
        self.config(bg=COLOR_NONE)
        
        self.border1 = tk.Frame(self, bg='grey', borderwidth=16)
        self.border = tk.Frame(self.border1, bg=COLOR_NONE, borderwidth=32)
        self.border.columnconfigure(1, minsize=500)
        self.border.rowconfigure(1,minsize=500)
        
        self.title = tk.Label(self.border, bg=COLOR_NONE, fg=TITLE, text='Cue 99.99', font=FONT)
        self.title.pack()
        # centre Toplevel on screen.        
        self.border.pack()
        self.border1.pack()                
        
                
    def subclassRefresh(self):  # called every frame when this form is visible                
        pass

    def showRefresh(self):  # only called when show is called
        super().showRefresh()
        self.title.configure(text=self.data.message)        
        
    def reset(self):
        pass
        
