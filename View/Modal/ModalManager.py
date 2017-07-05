from Model.ModalContainer import *

from . import TimeModal
from . import MainMenuModal
from . import PatchMenuModal
from . import DMXModal
from . import ConfirmationModal
from . import GroupModal
modalMapping = { TIME_MODAL: TimeModal.TimeModal,
                 MENU_MODAL: MainMenuModal.MainMenuModal,
                 PATCH_MODAL: PatchMenuModal.PatchMenuModal,
                 DMX_MODAL: DMXModal.DMXModal,
                 GROUP_MODAL: GroupModal.GroupModal,
                 CONFIRMATION_MODAL: ConfirmationModal.ConfirmationModal}  # todo!


class ModalManager():
    def __init__(self, modalContainer):
        self.modalForms = {}
        self.modalContainer = modalContainer
        self.myStack = []
        
        for key, value in modalContainer.data.items():
            viewClass = modalMapping[key]
            self.modalForms[key] = viewClass(value)
            
            
    # ensure our stack corresponds to model layer stack.
    def refreshDisplay(self):  # TOOD make this frame-agnostic instead of assuming only one change/frame
        i = 0
        unstack = False
        while i < len(self.modalContainer.stack):
            formType, form = self.modalContainer.stack[i]
            if i >= len(self.myStack):  # add to stack
                self.myStack.append(self.modalForms[formType])
                self.myStack[i].show(form)  
                print ("Showing", formType)
            self.myStack[i].refresh()                      
            i += 1
        
        while i < len(self.myStack):
            self.myStack[i].hide()
            unstack = True
            i += 1
            
        self.myStack = self.myStack[:len(self.modalContainer.stack)]
        
        if unstack and len(self.myStack) > 0: #force bring end of stack to view
            formType, form = self.modalContainer.stack[-1]
            self.myStack[-1].show(form)
            
        
        
