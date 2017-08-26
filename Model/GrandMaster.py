SLIDER_NUMBER = -1
class GrandMaster(object):
    def __init__(self):
        self.perc = 1.0
        self.DBO = False
    
    def setPerc(self, perc):
        self.perc = perc
    
    def toggleDBO(self):
        self.DBO = not self.DBO
        
    def getValue(self):
        if self.DBO:
            return 0.0
        else:
            return self.perc
    
    def getRawPerc(self):
        return self.perc
    
    def getDBO(self):
        return self.DBO 
        