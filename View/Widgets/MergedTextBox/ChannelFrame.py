import tkinter as tk
from View.Widgets.MergedTextBox.IntermediaryChannelValueRow import IntermediaryChannelValueRow
from View import ViewStyle

def ChannelLayout():
    layout = [('x  x  x  x  x  x') for _ in range(4)]
    layout = "|".join(layout) #add group splits
    layout = 'm' + layout + 'm' #add margins
    count = layout.count('x')
    return (layout, count)


from View.Widgets.ChannelGroupWidget import ChannelGroupWidget
from . import ChannelLabelRow
from . import ChannelFinalValueRow
from View.ViewStyle import CHANNEL, GROUP
import View.ViewStyle as VS

def chunks(l, n):
    """Yield successive n-sized chunks from l."""
    for i in range(0, len(l), n):
        yield l[i:i + n]
        
'''
ChannelGroupFrame with MergedTextBox implementation for performance
'''
class ChannelFrameMTB(tk.Frame):
    def __init__(self, channels, layoutType, *args):
        super().__init__(*args)     
        self.configure(bg='black')
        self.widgets = []
        self.columnconfigure(0,weight=1)
        
        # setup layout. Groups of 6 with gaps between elements,
        # double gaps between groups.        
        layout, layoutLen = ChannelLayout() 
                                       
        values = list(channels.values.values())
        
        # title bar
        title = tk.Label(self, text='Channels', bg='grey',
                         font=(VS.FONT, VS.font_size(16), 'bold'))
        title.grid(row=0, sticky=tk.NSEW)
        
        for chunk in chunks(values, layoutLen):            
            rowLabel = ChannelLabelRow.ChannelLabelRow(chunk, layout, self)
            rowLabel.grid(sticky=tk.NS)
            rowFinalValue = ChannelFinalValueRow.ChannelFinalValueRow(chunk, layout, self)
            rowFinalValue.grid(sticky=tk.NS)
            
            self.widgets.append(rowFinalValue)
            
            # we only show intermediary values if resolution is high enough
            if ViewStyle.screen_x() >= 1366:
                rowSubValue = IntermediaryChannelValueRow(chunk, layout, self)
                rowSubValue.grid(sticky=tk.NS)
                self.widgets.append(rowSubValue)

    
    def refreshDisplay(self):
        for widget in self.widgets:
            widget.refreshDisplay()
    
        
