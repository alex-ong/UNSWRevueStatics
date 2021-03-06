from Model.ModalForms.MainMenuModal import MainMenuModal     
from Model.ModalForms.ModalFormConsts import DMX_MODAL, GROUP_MODAL, FADER_MODAL, CONFIRM_BINDINGS_RESET
           
# menu options. Option Description, Modal to open
patchOptions = [
                   ("DMX Address Binding Menu", DMX_MODAL),
                   ("Group Menu", GROUP_MODAL),
                   ("Fader Menu", FADER_MODAL), 
                   ("Reset DMX, Groups, Faders to defaults", CONFIRM_BINDINGS_RESET)
               ]
                   
# only works up to 9 though.                   
numbers = [str(i + 1) for i in range(len(patchOptions))]                    
class PatchMenuModal(MainMenuModal.MainMenuModal):    
    def getMenuOptions(self):
        return patchOptions
    
    def getNumbers(self):
        return numbers