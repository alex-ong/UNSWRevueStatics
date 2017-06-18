import tkinter as tk

from View.ViewStyle import COLOR_NONE
from View.ViewStyle import COLOR_DIRECT as SELECTED
from View.Widgets.CueWidget import UP_ARROW, DOWN_ARROW
from View.Modal import AbstractModal
from View.Widgets import ConsoleWidget

FG = 'white'
HEADING_BG = '#444444'
HEADING_BG2 = '#bbbbbb'
FONT = ('Consolas', 10)
TITLE_FONT = ('Consolas', 48)
NUM_ROWS = 32
NUM_COLS = int(512 / NUM_ROWS)

class DMXModal(AbstractModal.AbstractModal):
    def __init__(self, data, *args):
        super().__init__(data, *args)

    def menuName(self):
        return 'DMX Patch'
    
    def subClassSetup(self):
        self.dmxFrame = DMXModalFrame(self.menuName(), self)
        #self.consoleWidget = ConsoleWidget.ConsoleWidget(console, self)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)
        
        self.scaleToScreen()                        
        self.dmxFrame.grid(sticky=tk.NSEW)     
        #self.consoleWidget.grid(sticky=tk.NSEW)   
        
    def scaleToScreen(self):
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        self.geometry("%dx%d" % (screen_width, screen_height))
    
    def reset(self):
        pass
    
    def subclassRefresh(self):                
        #self.consoleWidget.refreshDisplay()
        self.dmxFrame.refreshDisplay()
    
class DMXModalFrame(tk.Frame):
    def __init__(self, menuName, *args):
        super().__init__(*args)
        self.menuName = menuName
        self.subclassInit()
        
    def subclassInit(self):
        self.config(bg=COLOR_NONE)
        self.rowconfigure(0, weight=1)  # top pad
        self.columnconfigure(0, weight=10)  # left pad
        for i in range(1, NUM_COLS * 2):  # setup data columns            
            if i % 2 == 0:
                self.columnconfigure(i, weight=0)
            else:
                self.columnconfigure(i, weight=1)
                
        self.columnconfigure(NUM_COLS * 2 + 1, weight=10)  # right pad
        
        self.rowconfigure(NUM_ROWS + 3, weight=1)  # bottom padding
        
        self.title = tk.Label(self, bg=COLOR_NONE, fg=FG,
                              text=self.menuName, font=TITLE_FONT)
        self.title.grid(row=1, column=1, columnspan=NUM_COLS * 2)
        
        channelNumber = 1
        for c in range(NUM_COLS * 2):
            if c % 2 == 0:
                label = tk.Label(self, bg=HEADING_BG, fg=FG,
                                 text="Channel", font=FONT)
            else:
                label = tk.Label(self, bg=HEADING_BG2, fg=COLOR_NONE,
                                 text="DMX", font=FONT)
            label.grid(row=2, column=c + 1, sticky=tk.E)
            
        for c in range(NUM_COLS * 2):
            for r in range(NUM_ROWS):   
                if c % 2 == 0:             
                    label = tk.Label(self, bg=COLOR_NONE, fg=FG,
                                     text="C" + str(channelNumber),
                                     font=FONT)
                    channelNumber += 1
                else:
                    label = tk.Label(self, bg=COLOR_NONE, fg=FG,
                                     text="D" + str(channelNumber),
                                     font=FONT)
                label.grid(row=r + 3, column=c + 1, sticky=tk.E)

    def refreshDisplay(self):
        pass
    
if __name__ == '__main__':
    root = tk.Tk()
    modal = DMXModal(None)
    modal.show(None)
    root.mainloop()
