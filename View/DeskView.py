'''
@author: alex-ong
@date 2017-05-07
'''
import tkinter as tk

from View.Widgets.FaderFrame import FaderFrame
from View.Widgets.ChannelWidget import ChannelWidget
from View.Widgets.GroupWidget import GroupWidget
from View.Widgets.ChannelGroupFrame import ChannelGroupFrame
from View.Widgets.ConsoleWidget import ConsoleWidget

class DeskView(tk.Frame):
    def __init__(self):
        root = tk.Tk()
        root.geometry('1400x850')  # todo: scale to screen rez
        root.config(bg='red')
        super().__init__(root)
        # root.overrideredirect(True) # change to windowless border        
        self.grid(sticky=tk.NSEW)
        self.config(bg='red')
        root.wm_title("UNSW Revue Statics")
                
        self.columnconfigure(0, weight=1)
        
        self.channelFrame = None
        self.groupFrame = None
        self.faderFrame = None
        self.consoleWidget = None
        
    # called by model during setup
    def setupChannels(self, channels):
        cf = ChannelGroupFrame(channels, ChannelWidget, self)
        cf.grid(sticky=tk.NSEW)
        self.channelFrame = cf
        
    def setupGroups(self, groups):
        gf = ChannelGroupFrame(groups, GroupWidget, self)
        gf.grid(sticky=tk.NSEW)
        self.groupFrame = gf
        
    # todo: change faderLayout to "x x x  x" layout 
    def setupFaders(self, faders, faderLayout=[18, 9]):        
        ff = FaderFrame(faders, faderLayout, self)
        ff.grid(sticky=tk.NSEW)
        self.faderFrame = ff
    
    def setupConsole(self, console):
        cc = ConsoleWidget(console, self)
        cc.grid(sticky=tk.NSEW)
        self.consoleWidget = cc
        
    def handleInput(self, dictInput):
        self.channelFrame.handleInput(dictInput)
        
    def refreshDisplay(self):
        self.channelFrame.refreshDisplay()
        self.faderFrame.refreshDisplay()
        self.consoleWidget.refreshDisplay()
                
