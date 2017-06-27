'''
abstract class which just has enter for proceed and escape/clear to cancel.
'''
from Model.Console import CLEAR, MENU, ENTER
from Model.ModalForms.AbstractModal import AbstractModal

class ConfirmationModal(AbstractModal):
    def subclassShow(self):
        self.message = self.onShowArguments
    
    def handleCommand(self, command):
        if command == ENTER:
            self.onFinish(True, True)
        elif command == MENU:
            self.onFinish(False, False)
        elif command == CLEAR:
            self.onFinish(False, False)
    '''
    not required
    '''     
    def reset(self):
        pass
