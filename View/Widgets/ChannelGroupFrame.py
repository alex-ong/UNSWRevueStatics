import tkinter as tk


class ChannelGroupFrame(tk.Frame):
    def __init__(self, values, WidgetType, *args):
        super().__init__(*args)     
        self.configure(bg='black')
        self.widgets = {}
        
        # setup layout. Groups of 6 with gaps between elements,
        # double gaps between groups.
        layout = [('x x x x x x') for i in range(4)]
        layout = "  ".join(layout)
        layout = ' ' + layout + ' '                
        
        itemIndex = 0
        layoutIndex = 0
        
        for i in range (len(layout)):
            self.grid_columnconfigure(i, weight=0,minsize=16)
                                               
        values = list(values.values.values())
        
        while itemIndex < len(values):        
            col = layoutIndex % len(layout)
            row = layoutIndex // len(layout)
            layoutItem = layout[col]
            
            if layoutItem == 'x':
                value = values[itemIndex]
                itemIndex += 1
                cw = WidgetType(value, self)
                cw.grid(row=row, column=col)
                self.widgets[itemIndex] = cw
            layoutIndex += 1
                
    def refreshDisplay(self):
        for widget in self.widgets.values():
            widget.refreshDisplay()
    
        