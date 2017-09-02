'''
abstract class which just has enter for proceed and escape/clear to cancel.
'''
from Model.Console import ENTER
from Model.ModalForms.AbstractModal import AbstractModal

class TextEntryModal(AbstractModal):
    def subclassShow(self):
        self.message = self.onShowArguments
        self.entryText = ''
        
    def handleCommand(self, command):
        if command == ENTER:
            self.onFinish(True, self.entryText)        
        else:
            pass
        
    def rawToNice(self, rawButton):
        print (rawButton)
        return ''
    
    def handleRawButton(self, rawButton):
        self.entryText += rawButton

    def reset(self):
        self.entryText = ''
