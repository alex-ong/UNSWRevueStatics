'''
@author: alex-ong
@date 2017-05-07
k'''
import tkinter as tk

def autoString(value):        
    if value is None:
        return ''
    elif value == 100:
        return ('FL')
    else:
        return str(value).zfill(2)

from Model import Channel


import Model.Channel
import Model.Group

from View.Widgets.GroupWidget import GroupWidget
from View.Widgets.ChannelWidget import ChannelWidget

class FaderWidget(tk.Frame):
    def __init__(self, fader, *args):
        super().__init__(*args)
        self.fader = fader
        self.binding = self.fader.getBinding()
        
        if self.bindingIsChannel():
            self.subWidget = ChannelWidget(self.binding, True, self)
        else:  # self.bindingIsGroup():
            self.subWidget = GroupWidget(self.binding, True, self)            
        self.subWidget.pack()
        
    def bindingIsChannel(self):
        return isinstance(self.binding, Model.Channel.Channel)
    
    def bindingIsGroup(self):
        return isinstance(self.binding, Model.Group.Group)
    
    def refreshDisplay(self):    
        self.subWidget.refreshDisplay()        

        
