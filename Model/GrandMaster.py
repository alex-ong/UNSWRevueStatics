SLIDER_NUMBER = -1
class GrandMaster(object):
    def __init__(self):
        self.perc = 1.0
        self.DBO = False
        self.flash = False
    
    def setPerc(self, perc):
        self.perc = perc
    
    def setFlash(self, flash):
        self.flash = flash
        
    def toggleDBO(self):
        self.DBO = not self.DBO
        
    def getValue(self):
        if self.DBO:
            return 0.0
        else:
            return self.getSliderPerc()
    
    def getSliderPerc(self):
        if self.flash:
            return 100
        else:
            return self.perc
    
    def getDBO(self):
        return self.DBO 
        