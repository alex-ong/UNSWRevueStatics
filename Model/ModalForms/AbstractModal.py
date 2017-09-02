from Model import OptionButtons
class AbstractModal(object):
    def __init__(self):
        self.onShowArguments = None
        self.onFinish = None
    
    def optionButtonBindings(self):
        return OptionButtons.NO_BINDINGS
    
    def show(self, onShowArguments, onFinish):
        OptionButtons.getInstance().setState(self.optionButtonBindings())
        self.reset()
        self.onShowArguments = onShowArguments
        self.onFinish = onFinish
        self.subclassShow()
        
    def subclassShow(self):
        pass
    
    def reset(self):
        raise NotImplementedError()
    
    def handleCommand(self, command):
        raise NotImplementedError()
    
    # silently accept rawButtons unless overridden    
    def handleRawButton(self, rawButton):
        pass
