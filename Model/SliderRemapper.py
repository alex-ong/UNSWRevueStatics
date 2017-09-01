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
        return index
            
    def getSliderName(self, originalSliderName):
        try: 
            if 'b_slider' in originalSliderName:
                index = int(originalSliderName.replace('b_slider',''))
                newIndex = self.remapIndex(index)
                return 'b_slider'+str(newIndex)
            elif 'slider' in originalSliderName:
                index = int(originalSliderName.replace('slider',''))
                newIndex = self.remapIndex(index)
                return 'slider'+str(newIndex) 
        except:
            return originalSliderName
                
        return originalSliderName