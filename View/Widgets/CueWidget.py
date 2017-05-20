'''
Widget that displays cue info
'''

import tkinter as tk
from libs import string_decimal
from .ChannelWidget import autoString

FG_MAIN = 'white'
from View.Widgets.ChannelWidget import COLOR_PLAYBACK as FG_PLAY
from View.Widgets.ChannelWidget import COLOR_NONE as BG
from View.Widgets.ChannelWidget import COLOR_DIRECT as ACTIVE_CUE
BG_TITLE = 'grey'
FG_TITLE = 'black'
RELEASE = 'purple'

FONT = ('Consolas', '10')
FONT_HEADING = ('Consolas', '14', 'bold')
FONT_ACTIVE_CUE = ('Consolas', '25', 'bold')
class ChannelGroupValueCompact(tk.Frame):
    def __init__(self, *args):
        super().__init__(*args)
        self.config(bg=BG)
        self.title = tk.StringVar()
        self.cueValue = tk.StringVar()
        self.playValue = tk.StringVar()
        
        titleLabel = tk.Label(self, textvariable=self.title, bg=BG, fg=FG_MAIN, font=FONT)
        cueLabel = tk.Label(self, textvariable=self.cueValue, bg=BG, fg=FG_MAIN, font=FONT)
        playLabel = tk.Label(self, textvariable=self.playValue, bg=BG, fg=FG_PLAY, font=FONT)
        
        self.grid_columnconfigure(0, minsize=60, weight=0)
        self.grid_columnconfigure(1, minsize=40, weight=0)
        self.grid_columnconfigure(2, minsize=40, weight=0)
        
        titleLabel.grid(row=0, column=0, sticky=tk.W)        
        cueLabel.grid(row=0, column=1, sticky=tk.W)
        playLabel.grid(row=0, column=2,sticky=tk.NSEW)
        
    def setValue(self, title, cueValue, playValue):
        self.title.set(str(title) + ":")
        self.cueValue.set(cueValue)
        if playValue is not None:
            self.playValue.set('(' + autoString(playValue) + ')')
        else:
            self.playValue.set('')
    
    def clear(self):
        self.title.set('')
        self.cueValue.set('')
        self.playValue.set('')

class CompactValueFrame(tk.Frame):    
    def __init__(self, *args):
        super().__init__(*args)
        self.config(bg=BG)
        self.columnconfigure(0, weight=1, uniform='UniformGroup1')
        self.columnconfigure(1, weight=1, uniform='UniformGroup1')
        
        self.values = []
        
        # generate 5x2 frame
        for x in range(2):
            for y in range(5):
                cgvc = ChannelGroupValueCompact(self)
                cgvc.setValue('group' + str(y), '10', '10')
                cgvc.grid(row=y, column=x, sticky=tk.NSEW)
                self.values.append(cgvc)
                
    def refresh(self, bindings, playableCue):        
        i = 0
        finalBindings = {}
        for key, value in bindings.items():
            if playableCue is None:
                finalBindings[key] = [value, None]       
            else:
                finalBindings[key] = [value]
                                             
        if playableCue is not None:
            bindings2 = playableCue.getValues()
            for key, value in bindings2.items():
                finalBindings[key].append(value)
                
        for key, value in finalBindings.items():            
            self.values[i].setValue(key, value[0], value[1])
            i += 1
            
        while i < len(self.values):
            self.values[i].clear()
            i += 1
    
class CueNumberFrame(tk.Frame):
    def __init__(self, *args):
        super().__init__(*args)
        self.cueMain = tk.StringVar()
        self.cueSub = tk.StringVar()
        self.columnconfigure(0, minsize=40)
        self.columnconfigure(1, minsize=50)
        self.config(bg=BG_TITLE)
        cueMainLabel = tk.Label(self,
                                textvariable=self.cueMain,
                                bg=BG_TITLE,
                                fg=FG_TITLE,
                                justify=tk.LEFT,
                                font=FONT_HEADING)
        
        cueSubLabel = tk.Label(self,
                               textvariable=self.cueSub,
                               bg=BG_TITLE,
                               fg=FG_TITLE,
                               justify=tk.RIGHT,
                               font=FONT_HEADING)
        cueMainLabel.grid(row=0, column=0, sticky=tk.E)
        cueSubLabel.grid(row=0, column=1, sticky=tk.W)
        
    def refresh(self, string_dec):
        if string_dec is None:
            self.cueMain.set('')
            self.cueSub.set('')
        else:
            if (string_dec.mantissa == 0):
                self.cueMain.set(str(string_dec.base))
                self.cueSub.set('')
            else:                
                self.cueMain.set(str(string_dec.base))
                self.cueSub.set('.' + str(string_dec.mantissa))
UP_ARROW = '↑'
DOWN_ARROW = '↓'                                
class CueTimingFrame(tk.Frame):
    def __init__(self, *args):
        super().__init__(*args)
        self.config(bg=BG_TITLE)
        self.upLabel = tk.StringVar()
        self.downLabel = tk.StringVar()
        self.runLabel = tk.StringVar()
        self.columnconfigure(0, minsize=30, weight=1)  # blank space
        self.columnconfigure(1, minsize=40, weight=0)  # up text
        self.columnconfigure(2, minsize=5, weight=0)  # up arrow
        self.columnconfigure(3, minsize=40, weight=0)  # down text
        self.columnconfigure(4, minsize=5, weight=0)  # down arrow
        self.columnconfigure(5, minsize=80, weight=0)  # runLabel
        self.rowconfigure(0, weight=1)
        
        label1 = tk.Label(self, textvariable=self.upLabel, bg=BG_TITLE, fg=FG_TITLE, font=FONT_HEADING)
        label2 = tk.Label(self, text=UP_ARROW, bg=BG_TITLE, fg=FG_TITLE, font=FONT_HEADING)
        label3 = tk.Label(self, textvariable=self.downLabel, bg=BG_TITLE, fg=FG_TITLE, font=FONT_HEADING)
        label4 = tk.Label(self, text=DOWN_ARROW, bg=BG_TITLE, fg=FG_TITLE, font=FONT_HEADING)
        label5 = tk.Label(self, textvariable=self.runLabel, bg=BG_TITLE, fg=FG_TITLE, font=FONT_HEADING)
        
        label1.grid(row=0, column=1, sticky=tk.E)
        label2.grid(row=0, column=2, sticky=tk.W)
        label3.grid(row=0, column=3, sticky=tk.E)
        label4.grid(row=0, column=4, sticky=tk.W)
        label5.grid(row=0, column=5, sticky=tk.E)
        
    def refresh(self, up, down, run):
        self.upLabel.set(str(up))
        self.downLabel.set(str(down))    
        if run is not None:    
            self.runLabel.set(str(round(100 * run)) + '%')
        else:
            self.runLabel.set('')
        
class CueActiveFrame(tk.Frame):
    def __init__(self, *args):
        super().__init__(*args)
        self.config(bg=BG)
        self.lastColour = BG
        self.label = tk.Label(self, text='>', bg=BG, fg=BG,
                              font=FONT_ACTIVE_CUE, justify=tk.CENTER)
        self.label.place(relx=0.5, rely=0.5, anchor=tk.CENTER)
        
    def refresh(self, isActive):        
        newColour = ACTIVE_CUE if isActive else BG
        if newColour != self.lastColour:
            self.label.config(fg=newColour)
            self.lastColour = newColour
        
class CueWidget(tk.Frame):
    def __init__(self, *args):
        super().__init__(*args)
        self.config(bg='black')
        self.rowconfigure(0, weight=1)
        self.columnconfigure(0, weight=0, minsize=50)
        self.columnconfigure(1, weight=1, minsize=230)
        
        self.cnf = CueNumberFrame(self)        
        sd = string_decimal.fromStr('99.99')
        self.cnf.refresh(sd)
        
        self.ctf = CueTimingFrame(self)
        self.ctf.refresh(5, 5, 1.0)
        
        self.caf = CueActiveFrame(self)
        self.caf.refresh(False)
        
        self.cvf = CompactValueFrame(self)
        self.cvf.refresh({}, None)
                
        self.cnf.grid(row=0, column=0, sticky=tk.NSEW)
        self.ctf.grid(row=0, column=1, sticky=tk.NSEW)
        self.caf.grid(row=1, column=0, sticky=tk.NSEW)
        self.cvf.grid(row=1, column=1, sticky=tk.NSEW)
        self.isVisible = True
        
    def refreshDisplay(self, cueName, cue, selected):
        if not self.isVisible:            
            self.isVisible = True
            self.cnf.grid_forget()
            self.ctf.grid_forget()
            self.caf.grid_forget()
            self.cvf.grid_forget()  
                        
        self.cnf.refresh(cueName)            
        self.ctf.refresh(cue.upTime, cue.downTime,
                         cue.playableCue.displayPerc() if cue.playableCue else None)
        self.caf.refresh(selected)
        self.cvf.refresh(cue.mappings, cue.playableCue)
    
    def hide(self):
        if self.isVisible:
            self.isVisible = False            
            self.cnf.grid_forget()
            self.ctf.grid_forget()
            self.caf.grid_forget()
            self.cvf.grid_forget()
            
        
if __name__ == '__main__':
    root = tk.Tk()
    cw = CueWidget(root)    
    cw.grid()    
    tk.mainloop()
