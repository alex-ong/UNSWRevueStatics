'''
@author: alex-ong
@date 2017-05-07
'''
import tkinter as tk
import tkinter.ttk as ttk
import View.Widgets.FaderFrame as FaderFrame

from View.Widgets.ChannelWidget import ChannelWidget
from View.Widgets.GroupWidget import GroupWidget
from View.Widgets.ChannelGroupFrame import ChannelGroupFrame

class DeskView(tk.Frame):
    def __init__(self):
        root = tk.Tk()
        root.geometry('1400x700') #todo: scale to screen rez
        super().__init__(root)
        #root.overrideredirect(True) # change to windowless border        
        self.grid(sticky=tk.NSEW)
        self.config(bg='red')
        root.wm_title("UNSW Revue Statics")
        
        # this stops widgets using style elements overwriting other widgets also using styles
        self.style = ttk.Style(root)
        self.style.theme_use("winnative")
        
        self.channelFrame = None
        self.groupFrame = None
        self.faderFrame = None
        
    # called by model during setup
    def setupChannels(self, channels):
        cf = ChannelGroupFrame(channels, ChannelWidget, self)
        cf.grid(sticky=tk.NSEW)
        self.channelFrame = cf
        
    def setupGroups(self, groups):
        gf = ChannelGroupFrame(groups, GroupWidget, self)
        gf.grid(sticky=tk.NSEW)
        self.groupFrame = gf
        
    #todo: change faderLayout to "x x x  x" layout 
    def setupFaders(self, faders, faderLayout=[18, 9]):        
        ff = FaderFrame.FaderFrame(faders, faderLayout, self)
        ff.grid(sticky=tk.NSEW)
        self.faderFrame = ff
        
    def handleInput(self, dictInput):
        self.channelFrame.handleInput(dictInput)
        
    def refreshDisplay(self):
        self.channelFrame.refreshDisplay()
        self.faderFrame.refreshDisplay()
                
