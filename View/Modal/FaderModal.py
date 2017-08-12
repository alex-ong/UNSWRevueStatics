import tkinter as tk

from View.ViewStyle import COLOR_NONE
from View.ViewStyle import COLOR_DIRECT as SELECTED
from View.Widgets.CueWidget import UP_ARROW, DOWN_ARROW
from View.Modal import AbstractModal
from View.Widgets import ConsoleWidget
from View.Widgets.ChannelGroupWidget import ChannelGroupWidget
from View.Widgets.GroupPatchWidget import GroupPatchWidget
from View.Widgets.CompactChannelValueWidget import  CompactChannelValueWidget

FG = 'white'
FG_NONE = 'red'
HEADING_BG = '#444444'
HEADING_BG2 = '#bbbbbb'
FONT = ('Consolas', 18)
TITLE_FONT = ('Consolas', 48)


class FaderModal(AbstractModal.AbstractModal):
    def __init__(self, data, *args):
        super().__init__(data, *args)
    
    def subClassSetup(self):
        pass
#         self.groupFrame = GroupFrame(self.data, self)
#         self.configure(bg=COLOR_NONE)
#         self.consoleWidget = ConsoleWidget.ConsoleWidget(self.data.console, self)
#         self.columnconfigure(0, weight=1)
#         self.rowconfigure(0, weight=10)
#         
#         self.scaleToScreen()                        
#         self.groupFrame.grid(sticky=tk.NSEW)     
#         self.consoleWidget.grid(sticky=tk.NSEW)
#         # emptyness at bottom since windows taskbar gets in the way.  
#         self.rowconfigure(2, weight=1,minsize=50) 
        
    def scaleToScreen(self):
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        self.geometry("%dx%d" % (screen_width, screen_height))
    
    def reset(self):
        pass
    
    def subclassRefresh(self):                
        pass
    
                    