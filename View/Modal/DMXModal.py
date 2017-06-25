import tkinter as tk

from View.ViewStyle import COLOR_NONE
from View.ViewStyle import COLOR_DIRECT as SELECTED
from View.Widgets.CueWidget import UP_ARROW, DOWN_ARROW
from View.Modal import AbstractModal
from View.Widgets import ConsoleWidget

FG = 'white'
FG_NONE = 'red'
HEADING_BG = '#444444'
HEADING_BG2 = '#bbbbbb'
FONT = ('Consolas', 18)
TITLE_FONT = ('Consolas', 48)
MAX_CHANNELS = 96
NUM_ROWS = 12
NUM_COLS = int(MAX_CHANNELS / NUM_ROWS)

class DMXModal(AbstractModal.AbstractModal):
    def __init__(self, data, *args):
        super().__init__(data, *args)

    def menuName(self):
        return 'DMX Patch'
    
    def subClassSetup(self):
        self.dmxFrame = DMXModalFrame(self.menuName(), self)
        self.configure(bg=COLOR_NONE)
        self.consoleWidget = ConsoleWidget.ConsoleWidget(self.data.console, self)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=10)
        
        self.scaleToScreen()                        
        self.dmxFrame.grid(sticky=tk.NSEW)     
        self.consoleWidget.grid(sticky=tk.NSEW)
        # emptyness at botom since windows taskbar gets in the way.  
        self.rowconfigure(2, weight=1) 
        
    def scaleToScreen(self):
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        self.geometry("%dx%d" % (screen_width, screen_height))
    
    def reset(self):
        pass
    
    def subclassRefresh(self):                
        self.consoleWidget.refreshDisplay()
        self.dmxFrame.refreshDisplay(self.data.data)
    
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
                self.columnconfigure(i, weight=0, minsize=80)
            else:
                self.columnconfigure(i, weight=1, minsize=80)
                
        self.columnconfigure(NUM_COLS * 2 + 1, weight=10)  # right pad
        
        self.rowconfigure(NUM_ROWS + 3, weight=1)  # bottom padding
        
        self.title = tk.Label(self, bg=COLOR_NONE, fg=FG,
                              text=self.menuName, font=TITLE_FONT)
        self.title.grid(row=1, column=1, columnspan=NUM_COLS * 2)
        self.channels = []
        self.addresses = []
        self.prevDMXAddresses = [None for i in range(MAX_CHANNELS)]
        channelNumber = 1
        for c in range(NUM_COLS * 2):
            if c % 2 == 0:
                label = tk.Label(self, bg=HEADING_BG, fg=FG,
                                 text="Channel", font=FONT)
            else:
                label = tk.Label(self, bg=HEADING_BG2, fg=COLOR_NONE,
                                 text="DMX", font=FONT)
            label.grid(row=2, column=c + 1, sticky=tk.EW)
            
        for c in range(NUM_COLS * 2):
            for r in range(NUM_ROWS):   
                if c % 2 == 0:             
                    label = tk.Label(self, bg=COLOR_NONE, fg=FG,
                                     text="C" + str(channelNumber),
                                     font=FONT)                    
                    self.channels.append(label)
                    channelNumber += 1
                else:
                    label = tk.Label(self, bg=COLOR_NONE, fg=FG_NONE,
                                     font=FONT, text="None")
                    self.addresses.append(label)                    
                label.grid(row=r + 3, column=c + 1, sticky=tk.E)

    def refreshDisplay(self, data):
        for i in range (1, MAX_CHANNELS + 1):
            if i in data:
                if self.prevDMXAddresses[i - 1] != data[i]:
                    self.prevDMXAddresses[i - 1] = data[i]
                    self.addresses[i - 1].config(text=str(data[i]), fg=FG)
            else:
                if self.prevDMXAddresses[i - 1] != None:
                    self.prevDMXAddresses[i - 1] = None
                    self.addresses[i - 1].config(text="None", fg=FG_NONE)
                
if __name__ == '__main__':
    root = tk.Tk()
    modal = DMXModal(None)
    modal.show(None)
    root.mainloop()
