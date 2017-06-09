from Model.ModalForms.AbstractModal import AbstractModal
from Model.Console import MENU, BACKSPACE, CLEAR, ENTER
from Model.ModalForms.ModalFormConsts import *
from . import SubMenuHandlers
                             
#menu options. Option Description, Modal to open, modal's fixed arguments.
mainMenuOptions = [
                   ("Patch Menu", None),
                   ("Clear all Cues", None),
                   ("Default Fade times", TIME_MODAL),
                   ("Backup show", None)
                   ]
                   
# only works up to 9 though.                   
numbers = [str(i + 1) for i in range(len(mainMenuOptions))]                    
class MainMenuModal(AbstractModal):
    def __init__(self, modalContainer):
        super().__init__()
        self.currentSelection = None
        self.mainMenuOptions = mainMenuOptions
        self.modalMenus = None
        self.modalContainer = modalContainer
        self.model = None
        self.subMenuFinish = []
        self.subMenuSelect = []
        
    def setModel(self, model):
        self.model = model
        self.setupSubMenuOnSelect()
        self.setupSubMenuOnFinish()
        
    def setupSubMenuOnSelect(self):
        for mainMenuOption in self.mainMenuOptions:
            modalType = mainMenuOption[1]
            handler = SubMenuHandlers.GenerateSelectHandler(modalType, 
                                                            self.model,
                                                            self.modalContainer)
            self.subMenuSelect.append(handler)
            
    def setupSubMenuOnFinish(self):
        for mainMenuOption in self.mainMenuOptions:
            modalType = mainMenuOption[1]
            handler = SubMenuHandlers.GenerateFinishHandler(modalType, 
                                                            self.model, 
                                                            self.modalContainer)
            self.subMenuFinish.append(handler)
            
    def show(self, onShowArguments, onFinish):        
        super().show(onShowArguments, onFinish)                
        
    def reset(self):
        self.currentSelection = None
    
    def handleCommand(self, command):
        if command == MENU:
            self.onFinish()            
        elif command in numbers:
            self.currentSelection = int(command) - 1
        elif command in [BACKSPACE, CLEAR]:
            self.currentSelection = None
        elif command == ENTER:
            if self.currentSelection is not None:                
                selectHandler = self.subMenuSelect[self.currentSelection]
                finishHandler = self.subMenuFinish[self.currentSelection]
                if selectHandler is not None:
                    selectHandler.openForm(finishHandler.closeForm)                                     
                self.currentSelection = None
        else:
            print("MainMenuModal got command", command)
