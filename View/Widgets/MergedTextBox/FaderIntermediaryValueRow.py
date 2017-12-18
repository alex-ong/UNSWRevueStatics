from .IntermediaryChannelValueRow import IntermediaryChannelValueRow
from Model.Group import Group
class FaderIntermediaryValueRow(IntermediaryChannelValueRow):
    def getLayoutSpacing(self):
        return {' ': ' ' * 9,
                '|' : ' ' * 9,
                'm' : ' ' * 4}      
    def getValues(self, fader):
        underlyingItem = fader.getBinding()
        if isinstance(underlyingItem, Group):
            return (underlyingItem.getDirectValue(),
                    0,
                    underlyingItem.playbackValue)
        else: #isinstance(underlyingItem, Channel):
            return (underlyingItem.getDirectValue(),
                    underlyingItem.getGroupValue(),
                    underlyingItem.playbackValue)
    
    def rebuild(self, faders):
        self.channels = faders