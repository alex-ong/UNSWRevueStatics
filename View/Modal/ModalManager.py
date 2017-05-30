from Model.ModalContainer import TIME_MODAL

from . import TimeModal
modalMapping = { TIME_MODAL: TimeModal.TimeModal }


class ModalManager():
    def __init__(self, modalContainer):
        self.modalForms = {}
        self.modalContainer = modalContainer
        self.myStack = []
        
        for key, value in modalContainer.data.items():
            viewClass = modalMapping[key]
            self.modalForms[key] = viewClass(value)
            
            
    #ensure our stack corresponds to model layer stack.
    def refreshDisplay(self): #TOOD make this frame-agnostic instead of assuming only one change/frame
        i = 0
        while i < len(self.modalContainer.stack):
            formType, form = self.modalContainer.stack[i]
            if i >= len(self.myStack): #add to stack
                self.myStack.append(self.modalForms[formType])
                self.myStack[i].show(form)  
            self.myStack[i].refresh()                      
            i += 1
        
        while i < len(self.myStack):
            self.myStack[i].hide()
            i += 1
            
        self.myStack = self.myStack[:len(self.modalContainer.stack)]