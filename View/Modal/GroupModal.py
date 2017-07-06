import tkinter as tk

from View.ViewStyle import COLOR_NONE
from View.ViewStyle import COLOR_DIRECT as SELECTED
from View.Widgets.CueWidget import UP_ARROW, DOWN_ARROW
from View.Modal import AbstractModal
from View.Widgets import ConsoleWidget
from View.Widgets.GroupWidget import GroupWidget
from View.Widgets.GroupPatchWidget import GroupPatchWidget

FG = 'white'
FG_NONE = 'red'
HEADING_BG = '#444444'
HEADING_BG2 = '#bbbbbb'
FONT = ('Consolas', 18)
TITLE_FONT = ('Consolas', 48)

MAX_GROUPS = 54
NUM_ROWS = 5
NUM_COLS = int(MAX_GROUPS / NUM_ROWS)

class GroupModal(AbstractModal.AbstractModal):
    def __init__(self, data, *args):
        super().__init__(data, *args)
    
    def subClassSetup(self):
        self.groupFrame = GroupFrame(self.data, self)
        self.configure(bg=COLOR_NONE)
        self.consoleWidget = ConsoleWidget.ConsoleWidget(self.data.console, self)
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=10)
        
        self.scaleToScreen()                        
        self.groupFrame.grid(sticky=tk.NSEW)     
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
        self.groupFrame.refreshDisplay()
    

                    
class GroupFrame(tk.Frame):
    def __init__(self, data, *args):
        super().__init__(*args)
        self.data = data
        self.widgets = []
        self.subclassInit()
        
    def subclassInit(self):
        self.config(bg=COLOR_NONE)
        self.rowconfigure(0, weight=1)  # top pad
        self.columnconfigure(0, weight=10)  # left pad
        for i in range(1, NUM_COLS):  # setup data columns                    
            self.columnconfigure(i, weight=1, minsize=80)
        self.columnconfigure(NUM_COLS + 1, weight=10)  # left pad
        for i in range(1, NUM_ROWS):
            self.rowconfigure(i, weight=1, minsize=100)
        self.rowconfigure(NUM_ROWS + 2, weight=1)  # bottom padding
        
        self.title = tk.Label(self, bg=COLOR_NONE, fg=FG,
                              text="Group Menu", font=TITLE_FONT)
        self.title.grid(row=1, column=1, columnspan=NUM_COLS)
        
        data = self.data.getModelGroups()
        for i in range(1, MAX_GROUPS+1):            
            row = (i-1) // NUM_COLS
            col = (i-1) % NUM_COLS             
            if i in data:
                groupWidget = GroupPatchWidget(data[i], self) 
                groupWidget.grid(row=row+2, column=col + 1, sticky=tk.E)
                self.widgets.append(groupWidget)
    def refreshDisplay(self):        
        for widget in self.widgets:
            widget.refreshDisplay()
                
if __name__ == '__main__':
    root = tk.Tk()
    modal = DMXModal(None)
    modal.show(None)
    root.mainloop()