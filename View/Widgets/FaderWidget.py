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

def bindingIsChannel(binding):
    return isinstance(binding, Model.Channel.Channel)

def bindingIsGroup(binding):
    return isinstance(binding, Model.Group.Group)

from Model import Channel

import Model.Channel
import Model.Group

from View.Widgets.GroupWidget import GroupWidget
from View.Widgets.ChannelWidget import ChannelWidget

#contains both a channelWidget and a groupWidget
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
            if bindingIsChannel(binding):
                self.subWidget = ChannelWidget(binding, True, self)
            else:  # self.bindingIsGroup():
                self.subWidget = GroupWidget(binding, True, self)            
            self.subWidget.pack()
        
    def refreshDisplay(self):    
        self.subWidget.refreshDisplay()        

        
