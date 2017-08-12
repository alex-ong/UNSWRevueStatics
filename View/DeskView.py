'''
@author: alex-ong
@date 2017-05-07
'''
import tkinter as tk

from View.Widgets.FaderFrame import FaderFrame
from View.Widgets.ChannelGroupFrame import ChannelGroupFrame
from View.Widgets.ConsoleWidget import ConsoleWidget
from View.Widgets.CueListWidget import CueListWidget
from View.Modal.ModalManager import ModalManager
from View.Widgets.ChannelGroupWidget import ChannelGroupWidget
from View.ViewStyle import CHANNEL, GROUP

class DeskView(tk.Frame):
    def __init__(self):
        root = tk.Tk()        
        root.config(bg='red')
        super().__init__(root)
        root.overrideredirect(True) # change to windowless border                
        self.grid(sticky=tk.NSEW)
        self.config(bg='red')
        root.wm_title("UNSW Revue Statics")
                
        self.columnconfigure(0, weight=1)
        
        self.channelFrame = None
        self.groupFrame = None
        self.faderFrame = None
        self.consoleWidget = None
        self.cueListWidget = None
        self.modalManager = None
        
    # called by model during setup
    def setupChannels(self, channels):
        cf = ChannelGroupFrame(channels, CHANNEL, self)
        cf.grid(row=0, column=1, sticky=tk.NSEW)
        self.channelFrame = cf    
    
    # not used
    def setupGroups(self, groups):
        gf = ChannelGroupFrame(groups, GROUP, self)
        gf.grid(sticky=tk.NSEW)
        self.groupFrame = gf
        
    # todo: change faderLayout to "x x x  x" layout 
    def setupFaders(self, getFaderFunc, numFaders, faderLayout=[18, 9]):        
        ff = FaderFrame(getFaderFunc, numFaders, faderLayout, self)
        ff.grid(row=1, column=1, sticky=tk.NSEW)
        self.faderFrame = ff
    
    def setupConsole(self, console):
        cc = ConsoleWidget(console, self)
        cc.grid(row=2, column=1, columnspan=2, sticky=tk.NSEW)
        self.consoleWidget = cc
        
    def setupCueList(self, cueList):
        cl = CueListWidget(cueList, self)
        cl.grid(row=0, column=0,rowspan=3, sticky=tk.NSEW)
        self.cueListWidget = cl
        
    def setupModalForms(self, modalModel):
        mm = ModalManager(modalModel)
        self.modalManager = mm
        
    def handleInput(self, dictInput):
        self.channelFrame.handleInput(dictInput)
        
    def refreshDisplay(self):
        self.channelFrame.refreshDisplay()
        self.faderFrame.refreshDisplay()
        self.consoleWidget.refreshDisplay()
        self.cueListWidget.refreshDisplay()
        self.modalManager.refreshDisplay()
