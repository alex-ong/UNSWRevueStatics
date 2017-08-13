'''
@author: alex-ong
@date 2017-05-07
k'''
import tkinter as tk
from View.Widgets.ChannelGroupWidget import ChannelGroupWidget
from Model import Channel

#holds a ChannelGroupWidget
class FaderWidget(tk.Frame):
    def __init__(self, fader, faderNum, *args):
        super().__init__(*args)
        self.subWidget = None
        binding = self.getBinding(fader)    
        self.subWidget = ChannelGroupWidget(binding, faderNum, True, self)                    
        self.subWidget.pack()
        
    def getBinding(self, fader):
        binding = None
        if fader is not None:
            binding = fader.getBinding()
        return binding
    
    def changeFader(self, fader):                
        self.subWidget.changeFader(self.getBinding(fader))

    def refreshDisplay(self):    
        self.subWidget.refreshDisplay()        

        
