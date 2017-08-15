'''
Console widget.
Displays a list of strings.
'''

import tkinter as tk

BG = 'disabledbackground'
FG = 'disabledforeground'

VALID_COMMAND_FG = 'black'
INVALID_COMMAND_FG = 'red'  # not sure if we're going to use this yet

EXECUTED_COMMAND_BG = 'grey'
NORMAL_COMMAND_BG = 'white'

FONT = ('Consolas', 16, 'bold')              
      
NUM_PREV_COMMANDS = 3
class ConsoleWidget(tk.Frame):
    def __init__(self, console, *args):
        super().__init__(*args)
        self.columnconfigure(0, weight=1)
        for i in range (NUM_PREV_COMMANDS + 1):
            self.rowconfigure(i, weight=1)
            
        self.console = console
        self.currentCommandVar = tk.StringVar()
        self.currentCommand = self.makeEntry(self.currentCommandVar, NORMAL_COMMAND_BG)
        self.lockEntry(self.currentCommand)  
        self.currentCommand.grid(sticky=tk.NSEW)
        
        self.lastCommandResultVars = []
        self.lastCommandResultEntries = []
        self.lastCommandResultStrings = []
        for i in range(NUM_PREV_COMMANDS):
            self.lastCommandResultVars.append(tk.StringVar())
            self.lastCommandResultEntries.append(self.makeEntry(self.lastCommandResultVars[i], EXECUTED_COMMAND_BG))
            self.lockEntry(self.lastCommandResultEntries[i])
            self.lastCommandResultEntries[i].grid(sticky=tk.NSEW)            
            
        self.lastTokens = []
        self.setValue([])        
                
    def makeEntry(self, textVariable, disabledColour):
        return tk.Entry(self, textvariable=textVariable,
                       disabledbackground=disabledColour,
                       disabledforeground=VALID_COMMAND_FG,
                       font=FONT)
        
    #######################################################
    # Lock and unlock entries so user's can't click on them
    #######################################################
    def lockEntry(self, entry):
        entry.configure(state=tk.DISABLED)
        
    def unlockEntry(self, entry):
        entry.configure(state=tk.NORMAL)
        
    def setValue(self, tokens):
        self.unlockEntry(self.currentCommand)                        
        self.currentCommandVar.set(' '.join(tokens))
        self.lockEntry(self.currentCommand)        
        self.lastTokens = tokens
    
    def updateHistory(self, history):
        self.lastCommandResultStrings = history
        for i in range (NUM_PREV_COMMANDS):
            stringValue = ''
            if i < len(history):
                stringValue = history[i]
                self.unlockEntry(self.lastCommandResultEntries[i])
                self.lastCommandResultVars[i].set(stringValue)
                self.lockEntry(self.lastCommandResultEntries[i])
                    
    def refreshDisplay(self):        
        if self.lastTokens != self.console.tokens:            
            self.setValue(self.console.tokens.copy())
        # construct console history strings
        consoleHistory = []
        for i in range(NUM_PREV_COMMANDS):
            if len(self.console.lastCommandResults) > i:
                consoleHistory.append(str(self.console.lastCommandResults[i]))
        
        if self.lastCommandResultStrings != consoleHistory:
            print (consoleHistory)
            self.updateHistory(consoleHistory.copy())
            
