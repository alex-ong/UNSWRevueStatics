import tkinter as tk

def ChannelLayout():
    layout = [('x x x x x x') for _ in range(4)]
    layout = "  ".join(layout)
    layout = ' ' + layout + ' '
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
            rowLabel.grid(sticky=tk.NSEW)
            rowFinalValue = ChannelFinalValueRow.ChannelFinalValueRow(chunk, layout, self)
            rowFinalValue.grid(sticky=tk.NSEW)
            self.widgets.append(rowFinalValue)
        '''
        maxRow = 0
        while itemIndex < len(values):        
            col = layoutIndex % len(layout)
            row = layoutIndex // len(layout)
            maxRow = row
            layoutItem = layout[col]
            
            if layoutItem == 'x':
                value = values[itemIndex]
                itemIndex += 1
                cw = ChannelGroupWidget(value, itemIndex, False, self)
                cw.grid(row=row + 1, column=col, sticky=tk.NSEW)
                self.widgets.append(cw)
            layoutIndex += 1
        for i in range(maxRow):
            self.rowconfigure(i, weight=1)
        '''    
    
    def refreshDisplay(self):
        for widget in self.widgets:
            widget.refreshDisplay()
    
        