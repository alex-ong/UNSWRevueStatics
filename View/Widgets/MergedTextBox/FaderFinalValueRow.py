from . import ChannelFinalValueRow
class FaderFinalValueRow(ChannelFinalValueRow.ChannelFinalValueRow):
    # override in FaderFinalValueRow
    def layoutSpacing(self):
        return {' ': ' ' * 4,  # space
                '|': ' ' * 4,  # group gap
                'm': ' ' * 2}  # margin
    
    def getValueAndReason(self, item):
        if item is None:
            return 0, None
        else:
            return item.getBinding().getDisplayValueAndReason()
    
    def rebuild(self, faders):
        # make sure that the new item array is same length
        # as existing item array
        totalItems = len(self.indices)        
        faders = faders[:]        
        while len(faders) < totalItems:
            faders.append(None)
            
        self.items = faders
    
