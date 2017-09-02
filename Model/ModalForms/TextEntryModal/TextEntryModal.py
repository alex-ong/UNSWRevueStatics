'''
abstract class which just has enter for proceed and escape/clear to cancel.
'''
from Model.Console import ENTER, BACKSPACE
from Model.ModalForms.AbstractModal import AbstractModal
import string
from Model.OptionButtons import TEXT_ENTRY_STATE,EXIT2
MAX_LENGTH = 8

validchars = (string.ascii_uppercase + string.ascii_lowercase +
              string.digits)
class TextEntryModal(AbstractModal):
    def subclassShow(self):
        self.message = self.onShowArguments
        self.entryText = ''
        
    def optionButtonBindings(self):
        return TEXT_ENTRY_STATE
    
    def handleCommand(self, command):
        if command == ENTER:
            self.onFinish(True, self.entryText)
        elif command == BACKSPACE:
            self.entryText = self.entryText[:-1]                
        elif command == EXIT2:
            self.onFinish(False, None)
            
    def rawToNice(self, rawButton):
        text = rawButton.replace('raw_','')
        if text in validchars:
            return text
        return ''
    
    def handleRawButton(self, rawButton):        
        text = self.rawToNice(rawButton)
        self.entryText += text
        self.entryText = self.entryText[:MAX_LENGTH]
        
    def reset(self):
        self.entryText = ''
