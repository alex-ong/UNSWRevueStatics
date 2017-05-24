import tkinter as tk

# todo: abstractmodal to inherit from
from View.ViewStyle import COLOR_NONE
from View.ViewStyle import COLOR_DIRECT as TITLE
from View.Widgets.CueWidget import UP_ARROW, DOWN_ARROW

FG = 'white'

DESC_TEXT1 = 'Input Up time'
DESC_TEXT2 = 'Input Down time'
FONT = ('Consolas', 28)
TITLE_FONT = ('Consolas', 48)
class TimeModal(tk.Toplevel):
    def __init__(self, data, *args):
        super().__init__(*args)        
        self.data = None
        self.closeCallback = None
        self.config(bg=COLOR_NONE)
        
        self.border1 = tk.Frame(self, bg='grey',borderwidth=16)
        self.border = tk.Frame(self.border1, bg=COLOR_NONE,borderwidth=32)
        self.border.columnconfigure(1,minsize=140)
        
        self.title = tk.Label(self.border,bg=COLOR_NONE,fg=TITLE, text='Cue 99.99', font=TITLE_FONT)
        self.descriptionText1 = tk.Label(self.border, bg=COLOR_NONE,fg=FG, text = DESC_TEXT1, font=FONT)
        self.descriptionText2 = tk.Label(self.border, bg=COLOR_NONE,fg=FG, text = DESC_TEXT2, font=FONT)
        self.answer1 = tk.Label(self.border, bg='red',fg=FG, text='2', justify=tk.RIGHT, font=FONT)
        self.answer2 = tk.Label(self.border, bg='red',fg=FG, text='2.999', font=FONT)
        self.upArrow = tk.Label(self.border, bg=COLOR_NONE,fg=FG, text=UP_ARROW, font=FONT)
        self.downArrow = tk.Label(self.border, bg=COLOR_NONE,fg=FG, text=DOWN_ARROW, font=FONT)
        
        self.title.grid(row=0,columnspan=3,sticky=tk.NSEW)
        self.descriptionText1.grid(row=1,column=0, sticky=tk.W)
        self.descriptionText2.grid(row=2,column=0, sticky=tk.W)
        self.answer1.grid(row=1,column=1,sticky=tk.E)
        self.answer2.grid(row=2,column=1,sticky=tk.E)
        self.upArrow.grid(row=1,column=2,sticky=tk.NSEW)
        self.downArrow.grid(row=2,column=2,sticky=tk.NSEW)
        # centre Toplevel on screen.        
        self.border.pack()
        self.border1.pack()
        self.overrideredirect(True) #borderless
        self.centreOnScreen()
        
    def centreOnScreen(self):
        self.update_idletasks() #refresh widget to get correct size
        w = self.winfo_width()
        h = self.winfo_height()
        geoString = '%dx%d+%d+%d' % (w, h, 
                                     int(self.winfo_screenwidth() / 2 - 0.5* w),
                                     int(self.winfo_screenheight() / 2 - 0.5* h))        
        self.geometry(geoString)
    def show(self, data, callback):
        self.data = data
        # self.configure(self.winfo_screenwidth())
                
    def reset(self, ):
        self.descriptionText2.config(fg=COLOR_NONE)
        
    def done(self, result):
        self.closeCallback(result)
        
    
        
        
if __name__ == '__main__':
    root = tk.Tk()
    tm = TimeModal(root)
    
    root.mainloop()
    
