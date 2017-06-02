from Model.ModalForms.AbstractModal import AbstractModal

mainMenuOptions = [
                   ("Patch Menu", None),
                   ("Clear all Cues", None),
                   ("Default Fade times", None),
                   ("Backup show", None)
                   ]
                   
class MainMenuModal(AbstractModal):
    def __init__(self):
        super().__init__()
        self.currentSelection = None
        
    def show(self, onShowArguments, onFinish):
        super().show(onShowArguments,onFinish)
        self.defaultFadeTimes = onShowArguments
        print("woot, showing mainMenuModal")
    def reset(self):
        pass
    
    def handleCommand(self, command):
        print("MainMenuModal got command", command)