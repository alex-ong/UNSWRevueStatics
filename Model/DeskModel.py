'''
@author: alex-ong
@date 2017-05-07
'''
from Model import ChannelValues
import Model.Configuration.ConfigReader as ConfigReader




class DeskModel(object):
    def __init__(self):
        self.config = ConfigReader.ConfigReader('config/config.json')
        self.patching = self.config.readDMXBindings()
        
        self.channelValues = ChannelValues.ChannelValues(self.patching)    
        
    def Reset(self):
        # get configReader to reset everything, then load everything
        pass
         
    
