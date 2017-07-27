'''
@author: alex-ong
@date 2017-05-09
'''

'''
an array of groups
'''
import Model.Group as Group
from _collections import OrderedDict


class GroupValues(object):
    def __init__(self, groupsConfiguration, channelValues):     
        self.values = OrderedDict() 
        self.setupValues(groupsConfiguration, channelValues)
        
    def setupValues(self,groupsConfiguration, channelValues):        
        for groupNumber, value in groupsConfiguration.items():            
            mapping = value['channels']
            label = value['name']
            #remap from pair of channelNum/maxValue to Channel.Channel/maxValue
            mapping = [[channelValues[pair[0]], pair[1]] for pair in mapping]
            self.values[groupNumber] = Group.Group(groupNumber, label, mapping)        
        
    def refreshGroupBindings(self, groupsConfiguration, channelValues):
        for groupNumber, value in groupsConfiguration.items():
            mapping = value['channels']
            label = value['name']
            #remap from pair of channelNum/maxValue to Channel.Channel/maxValue
            mapping = [[channelValues[pair[0]], pair[1]] for pair in mapping]            
            self.values[groupNumber].label = label
            self.values[groupNumber].channelMappings = mapping
                        
    def __iter__(self):
        return iter(self.values)
    
    def __getitem__(self, i):
        return self.values[i]
    
    def __len__(self):
        return len(self.values)
    
    def resetValues(self):
        for value in self.values:
            value.reset()
            
    def clearPlayback(self):
        for value in self.values.values():
            value.clearPlayback()
                
    def clearRecord(self):
        for value in self.values.values():
            value.clearRecord()
            