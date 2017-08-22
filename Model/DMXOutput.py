UNIVERSE_SIZE = 512
BYTE = 255
PERC = 100
class DMXOutput(object):
    def __init__(self, deskModel):
        self.deskModel = deskModel
        self.grandMaster = deskModel.grandMaster
        
    def getOutput(self):
        byteArray = [0 for i in range(UNIVERSE_SIZE)]
        
        channelValues = self.deskModel.channelValues.values
        channelToDMX = self.deskModel.patching
        
        for channelNum, channel in channelValues.items():
            percValue = channel.getDisplayValueAndReason()[0]
            percValue = float(percValue) * self.grandMaster.getValue()
            byteValue = round(percValue / PERC * BYTE)
            byteIndex = channelToDMX[channelNum] - 1
            byteArray[byteIndex] = byteValue
            
        return byteArray
            
        
