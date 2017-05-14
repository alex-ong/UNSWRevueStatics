'''
Console widget.
Displays a list of strings.
'''

import tkinter as tk

BG = 'disabledbackground'
FG = 'disabledforeground'

VALID_COMMAND_FG = 'black'
INVALID_COMMAND_FG = 'red' #not sure if we're going to use this yet

EXECUTED_COMMAND_BG = 'grey'
NORMAL_COMMAND_BG = 'white'

appearance = {BG: NORMAL_COMMAND_BG,
              FG: VALID_COMMAND_FG,
              'font':  ('Consolas',16,'bold')              
              }

class ConsoleWidget(tk.Entry):
    def __init__(self, console, *args, **kwargs):
        self.s = tk.StringVar()
        kwargs.update(appearance)
        kwargs['textvariable'] = self.s
        
        super().__init__(*args, **kwargs)
        self.configure(state=tk.DISABLED)
        self.setValue([])
        
    def setValue(self, tokens):
        #reset background
        self.configure({BG:NORMAL_COMMAND_BG})        
        
        self.configure(state=tk.NORMAL)
        self.s.set(' '.join(tokens))
        self.configure(state=tk.DISABLED)
        
    def executeCommand(self):
        self.configure({BG:EXECUTED_COMMAND_BG})