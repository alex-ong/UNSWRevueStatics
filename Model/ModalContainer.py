from .ModalForms.TimeModal import TimeModal
from .ModalForms.MainMenuModal import MainMenuModal
from Model.ModalForms.PatchMenuModal import PatchMenuModal
from .ModalForms.DMXModal import DMXModal
from .ModalForms.ConfirmationModal import ConfirmationModal
from .ModalForms.GroupModal import GroupModal
from .ModalForms.FaderModal import FaderModal
from .ModalForms.TextEntryModal import TextEntryModal
from .ModalForms.ModalFormConsts import *
from Model import OptionButtons


'''
This class has an instance of every possible modal.
it also has a stack for you to add and interact with modal forms. 
Some modals can be stacked (e.g. menu modal, then time modal)
'''

class ModalList(object):
    def __init__(self, model):
        self.data = {}
        self.stack = []
        self.setupModals(model)
        
    def setupModals(self, model):
        self.data[TIME_MODAL] = TimeModal.TimeModal()
        self.data[MENU_MODAL] = MainMenuModal.MainMenuModal(self, model)
        self.data[PATCH_MODAL] = PatchMenuModal.PatchMenuModal(self, model)
        self.data[DMX_MODAL] = DMXModal.DMXModal()
        self.data[GROUP_MODAL] = GroupModal.GroupModal(model)
        self.data[FADER_MODAL] = FaderModal.FaderModal(model)
        self.data[CONFIRMATION_MODAL] = ConfirmationModal.ConfirmationModal()
        self.data[TEXT_ENTRY_MODAL] = TextEntryModal.TextEntryModal()
        
    def getModal(self, modalType):
        return self.data[modalType]

    def addToStack(self, modalType):
        self.stack.append([modalType, self.getModal(modalType)])
    
    def popStack(self):
        self.stack.pop()
        #hack since mainscene isn't a modal.. yet...
        if len(self.stack) == 0:
            OptionButtons.getInstance().setState(OptionButtons.MAIN_STATE)
            
    def peekStack(self):
        if len(self.stack) > 0:
            return self.stack[-1][1]
        else:
            return None
    
    def isEmpty(self):
        return len(self.stack) == 0
    
    def handleInput(self, input, buttonPressed):
        #Hack - our modals only care about onButtonDown
        if (buttonPressed):        
            self.peekStack().handleCommand(input)
    
    def handleRawButtonInput(self, rawButtonName, buttonPressed):
        #Hack - our modals only care about onButtonDown
        if (buttonPressed):            
            self.peekStack().handleRawButton(rawButtonName)
                    
    def handleSliderInput(self, input, value):
        #hack - we don't accept slider input in modals
        return
    
    