class LogicController(object):
    def __init__(self, model, view):
        self.model = model
        self.view = view
    
        self.view.setupChannels(model.channelValues)
        
    def update(self):
        pass
        #use this function to poll the midi controller etc.