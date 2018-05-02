from Model.ModalForms.AbstractModal import AbstractModal
from Model.Console import MENU, BACKSPACE, CLEAR, ENTER
from Model.ModalForms.ModalFormConsts import \
                PATCH_MODAL, DELETE_CUES_MODAL,TIME_MODAL, \
                CONFIRM_DESK_RESET, CONFIRM_BACKUP_MODAL, CONFIRM_RESTORE_MODAL 
from Model.ModalForms import SubMenuHandlers
                             
#menu options. Option Description, Modal to open, modal's fixed arguments.
mainMenuOptions = [
                   ("Patch Menu", PATCH_MODAL),
                   ("Clear all Cues", DELETE_CUES_MODAL),
                   ("Default Fade times", TIME_MODAL),
                   ("Reset Desk", CONFIRM_DESK_RESET),
                   ("Backup show locally", CONFIRM_BACKUP_MODAL),
                   ("Restore local backup", CONFIRM_RESTORE_MODAL)
                   ]
                   
# only works up to 9 though.                   
numbers = [str(i + 1) for i in range(len(mainMenuOptions))]                    
class MainMenuModal(AbstractModal):
    def __init__(self, modalContainer, model):
        super().__init__()
        self.currentSelection = None
        self.mainMenuOptions = self.getMenuOptions()
        self.modalMenus = None
        self.modalContainer = modalContainer
        self.model = model
        self.subMenuFinish = []
        self.subMenuSelect = []
        self.setupSubMenuOnSelect()
        self.setupSubMenuOnFinish()
    
    def getMenuOptions(self):
        return mainMenuOptions
    
    def getNumbers(self):
        return numbers
        
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
            self.onFinish(None, None)            
        elif command in self.getNumbers():
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
