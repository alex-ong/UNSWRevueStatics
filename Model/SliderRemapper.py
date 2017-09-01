_instance = None
def instance():
    global _instance
    if _instance is None:
        _instance = SliderRemapper()
    return _instance

class SliderRemapper(object):
    def __init__(self):
        pass
    
    #hack!
    def remapIndex(self, index):
        if index >= 19:
            return index - 18
        elif index >= 1:
            return index + 9
        else:
            return index
            
    def getSliderName(self, originalSliderName):         
        if 'b_slider' in originalSliderName:
            index = int(originalSliderName.replace('b_slider',''))
            newIndex = self.remapIndex(index)
            newSliderName ='b_slider'+str(newIndex)            
            return newSliderName 
        elif 'slider' in originalSliderName:
            index = int(originalSliderName.replace('slider',''))
            newIndex = self.remapIndex(index)
            newSliderName ='slider'+str(newIndex)           
            return newSliderName    
                
        return originalSliderName