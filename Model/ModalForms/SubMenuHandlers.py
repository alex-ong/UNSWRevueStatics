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
    elif menuType == GROUP_MODAL:
        return GroupModalSelectHandler(model, modalContainer)
    elif menuType == FADER_MODAL:
        return FaderModalSelectHandler(model, modalContainer)
#     elif menuType == TEXT_ENTRY_MODAL:
#         return TextEntryModalSelectHandler(model, modalContainer)
    elif menuType == CONFIRM_BACKUP_MODAL:        
        return ConfirmBackupSelectHandler(model, modalContainer)
    elif menuType == CONFIRM_RESTORE_MODAL:
        return ConfirmRestoreSelectHandler(model, modalContainer)
    elif menuType == CONFIRM_DESK_RESET:
        return ConfirmDeskResetSelectHandler(model, modalContainer)
    elif menuType == CONFIRM_BINDINGS_RESET:
        return ConfirmResetBindingsSelectHandler(model, modalContainer)
    elif menuType is None:
        return None
    else:
        print ("unknown menu type", menuType)
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
    elif menuType == GROUP_MODAL:
        return GroupModalFinishHandler(model, modalContainer)
    elif menuType == FADER_MODAL:
        return FaderModalFinishHandler(model, modalContainer)
#     elif menuType == TEXT_ENTRY_MODAL:
#         return TextEntryModalFinishHandler(model, modalContainer)
    elif menuType == CONFIRM_BACKUP_MODAL:
        return ConfirmBackupFinishHandler(model, modalContainer)
    elif menuType == CONFIRM_RESTORE_MODAL:
        return ConfirmRestoreFinishHandler(model, modalContainer)
    elif menuType == CONFIRM_DESK_RESET:
        return ConfirmDeskResetFinishHandler(model, modalContainer)
    elif menuType == CONFIRM_BINDINGS_RESET:
        return ConfirmResetBindingsFinishHandler(model, modalContainer)
    elif menuType is None:
        return None
    else:
        print ("unknown menu type", menuType)
    return None

############################
# Base Select/Finish Handlers
############################
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
    
############################
# TIME SETTING MODAL
############################
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
    
############################
# PATCH MENU
############################
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
############################
# DMX Patch
############################
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

############################
# CLEAR CUE
############################
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
    

############################
# Group modal
############################
class GroupModalFinishHandler(AbstractMainMenuFinishHandler):    
    def getMenuType(self):
        return GROUP_MODAL
    
    def closeForm(self, response, data):
        self.closeFormSubclass(response, data)
        self.modalContainer.popStack()    
            
 
class GroupModalSelectHandler(AbstractMainMenuSelectHandler):
    def getMenuType(self):
        return GROUP_MODAL
    
    def writeReadBindings(self, bindings):
        self.model.config.writeGroupBindings(bindings)
        self.model.refreshGroupBindings()
        
    def subClassGetFormData(self):        
        return (self.model.groupBindings, self.writeReadBindings)  
    
############################
# Fader Modal
############################
class FaderModalFinishHandler(AbstractMainMenuFinishHandler):    
    def getMenuType(self):
        return FADER_MODAL
    
    def closeForm(self, response, data):
        self.closeFormSubclass(response, data)
        self.modalContainer.popStack()    
            
 
class FaderModalSelectHandler(AbstractMainMenuSelectHandler):
    def getMenuType(self):
        return FADER_MODAL
    
    def writeReadBindings(self, bindings):
        self.model.config.writeFaderBindings(bindings)
        self.model.refreshFaderBindings()
        
    def subClassGetFormData(self):        
        return (self.model.faderBindings, self.writeReadBindings)

############################
# Text entry
############################
class TextEntryFinishHandler(AbstractMainMenuFinishHandler):    
    def getMenuType(self):
        return TEXT_ENTRY_MODAL
    
    def closeForm(self, response, data):
        self.closeFormSubclass(response, data)
        self.modalContainer.popStack()    
        if response and data:
            self.model.resetBindings()
 
class TextEntrySelectHandler(AbstractMainMenuSelectHandler):
    def getMenuType(self):
        return TEXT_ENTRY_MODAL
        
    def subClassGetFormData(self):        
        return ('Reset all bindings to default?')



############################
# Confirm backup
############################
class ConfirmBackupFinishHandler(AbstractMainMenuFinishHandler):    
    def getMenuType(self):
        return CONFIRMATION_MODAL
    
    def closeForm(self, response, data):
        self.closeFormSubclass(response, data)
        self.modalContainer.popStack()        
        if response and data:
            self.model.backupShow()
 
class ConfirmBackupSelectHandler(AbstractMainMenuSelectHandler):
    def getMenuType(self):
        return CONFIRMATION_MODAL
        
    def subClassGetFormData(self):        
        return ('Confirm backup of all Data?')

############################
# Confirm restore
############################
class ConfirmRestoreFinishHandler(AbstractMainMenuFinishHandler):    
    def getMenuType(self):
        return CONFIRMATION_MODAL
    
    def closeForm(self, response, data):
        self.closeFormSubclass(response, data)
        self.modalContainer.popStack()        
        if response and data:
            self.model.restoreShow()
 
class ConfirmRestoreSelectHandler(AbstractMainMenuSelectHandler):
    def getMenuType(self):
        return CONFIRMATION_MODAL
        
    def subClassGetFormData(self):        
        return ('Confirm RESTORE of all Data?\n YOU WILL LOSE CURRENT DATA')


############################
# Confirm desk reset
############################
class ConfirmDeskResetFinishHandler(AbstractMainMenuFinishHandler):    
    def getMenuType(self):
        return CONFIRMATION_MODAL
    
    def closeForm(self, response, data):
        self.closeFormSubclass(response, data)
        self.modalContainer.popStack()    
        if response and data:
            self.model.totalReset()
 
class ConfirmDeskResetSelectHandler(AbstractMainMenuSelectHandler):
    def getMenuType(self):
        return CONFIRMATION_MODAL
        
    def subClassGetFormData(self):        
        return ('Delete ALL CUES AND BINDINGS?')
    
############################
# Confirm desk reset
############################
class ConfirmResetBindingsFinishHandler(AbstractMainMenuFinishHandler):    
    def getMenuType(self):
        return CONFIRMATION_MODAL
    
    def closeForm(self, response, data):
        self.closeFormSubclass(response, data)
        self.modalContainer.popStack()    
        if response and data:
            self.model.resetBindings()
 
class ConfirmResetBindingsSelectHandler(AbstractMainMenuSelectHandler):
    def getMenuType(self):
        return CONFIRMATION_MODAL
        
    def subClassGetFormData(self):        
        return ('Reset all bindings to default?')
