# Fader frame using merged text boxes.
# @author alex-ong
# @date 2017-12-13
 
import tkinter as tk

from .FaderNumberRow import FaderNumberRow
from .FaderFinalValueRow import FaderFinalValueRow
from .FaderDescriptionRow import FaderDescriptionRow
from .FaderTitleRow import FaderTitleRow
import View.ViewStyle as VS
from View.Widgets.MergedTextBox.FaderIntermediaryValueRow import FaderIntermediaryValueRow


HEADING_FONT = (VS.FONT, VS.font_size(16), 'bold')


def getLayout(faderLayout):
    layout = []    
    for rowLength in faderLayout:
        rowLayout = ' '.join('x' * rowLength)            
        layout.append('m' + rowLayout + 'm')
    return layout

class FaderFrameMTB(tk.Frame):
    def __init__(self, getFaderFunc, numFaders, faderLayout, *args):
        super().__init__(*args)
        self.columnconfigure(0, weight=1)     
        self.configure(bg='black')
        self.widgets = {}
        self.getFaderFunc = getFaderFunc
        self.numFaders = numFaders
        
        self.layout = getLayout(faderLayout)
                                    
        
        
        # title bar
        title = tk.Label(self, text='Faders', bg='grey', font=HEADING_FONT)        
        title.grid(sticky=tk.NSEW)        
        
        faderValues = list(getFaderFunc().values.values())    
        # fader numbers
        faderIndex = 0
        for (rowNumber, rowLayout) in enumerate(self.layout):   
            rowSize = rowLayout.count('x')
            rowFaderValues = faderValues[faderIndex:faderIndex + rowSize]
            

            faderTitle = FaderTitleRow(rowFaderValues, rowLayout, self)
            faderTitle.grid(sticky=tk.W)
            self.widgets[str(rowNumber) + '_faderTitleRow'] = faderTitle
            
            faderDesc = FaderDescriptionRow(rowFaderValues, rowLayout, self)
            faderDesc.grid(sticky=tk.W)
            self.widgets[str(rowNumber) + '_faderDescRow'] = faderDesc
                        
            faderNumbers = FaderNumberRow(rowFaderValues, rowLayout, self)            
            faderNumbers.grid(sticky=tk.W)
            
            faderFinalValueRow = FaderFinalValueRow(rowFaderValues, rowLayout, self)
            faderFinalValueRow.grid(sticky=tk.W)            
            self.widgets[str(rowNumber) + '_faderFinalValueRow'] = faderFinalValueRow
            
            intermediary = FaderIntermediaryValueRow(rowFaderValues, rowLayout, self)
            intermediary.grid(sticky=tk.W)
            self.widgets[str(rowNumber) + '_intermediaryRow'] = intermediary
            faderIndex += rowSize

        self.lastFaderValues = self.getFaderFunc()
    
    # done everytime use presses next/prev fader
    def rebuild(self, faderValues):
        faderIndex = 0
        for (rowNumber, rowLayout) in enumerate(self.layout):   
            rowSize = rowLayout.count('x')            
            faderRowValues = faderValues[faderIndex:faderIndex + rowSize]
            faderDesc = self.widgets[str(rowNumber) + '_faderDescRow']
            faderDesc.rebuild(faderRowValues)
            faderTitle = self.widgets[str(rowNumber) + '_faderTitleRow']
            faderTitle.rebuild(faderRowValues)
            faderFinalValueRow = self.widgets[str(rowNumber) + '_faderFinalValueRow']
            faderFinalValueRow.rebuild(faderRowValues)
            intermediary = self.widgets[str(rowNumber) + '_intermediaryRow']
            intermediary.rebuild(faderRowValues)            
            faderIndex += rowSize
    
    def refreshDisplay(self):    
        # check for if user changed page    
        if self.lastFaderValues != self.getFaderFunc():            
            self.lastFaderValues = self.getFaderFunc()
            faderValues = list(self.getFaderFunc().values.values())    
            self.rebuild(faderValues)
            
        for widget in self.widgets.values():
            widget.refreshDisplay()
    
        
