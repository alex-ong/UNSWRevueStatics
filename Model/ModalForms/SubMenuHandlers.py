from Model.ModalForms.ModalFormConsts import *

def GenerateSelectHandler(menuType, model, modalContainer):
    if menuType == TIME_MODAL:
        return TimeSubMenuSelectHandler(model, modalContainer)
    elif menuType == PATCH_MODAL:
        return PatchSubMenuSelectHandler(model, modalContainer)
    elif menuType == DMX_MODAL:
        return DmxSubMenuSelectHandler(model, modalContainer)
    elif menuType == DELETE_CUES_MODAL:
        return ClearCueSelectHandler(model, modalContainer)
    return None

def GenerateFinishHandler(menuType, model, modalContainer):
    if menuType == TIME_MODAL:
        return TimeSubMenuFinishHandler(model, modalContainer)
    elif menuType == PATCH_MODAL:
        return PatchSubMenuFinishHandler(model, modalContainer)
    elif menuType == DMX_MODAL:
        return DmxSubMenuFinishHandler(model, modalContainer)
    elif menuType == DELETE_CUES_MODAL:
        return ClearCueFinishHandler(model, modalContainer)
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
    
    def closeFormSubclass(self, response, data):
        if data is not None:
            upTime = data[0]
            downTime = data[1]
            self.model.updateFadeTimes(upTime, downTime)
            
        
class TimeSubMenuSelectHandler(AbstractMainMenuSelectHandler):    
    def getMenuType(self):
        return TIME_MODAL
    
    def subClassGetFormData(self):
        return 'Default Fade'
    
class PatchSubMenuSelectHandler(AbstractMainMenuSelectHandler):
    def getMenuType(self):
        return PATCH_MODAL
    
    def subClassGetFormData(self):
        print ("patchsubmenu select handler summoned!")
        # hard link to patch dictionary, reference to saveFile func.
        return None 
    
class PatchSubMenuFinishHandler(AbstractMainMenuFinishHandler):
    def getMenuType(self):
        return PATCH_MODAL
    
    def closeFormSubclss(self, response, data):
        pass  # we ignore this since we do all the model updates inside

class DmxSubMenuSelectHandler(AbstractMainMenuSelectHandler):
    def getMenuType(self):
        return DMX_MODAL
    
    def subClassGetFormData(self):        
        return (self.model.patching, self.model.config.writeDMXBindings) 
    
class DmxSubMenuFinishHandler(AbstractMainMenuFinishHandler):
    def getMenuType(self):
        return DMX_MODAL
    
    def closeFormSubclass(self, response, data):
        pass  # we ignore this since we do all the model updates inside

class ClearCueFinishHandler(AbstractMainMenuFinishHandler):    
    def getMenuType(self):
        return CONFIRMATION_MODAL
    
    def closeForm(self, response, data):
        self.closeFormSubclass(response, data)
        self.modalContainer.popStack()
    
    def closeFormSubclass(self, response, data):
        if (response): #confirm delete all
            self.model.deleteAllCues()
            
class ClearCueSelectHandler(AbstractMainMenuSelectHandler):
    def getMenuType(self):
        return CONFIRMATION_MODAL
    
    def openForm(self, finishHandler):
        self.modalContainer.addToStack(self.getMenuType())
        self.modalContainer.peekStack().show(self.subClassGetFormData(),
                                             finishHandler)    
    def subClassGetFormData(self):
        return "Do you really want to delete all cues?" 
    

