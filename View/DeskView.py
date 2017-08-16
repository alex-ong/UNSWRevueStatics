'''
@author: alex-ong
@date 2017-05-07
'''
import tkinter as tk
import os

from View.Widgets.FaderFrame import FaderFrame
from View.Widgets.ChannelGroupFrame import ChannelGroupFrame
from View.Widgets.ConsoleWidget import ConsoleWidget
from View.Widgets.CueListWidget import CueListWidget
from View.Modal.ModalManager import ModalManager
from View.Widgets.ChannelGroupWidget import ChannelGroupWidget
from View.ViewStyle import CHANNEL, GROUP, SCREEN_RESOLUTION

class DeskView(tk.Frame):
        
    def __init__(self, keyboardHandler=None):
        self.keyboardHandler = keyboardHandler
                
        root = tk.Tk()        
        root.config(bg='blue')
        super().__init__(root)        
        root.geometry(SCREEN_RESOLUTION)        
        root.overrideredirect(True)  # change to windowless border        
        root.wm_title("UNSW Revue Statics")
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        
        # the following captures input as long as the application is open        
        root.bind('<KeyPress>', self.keyboardHandler)
        self.root = root
                        
        self.grid(sticky=tk.NSEW)
        self.config(bg='red')
        NUM_ROWS = 3
        NUM_COLS = 2
        for i in range(NUM_ROWS):
            self.rowconfigure(i, weight=1)
        for i in range(NUM_COLS):
            self.columnconfigure(i, weight=1)
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
        cc.grid(row=2, column=1, sticky=tk.NSEW)
        self.consoleWidget = cc
        
    def setupCueList(self, cueList):
        cl = CueListWidget(cueList, self)
        cl.grid(row=0, column=0, rowspan=3, sticky=tk.NSEW)
        self.cueListWidget = cl
        
    def setupModalForms(self, modalModel):
        mm = ModalManager(modalModel, self.keyboardHandler, self)
        self.modalManager = mm
        
    def handleInput(self, dictInput):
        self.channelFrame.handleInput(dictInput)
        
    def refreshDisplay(self):
        self.channelFrame.refreshDisplay()
        self.faderFrame.refreshDisplay()
        self.consoleWidget.refreshDisplay()
        self.cueListWidget.refreshDisplay()
        self.modalManager.refreshDisplay()
