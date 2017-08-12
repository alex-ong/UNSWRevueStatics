'''
@author: alex-ong
@date 2017-05-07
k'''
import tkinter as tk
from View.Widgets.ChannelGroupWidget import ChannelGroupWidget
from Model import Channel

#holds a ChannelGroupWidget
class FaderWidget(tk.Frame):
    def __init__(self, fader, *args):
        super().__init__(*args)
        self.subWidget = None
        self.changeFader(fader)
    
    def changeFader(self, fader):
        if self.subWidget is not None:
            self.subWidget.pack_forget()
        if fader is not None:
            binding = fader.getBinding()    
            self.subWidget = ChannelGroupWidget(binding, True, self)                    
            self.subWidget.pack()
        
    def refreshDisplay(self):    
        self.subWidget.refreshDisplay()        

        
