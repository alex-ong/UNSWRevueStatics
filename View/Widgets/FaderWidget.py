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

COLOR_DIRECT = 'yellow'
COLOR_PLAYBACK = 'green'
COLOR_GROUP = 'cyan'
COLOR_RECORD = 'red'
COLOR_NONE = 'black'

typeColourMapping = { Channel.ValueType.DIRECT : COLOR_DIRECT,
                     Channel.ValueType.PLAYBACK : COLOR_PLAYBACK,
                     Channel.ValueType.GROUP : COLOR_GROUP,
                     Channel.ValueType.RECORD : COLOR_RECORD,
                     Channel.ValueType.NONE: COLOR_NONE}
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
            self.subWidget = ChannelWidget(self.binding,self)
        else: #self.bindingIsGroup():
            self.subWidget = GroupWidget(self.binding,self)            
        self.subWidget.pack()
        
    def bindingIsChannel(self):
        return isinstance(self.binding, Model.Channel.Channel)
    
    def bindingIsGroup(self):
        return isinstance(self.binding, Model.Group.Group)
    
    def refreshDisplay(self):    
        self.subWidget.refreshDisplay()        

        
