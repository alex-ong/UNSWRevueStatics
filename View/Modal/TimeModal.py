import tkinter as tk

# todo: abstractmodal to inherit from
from View.ViewStyle import COLOR_NONE
from View.ViewStyle import COLOR_DIRECT as TITLE
from View.Widgets.CueWidget import UP_ARROW, DOWN_ARROW

from Model.ModalForms.TimeModal.TimeModal import TimeState

FG = 'white'

DESC_TEXT1 = 'Input Up time'
DESC_TEXT2 = 'Input Down time'
FONT = ('Consolas', 28)
TITLE_FONT = ('Consolas', 48)
def autoString(value):
    if value is None:
        return ''
    else:
        return str(value)
    
class TimeModal(tk.Toplevel):
    def __init__(self, data, *args):
        super().__init__(*args)        
        self.data = data
        self.closeCallback = None
        self.config(bg=COLOR_NONE)
        
        self.border1 = tk.Frame(self, bg='grey', borderwidth=16)
        self.border = tk.Frame(self.border1, bg=COLOR_NONE, borderwidth=32)
        self.border.columnconfigure(1, minsize=140)
        
        self.title = tk.Label(self.border, bg=COLOR_NONE, fg=TITLE, text='Cue 99.99', font=TITLE_FONT)
        self.descriptionText1 = tk.Label(self.border, bg=COLOR_NONE, fg=FG, text=DESC_TEXT1, font=FONT)
        self.descriptionText2 = tk.Label(self.border, bg=COLOR_NONE, fg=FG, text=DESC_TEXT2, font=FONT)
        self.answer1Str = tk.StringVar()
        self.answer2Str = tk.StringVar()
        self.answer1 = tk.Label(self.border, bg='red', fg=FG, textvariable=self.answer1Str, justify=tk.RIGHT, font=FONT)
        self.answer2 = tk.Label(self.border, bg='red', fg=FG, textvariable=self.answer2Str, font=FONT)
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
        self.centreOnScreen()  
        self.overrideredirect(True)
        self.isVisible = False      
        self.hide()
        # todo store old values to compare every frame
        # prevAnswer1Value = None
        # prevAnswer2Value = None
        
    def refresh(self):  # called every frame when this form is visible
        if self.isVisible:        
            if self.data.currentState == TimeState.ENTER_UP:
                self.answer1Str.set(autoString(self.data.upTime))
                self.answer2.config(bg=COLOR_NONE)
            elif self.data.currentState == TimeState.ENTER_DOWN:
                self.answer1.config(bg=COLOR_NONE)
                self.answer2.config(bg='red')
                self.answer2Str.set(autoString(self.data.downTime))

    def showRefresh(self):  # only called when show is called
        self.title.configure(text=self.data.description)
        self.refresh()
        
    def centreOnScreen(self):
        self.update_idletasks()  # refresh widget to get correct size
        w = self.winfo_width()
        h = self.winfo_height()
        geoString = '%dx%d+%d+%d' % (w, h,
                                     int(self.winfo_screenwidth() / 2 - 0.5 * w),
                                     int(self.winfo_screenheight() / 2 - 0.5 * h))        
        self.geometry(geoString)    
    
    def show(self, data):
        self.data = data        
        self.deiconify()        
        self.overrideredirect(True)
        self.isVisible = True        
        self.showRefresh()
        
    def hide(self):
        self.overrideredirect(False)
        self.withdraw()
        self.isVisible = False
                        
    def reset(self,):
        self.descriptionText2.config(fg=COLOR_NONE)
        
    def done(self, result):
        self.closeCallback(result)
        
    
        
        
if __name__ == '__main__':
    root = tk.Tk()
    tm = TimeModal(root)
    
    root.mainloop()
    
