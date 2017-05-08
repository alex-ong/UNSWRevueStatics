import tkinter as tk
import View.Widgets.ChannelWidget as ChannelWidget

class ChannelFrame(tk.Frame):
    def __init__(self, channelValues, *args):
        super().__init__(*args)     
        self.configure(bg='black')
        self.channelWidgets = {}
        
        # setup layout. Groups of 6 with gaps between elements,
        # double gaps between groups.
        layout = [('x x x x x x') for i in range(4)]
        layout = "  ".join(layout)
        layout = ' ' + layout + ' '                
        
        channelIndex = 0
        layoutIndex = 0
        
        for i in range (len(layout)):
            self.grid_columnconfigure(i, weight=0,minsize=16)
            
        while channelIndex < len(channelValues):
            
            col = layoutIndex % len(layout)
            row = layoutIndex // len(layout)
            layoutItem = layout[col]
            
            if layoutItem == 'x':
                channel = channelValues[channelIndex]
                channelIndex += 1
                cw = ChannelWidget.ChannelWidget(channel, self)
                cw.grid(row=row, column=col)
                self.channelWidgets[channelIndex] = cw
            layoutIndex += 1
                
    def handleInput(self, dictInput):
        for key in self.channelWidgets:            
            if 'slider' + str(key) in dictInput:
                self.channelWidgets[key].updateValues(dictInput['slider'+str(key)],0,0,None)
        