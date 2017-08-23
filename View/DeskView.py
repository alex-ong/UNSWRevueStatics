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
from View.Widgets.FunctionButtonWidget import FunctionButtonFrame
from View.Widgets.TopBar import TopBar
class DeskView(tk.Frame):
        
    def __init__(self, keyDownHandler, keyUpHandler):
        self.keyDownHandler = keyDownHandler
        self.keyUpHandler = keyUpHandler
                
        root = tk.Tk()        
        root.config(bg='blue')
        super().__init__(root)        
        root.geometry(SCREEN_RESOLUTION)        
        root.overrideredirect(True)  # change to windowless border        
        root.wm_title("UNSW Revue Statics")
        root.columnconfigure(0, weight=1)
        root.rowconfigure(0, weight=1)
        
        # the following captures input as long as the application is open        
        root.bind('<KeyPress>', self.keyDownHandler)
        root.bind('<KeyRelease>', self.keyUpHandler)
        self.root = root
                        
        self.grid(sticky=tk.NSEW)
        self.config(bg='red')
        NUM_ROWS = 3
        NUM_COLS = 4
        for i in range(NUM_ROWS):
            self.rowconfigure(i, weight=1)
        
        self.columnconfigure(0,weight=0)
        self.columnconfigure(1,weight=1)
        self.columnconfigure(2,weight=1)
        self.columnconfigure(3,weight=0)
        
        
        self.channelFrame = None
        self.groupFrame = None
        self.faderFrame = None
        self.consoleWidget = None
        self.cueListWidget = None
        self.modalManager = None
        self.topBar = None
        
    # called by model during setup
    def setupChannels(self, channels):
        cf = ChannelGroupFrame(channels, CHANNEL, self)
        cf.grid(row=1, column=1, sticky=tk.NSEW, columnspan=3)
        self.channelFrame = cf    
    
    # not used
    def setupGroups(self, groups):
        gf = ChannelGroupFrame(groups, GROUP, self)
        gf.grid(sticky=tk.NSEW)
        self.groupFrame = gf
        
    # todo: change faderLayout to "x x x  x" layout 
    def setupFaders(self, getFaderFunc, numFaders, faderLayout=[18, 9]):        
        ff = FaderFrame(getFaderFunc, numFaders, faderLayout, self)
        ff.grid(row=2, column=1, sticky=tk.NSEW, columnspan=3)
        self.faderFrame = ff
    
    def setupConsole(self, console):
        cc = ConsoleWidget(console, self)
        cc.grid(row=3, column=1,columnspan=2, sticky=tk.NSEW)
        self.consoleWidget = cc
        
    def setupFunctionButtons(self, func):
        fb = FunctionButtonFrame(func, self)
        fb.grid(row=3, column=3, sticky=tk.NSEW)
        self.functionButtonFrame = fb
    
    def setupCueList(self, cueList):
        cl = CueListWidget(cueList, self)
        cl.grid(row=1, column=0, rowspan=3, sticky=tk.NSEW)
        self.cueListWidget = cl
        
    def setupModalForms(self, modalModel):
        mm = ModalManager(modalModel, self.keyDownHandler, self.keyUpHandler, self)
        self.modalManager = mm
    
    def setupTopBar(self, gmPerc):        
        tb = TopBar(gmPerc, self)
        tb.grid(row=0, column=0, columnspan=4, sticky=tk.NSEW)
        self.topBar = tb
                
    def handleInput(self, dictInput):
        self.channelFrame.handleInput(dictInput)
        
    def refreshDisplay(self):
        self.channelFrame.refreshDisplay()
        self.faderFrame.refreshDisplay()
        self.consoleWidget.refreshDisplay()
        self.cueListWidget.refreshDisplay()
        self.modalManager.refreshDisplay()
        self.functionButtonFrame.refreshDisplay()
        self.topBar.refreshDisplay()
