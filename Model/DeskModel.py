'''
@author: alex-ong
@date 2017-05-07
'''
from Model import ChannelValues
import Model.Configuration.ConfigReader as ConfigReader




class DeskModel(object):
    def __init__(self):
        self.config = ConfigReader.ConfigReader('config/config.json')
        self.settings = self.config.readGeneralSettings()
        numFaders = self.settings['faders']
        numChannels = self.settings['channels']
        
        self.patching = self.config.readDMXBindings(numChannels)
        self.faderBindings = self.config.readFaderBindings(numFaders, numChannels)
        self.channelValues = ChannelValues.ChannelValues(self.patching)    
        
    def Reset(self):
        # get configReader to reset everything, then load everything
        pass
         
    
