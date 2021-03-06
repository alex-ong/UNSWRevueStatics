import tkinter as tk

# todo: abstractmodal to inherit from
from View.ViewStyle import COLOR_NONE
from View.ViewStyle import COLOR_DIRECT as TITLE
from View.Widgets.CueWidget import UP_ARROW, DOWN_ARROW
from . import AbstractModal
from Model.ModalForms.TimeModal.TimeModal import TimeState

import View.ViewStyle as VS

FG = 'white'
FONT = (VS.FONT, VS.font_size(28))

    
class ConfirmationModal(AbstractModal.AbstractModal):
    def __init__(self, data, *args):
        super().__init__(data, *args)
    
    def subClassSetup(self):        
        self.config(bg=COLOR_NONE)
        
        self.border1 = tk.Frame(self, bg='grey', borderwidth=16)
        self.border1.columnconfigure(0, weight=1)
        self.border1.rowconfigure(0, weight=1)
        self.border = tk.Frame(self.border1, bg=COLOR_NONE, borderwidth=VS.pixel_size(32))
        self.border.columnconfigure(0, minsize=VS.pixel_size(400), weight=0)
        self.border.rowconfigure(0, minsize=VS.pixel_size(100), weight=0)
        
        self.title = tk.Label(self.border, bg=COLOR_NONE, fg=FG,
                              text=self.splitWords('This is a super long message that is too long'),
                              font=FONT)
        self.title.grid(sticky=tk.NSEW)
        
        self.confirmationLabel = tk.Label(self.border, bg=COLOR_NONE, fg=FG,
                                          text='Enter: Confirm\nMenu/Clear: Cancel')
        self.confirmationLabel.grid(sticky=tk.NSEW)
        # centre Toplevel on screen.        
        self.border.grid(sticky=tk.NSEW)
        self.border1.grid(sticky=tk.NSEW)                        
                
    def subclassRefresh(self):  # called every frame when this form is visible                
        pass

    def splitWords(self, message):
        words = message.split()
        lines = []
        line = ""
        LIMIT = 25
        for word in words:
            if len(line) > 0 and len(line) + len(word) > LIMIT:
                lines.append(line)
                line = word
            elif len(line) == 0:
                line = word
            else:
                line = line + " " + word
        lines.append(line)
        return "\n".join(lines)
        
    def showRefresh(self):  # only called when show is called
        super().showRefresh()        
        self.title.configure(text=self.splitWords(self.data.message))        
        
    def reset(self):
        pass
        
