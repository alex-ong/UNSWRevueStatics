import tkinter as tk
import SliderPlusButton
import CherryButton

buttons = [['<-', 'Delete', '-', '+', '', 'Clear', 'Menu'],
           ['7', '8', '9', 'Thru', '', 'Cue', 'S1'],
           ['4', '5', '6', 'Full', '', 'Group', 'S2'],
           ['1', '2', '3', '@', '', 'Time', 'S3'],
           ['0', '.', 'Enter', '', '', 'Rec', 'S4']]

RECORD = 'Record'
THRU = 'Thru'
GROUP = 'Group'
CHANNEL = 'Channel'
CUE = 'Cue'
FADER = 'Fader'
AT = '@'
PLUS = '+'
MINUS = '-'
NUMBER = 'Number'
DECIMAL = '.'
DELETE = 'Delete'

#quickly map from buttonName to correct name to send
buttonToSendMapping = {'Rec': RECORD,
                       }
class RightPanel(tk.Frame):
    def __init__(self, *args):
        super().__init__(*args)
        self.buttons = []
        self.grid_columnconfigure(0, minsize=32)
        self.grid_columnconfigure(1, minsize=32)
        self.grid_columnconfigure(2, minsize=32)
        self.grid_columnconfigure(3, minsize=32)    
        self.grid_columnconfigure(4, minsize=5)
        self.grid_columnconfigure(5, minsize=32)
        self.grid_columnconfigure(6, minsize=32)
                
        self.grid_rowconfigure(0, minsize=32)
        self.grid_rowconfigure(1, minsize=32)
        self.grid_rowconfigure(2, minsize=32)
        self.grid_rowconfigure(3, minsize=32)
        self.grid_rowconfigure(4, minsize=32)                    
        self.initPanel()
        

    def initPanel(self):        
        for y in range(len(buttons)):
            for x in range(len(buttons[y])):
                label = buttons[y][x]
                if label == '':
                    continue
                if label in buttonToSendMapping:
                    sendLabel = buttonToSendMapping[label]
                else:
                    sendLabel = label
                cherryButton = CherryButton.CherryButton(buttons[y][x], sendLabel, self)
                if label == 'Enter':
                    cherryButton.grid(row=y, column=x, columnspan=2, sticky=tk.NSEW)
                else:
                    cherryButton.grid(row=y, column=x, sticky=tk.NSEW)
                
                self.buttons.append(cherryButton)
             
    def getState(self):
        result = {}
        for button in self.buttons:
            result.update(button.getState())
        return result
