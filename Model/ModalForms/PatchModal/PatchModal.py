from Model.ModalForms.MainMenuModal import MainMenuModal     
from Model.ModalForms.ModalFormConsts import DMX_MODAL                        
# menu options. Option Description, Modal to open
patchOptions = [
                   ("DMX Address Binding Menu", DMX_MODAL),
                   ("Group Menu", None),
                   ("Fader Menu", None),
                   ("Reset DMX, Groups, Faders to defaults", None)
               ]
                   
# only works up to 9 though.                   
numbers = [str(i + 1) for i in range(len(patchOptions))]                    
class PatchModal(MainMenuModal.MainMenuModal):    
    def getMenuOptions(self):
        return patchOptions
    
    def getNumbers(self):
        return numbers