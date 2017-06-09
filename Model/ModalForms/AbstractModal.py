class AbstractModal(object):
    def __init__(self):
        self.onShowArguments = None
        self.onFinish = None
    
    def show(self, onShowArguments, onFinish):
        self.reset()
        self.onShowArguments = onShowArguments
        self.onFinish = onFinish
    
    def reset(self):
        raise NotImplementedError()
    
    def handleCommand(self, command):
        raise NotImplementedError()
    
    