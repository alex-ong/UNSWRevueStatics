import tkinter as tk

from View.ViewStyle import COLOR_NONE
from View.ViewStyle import COLOR_DIRECT as SELECTED
from View.Widgets.CueWidget import UP_ARROW, DOWN_ARROW
from View.Modal import AbstractModal

FG = 'white'

FONT = ('Consolas', 28)
TITLE_FONT = ('Consolas', 48)

class MainMenuModal(AbstractModal.AbstractModal):
    def __init__(self, data, *args):
        super().__init__(data, *args)
        
    def subClassSetup(self):
        self.config(bg=COLOR_NONE)
        self.rowconfigure(0, weight=1)  # top pad
        self.columnconfigure(0, weight=1)  # left pad
        self.columnconfigure(1, weight=0)  # label
        self.columnconfigure(2, weight=0)  # meta info
        self.columnconfigure(3, weight=1)  # right pad
        
        self.title = tk.Label(self, bg=COLOR_NONE, fg=FG,
                              text='Main Menu', font=TITLE_FONT)
        
        self.options = []  # label/bool pairs. The bool represents selected. 
        
        for option in self.data.mainMenuOptions:
            string = option[0]
            index = len(self.options) + 1
            stringOpt = tk.Label(self, bg=COLOR_NONE, fg=FG,
                                 text=str(index) + ' - ' + string,
                                 justify=tk.LEFT, font=FONT)
            self.options.append([stringOpt, False])
            
        row = 1
        self.title.grid(row=row, column=1, columnspan=2)
        row += 1
        for option in self.options:
            option[0].grid(row=row, column=1, sticky=tk.W)
            row += 1
        self.rowconfigure(row, weight=1)  # bottom padding
        self.scaleToScreen()
        
    def scaleToScreen(self):
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        self.geometry("%dx%d" % (screen_width, screen_height))
    
    def setOptionSelected(self, index, selected):    
        if (self.options[index][1] != selected):            
            self.options[index][1] = selected
            colour = SELECTED if selected else FG
            self.options[index][0].config(fg=colour)
            
    def resetSelected(self):
        for index in range(len(self.options)):
            self.setOptionSelected(index, False)
    
    def reset(self):
        self.resetSelected()
        
    def subclassRefresh(self):        
        self.resetSelected()
        if self.data.currentSelection is not None:
            self.setOptionSelected(self.data.currentSelection, True)
        
class Tester():
    def __init__(self):
        self.mainMenuOptions = [('option1', None),
                                ('option2', None),
                                ('option3', None),
                                ('option4', None)]
if __name__ == '__main__':
    root = tk.Tk()
    data = Tester()
    
                                
    mm = MainMenuModal(data)
    mm.show(None)
    root.mainloop()
