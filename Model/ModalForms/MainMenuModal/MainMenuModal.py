from Model.ModalForms.AbstractModal import AbstractModal
from Model.Console import MENU, BACKSPACE, CLEAR, ENTER
from Model.ModalForms.ModalFormConsts import *

#menu options. Option Description, Modal to open, modal's fixed arguments.
mainMenuOptions = [
                   ("Patch Menu", None),
                   ("Clear all Cues", None),
                   ("Default Fade times", TIME_MODAL, "Default Fade"),
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
        
    def setModel(self, model):
        self.model = model
        self.setupSubMenuOnFinish()
        
    def setupSubMenuOnFinish(self):
        for mainMenuOption in self.mainMenuOptions:
            modalType = mainMenuOption[1]  
            if modalType == TIME_MODAL:
                #todo: what do we do with the callback?
                self.subMenuFinish.append(None)
            elif modalType is None:
                self.subMenuFinish.append(None)
            
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
                option = self.mainMenuOptions[self.currentSelection]
                modalToOpen = option[1]
                if modalToOpen is not None:
                    self.modalContainer.addToStack(modalToOpen)
                    desc = option[2]
                    self.modalContainer.peekStack().show(desc, 
                                                         self.subMenuFinish[self.currentSelection])
                                     
                self.currentSelection = None
        else:
            print("MainMenuModal got command", command)

class AbstractMainMenuFinishHandler(object):
    def __init__(self):
        pass

class AbstractMainMenuSelectHandler(object):
    def __init__(self):
        pass