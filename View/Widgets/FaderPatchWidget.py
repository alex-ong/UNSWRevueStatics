'''
FaderPatchFrame

Shows what the fader is patched to.
@author: alex-ong
@date 2017-08-13
'''

from View.ViewStyle import COLOR_DIRECT, COLOR_GROUP, COLOR_PLAYBACK, COLOR_RECORD, COLOR_NONE, CHANNEL, GROUP
from View.ViewStyle import typeColourMapping
from View.Widgets.ChannelGroupWidget import bindingIsChannel, bindingIsGroup
HEADING_FONT = ('Consolas', 10)
FONT = ('Consolas', 8)

class FaderPatchWidget(tk.Frame):
    def __init__(self, fader,  *args):
        super().__init__(*args)
        
        self.config(bg='black')
        self.fader = fader
        faderBinding = self.fader.getBinding()
        
        bindingType = self.getBindingType()
        
        self.columnconfigure(0, weight=0, minsize=100)                        
        self.rowconfigure(1, weight=0, minsize=100)
                
        self.headingLabel = tk.Label(self, text=str(self.fader.number).zfill(2), 
                                     font=HEADING_FONT, fg='grey', bg='black')
        self.patchLabel = tk.Label(self, text=self.getFaderLabelString(), font=FONT, 
                                   fg=typeColourMapping[bindingType], bg='black')
        self.headingLabel.grid(sticky=tk.NSEW)
        self.patchLabel.grid(sticky=tk.NSEW)
        
    def getBindingType(self):
        faderBinding = self.fader.getBinding()        
        bindingType = None
        if bindingIsChannel(faderBinding):
            bindingType = CHANNEL
        else:
            bindingType = GROUP
        return bindingType
    
    def getFaderLabelString(self):
        binding = self.fader.getBinding()
        if self.dataType == CHANNEL:
            faderLabelString = 'Chan' + str(binding.number).zfill(2)
        else: # self.dataType == GROUP:
            #todo: also get group label and '\n'
            faderLabelString = 'Group' + str(binding.number).zfill(2) + '\n' + binding.label
        return faderLabelString
            
    def rebuildWidget(self):
        bindingType = self.getBindingType()
        self.patchLabel.config(text=self.getFaderLabelString(),fg=typeColourMapping[bindingType])
    
    def refreshDisplay(self, newFader):    
        if self.fader != newFader:
            self.fader = newFader            
            self.rebuildWidget()
        
