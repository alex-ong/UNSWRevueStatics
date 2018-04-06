from .FaderDescriptionRow import FaderDescriptionRow
import Model.Group as Group
from View.ViewStyle import COLOR_DIRECT, COLOR_GROUP, COLOR_NONE

import View.ViewStyle as VS
FADER_LABEL_FONT = (VS.FONT, VS.font_size(8))
class FaderTitleRow(FaderDescriptionRow):
    
    def getFont(self):
        return FADER_LABEL_FONT
    
    def getLayoutSpacing(self):
        return {' ': ' ' * 9,  # item space
                '|': ' ' * 4,  # group space
                'm': ' ' * 5}  # margin
        
    def getTextAndColour(self, faderBinding):
        text = ''
        color = COLOR_NONE
        if isinstance(faderBinding, Group.Group):
            if not faderBinding.label.startswith('Group'):
                text = faderBinding.label
                color = COLOR_GROUP                                       
        else:  # isinstance(faderRef, Channel.Channel):
            strNumber = str(faderBinding.number)
            if not strNumber == faderBinding.label:                            
                text = faderBinding.label
                color = COLOR_DIRECT
        text = text[:6]
        left = False
        
        #centre string
        while len(text) < 6:
            if left:
                text = ' ' + text
            else:
                text = text + ' ' 
            left = not left
            
        return (text,color)
    