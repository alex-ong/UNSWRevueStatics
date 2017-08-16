import tkinter as tk

# todo: abstractmodal to inherit from
from View.ViewStyle import COLOR_NONE
from View.ViewStyle import COLOR_DIRECT as TITLE
from View.Widgets.CueWidget import UP_ARROW, DOWN_ARROW
from . import AbstractModal
from Model.ModalForms.TimeModal.TimeModal import TimeState
import View.ViewStyle as VS

FG = 'white'

DESC_TEXT1 = 'Input Up time'
DESC_TEXT2 = 'Input Down time'
FONT = (VS.FONT, VS.font_size(28))
TITLE_FONT = (VS.FONT, VS.font_size(48))
COLOR_CONSOLE = 'red'
def autoString(value):
    if value is None:
        return ''
    else:
        return str(value)
    
class TimeModal(AbstractModal.AbstractModal):
    def __init__(self, data, *args):
        super().__init__(data, *args)
    
    def subClassSetup(self):        
        self.config(bg=COLOR_NONE)
        
        self.border1 = tk.Frame(self, bg='grey', borderwidth=VS.pixel_size(16))
        self.border = tk.Frame(self.border1, bg=COLOR_NONE, borderwidth=VS.pixel_size(32))
        self.border.columnconfigure(1, minsize=140)
        
        self.title = tk.Label(self.border, bg=COLOR_NONE, fg=TITLE, text='Cue 99.99', font=TITLE_FONT)
        self.descriptionText1 = tk.Label(self.border, bg=COLOR_NONE, fg=FG, text=DESC_TEXT1, font=FONT)
        self.descriptionText2 = tk.Label(self.border, bg=COLOR_NONE, fg=FG, text=DESC_TEXT2, font=FONT)
        self.answer1Str = tk.StringVar()
        self.answer2Str = tk.StringVar()
        self.answer1 = tk.Label(self.border, bg=COLOR_CONSOLE, fg=FG, textvariable=self.answer1Str, justify=tk.RIGHT, font=FONT)
        self.answer2 = tk.Label(self.border, bg=COLOR_CONSOLE, fg=FG, textvariable=self.answer2Str, font=FONT)
        self.upArrow = tk.Label(self.border, bg=COLOR_NONE, fg=FG, text=UP_ARROW, font=FONT)
        self.downArrow = tk.Label(self.border, bg=COLOR_NONE, fg=FG, text=DOWN_ARROW, font=FONT)

        self.title.grid(row=0, columnspan=3, sticky=tk.NSEW)
        self.descriptionText1.grid(row=1, column=0, sticky=tk.W)
        self.descriptionText2.grid(row=2, column=0, sticky=tk.W)
        self.answer1.grid(row=1, column=1, sticky=tk.E)
        self.answer2.grid(row=2, column=1, sticky=tk.E)
        self.upArrow.grid(row=1, column=2, sticky=tk.NSEW)
        self.downArrow.grid(row=2, column=2, sticky=tk.NSEW)
        # centre Toplevel on screen.        
        self.border.pack()
        self.border1.pack()                
        
        # todo store old values to compare every frame
        self.prevAnswer1Value = None
        self.prevAnswer2Value = None
        self.prevAnswer1Color = None
        self.prevAnswer2Color = None
        
    def subclassRefresh(self):  # called every frame when this form is visible                
        if self.data.currentState == TimeState.ENTER_UP:
            self.setAnswer1Str(autoString(self.data.upTime))
            self.setAnswer2Color(COLOR_NONE)
        elif self.data.currentState == TimeState.ENTER_DOWN:
            self.setAnswer1Color(COLOR_NONE)
            self.setAnswer2Color(COLOR_CONSOLE)
            self.setAnswer2Str(autoString(self.data.downTime))

    def showRefresh(self):  # only called when show is called
        super().showRefresh()
        self.title.configure(text=self.data.description)        
        
    def reset(self,):
        self.setAnswer1Color(COLOR_CONSOLE)
        self.setAnswer2Color(COLOR_NONE)
        self.setAnswer1Str('')
        self.setAnswer2Str('')
        
    def setAnswer1Str(self, string):
        if self.prevAnswer1Value != string:
            self.answer1Str.set(string)
            self.prevAnswer1Value = string        
    
    def setAnswer2Str(self, string):
        if self.prevAnswer2Value != string:
            self.answer2Str.set(string)
            self.prevAnswer2Value = string
    
    def setAnswer1Color(self, color):
        if self.prevAnswer1Color != color:
            self.answer1.config(bg=color)
            self.prevAnswer1Color = color
    
    def setAnswer2Color(self, color):
        if self.prevAnswer2Color != color:
            self.answer2.config(bg=color)
            self.prevAnswer2Color = color
        
    
        

if __name__ == '__main__':
    root = tk.Tk()
    tm = TimeModal(root)
    
    root.mainloop()
    
