from . import ChannelFinalValueRow
class FaderFinalValueRow(ChannelFinalValueRow.ChannelFinalValueRow):
    #override in FaderFinalValueRow
    def layoutSpacing(self):
        return {' ': ' '*4, # space
                '|': ' '*4, # group gap
                'm': ' '} # margin
    def getValueAndReason(self, item):
        return item.getBinding().getDisplayValueAndReason()
    
    def rebuild(self, faders):
        self.items = faders
    