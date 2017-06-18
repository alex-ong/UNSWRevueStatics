from .ModalForms.TimeModal import TimeModal
from .ModalForms.MainMenuModal import MainMenuModal
from .ModalForms.PatchModal import PatchModal
from .ModalForms.DMXModal import DMXModal
from .ModalForms.ModalFormConsts import *
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
        self.data[PATCH_MODAL] = PatchModal.PatchModal(self, model)
        self.data[DMX_MODAL] = DMXModal.DMXModal()
        
    def getModal(self, modalType):
        return self.data[modalType]

    def addToStack(self, modalType):
        self.stack.append([modalType, self.getModal(modalType)])
    
    def popStack(self):
        self.stack.pop()
    
    def peekStack(self):
        if len(self.stack) > 0:
            return self.stack[-1][1]
        else:
            return None
    
    def isEmpty(self):
        return len(self.stack) == 0
    
    def handleInput(self, input):
        self.peekStack().handleCommand(input)
        
    
