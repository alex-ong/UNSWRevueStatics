import tkinter as tk

from View.ViewStyle import COLOR_NONE
from View.Modal import AbstractModal
from View.Widgets import ConsoleWidget
from View.Widgets.FaderPatchWidget import FaderPatchWidget
from View.Widgets.FunctionButtonWidget import FunctionButtonFrame

#bad hack - using a global directly instead of asking model for it
from Model.OptionButtons import getInstance as OptionFunc

import View.ViewStyle as VS 
FG = 'white'
FG_NONE = 'red'
HEADING_BG = '#444444'
HEADING_BG2 = '#bbbbbb'
FONT = (VS.FONT, VS.font_size(18))
TITLE_FONT = (VS.FONT, VS.font_size(48))


class FaderModal(AbstractModal.AbstractModal):
    def __init__(self, data, *args):
        super().__init__(data, *args)
    
    def subClassSetup(self):        
        self.configure(bg=COLOR_NONE)
        
        self.patchFrame = FaderPatchFrame(self.data, self)        
        self.selectedFrame = SelectedBindingLabel(self.data,self)
        self.consoleWidget = ConsoleWidget.ConsoleWidget(self.data.console, self)
        self.functionButtonFrame = FunctionButtonFrame(OptionFunc().getCurrentState, self)
        
        self.columnconfigure(0, weight=1)        
        self.rowconfigure(0, weight=VS.pixel_size(10))
        self.rowconfigure(1, minsize=VS.pixel_size(50))
  
        self.scaleToScreen()                        
        self.patchFrame.grid(sticky=tk.NSEW,row=0, columnspan=2) #row = 0   
        self.selectedFrame.grid(sticky=tk.NSEW,row=1, columnspan=2) #row = 1
        self.consoleWidget.grid(sticky=tk.NSEW,row=2) #row = 2, column = 1
        self.functionButtonFrame.grid(sticky=tk.NSEW,row=2,column=2) #row = 2, column = 2
        
        # emptyness at bottom since windows taskbar gets in the way.  
        self.rowconfigure(3, weight=1,minsize=VS.pixel_size(50)) 
        
    def scaleToScreen(self):        
        self.geometry(VS.SCREEN_RESOLUTION)
    
    def reset(self):
        pass
    
    def subclassRefresh(self):                
        self.consoleWidget.refreshDisplay()
        self.patchFrame.refreshDisplay()
        self.selectedFrame.refreshDisplay()
        self.functionButtonFrame.refreshDisplay()
    
NUM_COLS = 18
NUM_ROWS = 2
NUM_FADERS = 27 #TODO read this from config file.
class FaderPatchFrame(tk.Frame):
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
            self.columnconfigure(i, weight=1, minsize=VS.pixel_size(80))
        self.columnconfigure(NUM_COLS + 1, weight=10)  # left pad
        
        for i in range(1, NUM_ROWS):
            self.rowconfigure(i, weight=1, minsize=VS.pixel_size(100))
        self.rowconfigure(NUM_ROWS + 2, weight=1,minsize=VS.pixel_size(200))  # bottom padding
        self.rowconfigure(NUM_ROWS + 3, weight=1)  # bottom padding
        
        #currentPageNumber = self.data.currentPageNumber
        self.title = tk.Label(self, bg=COLOR_NONE, fg=FG,
                              text="Fader Patch Menu", font=TITLE_FONT)
        self.title.grid(row=1, column=1, columnspan=NUM_COLS)
        
        data = self.data.getFaders()
        
        for i in range(1, NUM_FADERS+1):            
            row = (i-1) // NUM_COLS
            col = (i-1) % NUM_COLS            
            
            faderPatch = None #points to a channel or group object
            if i in data:
                faderPatch = data[i]
                             
            groupWidget = FaderPatchWidget(i, faderPatch, self) 
            groupWidget.grid(row=row+2, column=col + 1, sticky=tk.NSEW)
            self.widgets.append(groupWidget)

    
    def refreshDisplay(self):
        faders = self.data.getFaders()
        for i in range(1, NUM_FADERS+1):                
            widget = self.widgets[i-1]
            if i in faders:
                widget.refreshDisplay(faders[i])

    
class SelectedBindingLabel(tk.Frame):
    def __init__(self, data, *args):
        super().__init__(*args)
        self.columnconfigure(0, weight=1) #force label to take up entire frame
        self.data = data
        self.config(bg=COLOR_NONE)
        self.labelString = tk.StringVar()        
        self.label = tk.Label(self, textvariable=self.labelString, font=TITLE_FONT, 
                              fg=FG, bg=COLOR_NONE,justify=tk.CENTER)
        self.label.grid(sticky=tk.NSEW)
        self.prevValue = ''
        
    def refreshDisplay(self):        
        newValue = str(self.data.currentMappings)
        if newValue != self.prevValue:            
            self.prevValue = newValue
            self.labelString.set("Selected: " + self.prevValue)
            