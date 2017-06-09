from Model.ModalForms.ModalFormConsts import TIME_MODAL

def GenerateSelectHandler(menuType, model, modalContainer):
    if menuType == TIME_MODAL:
        return TimeSubMenuSelectHandler(model, modalContainer)
    return None

def GenerateFinishHandler(menuType, model, modalContainer):
    if menuType == TIME_MODAL:
        return TimeSubMenuFinishHandler(model, modalContainer)
    return None

class AbstractMainMenuFinishHandler(object):
    def __init__(self, model, modalContainer):
        self.modalContainer = modalContainer
        self.model = model
        
    def getMenuType(self):
        return None
    
    def closeForm(self, response, data):
        self.closeFormSubclass(response, data)
        self.modalContainer.popStack()
    
    def closeFormSubclass(self, response, data):
        print ("closed", self.getMenuType(), "got", data)
    
class AbstractMainMenuSelectHandler(object):
    def __init__(self, model, modalContainer):
        self.modalContainer = modalContainer
        self.model = model
        
    def getMenuType(self):
        return None
    
    def openForm(self, finishHandler):
        self.modalContainer.addToStack(self.getMenuType())
        self.modalContainer.peekStack().show(self.subClassGetFormData(),
                                             finishHandler)    
    def subClassGetFormData(self):
        return None
    
class TimeSubMenuFinishHandler(AbstractMainMenuFinishHandler):    
    def getMenuType(self):
        return TIME_MODAL
        
class TimeSubMenuSelectHandler(AbstractMainMenuSelectHandler):    
    def getMenuType(self):
        return TIME_MODAL
    
    def subClassGetFormData(self):
        return 'Default Fade'