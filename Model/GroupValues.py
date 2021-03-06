'''
@author: alex-ong
@date 2017-05-09
'''

'''
an array of groups
'''
import Model.Group as Group
from _collections import OrderedDict
from Model.CommandProgrammer.parser import GROUP

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
        prevRecordValues = {}
        #mute everything
        for (key, group) in self.values.items():
            prevRecordValues[key] = group.recordValue
            group.setRecordValue(0)
            
        for groupNumber, value in groupsConfiguration.items():
            mapping = value['channels']
            label = value['name']
            #remap from pair of channelNum/maxValue to Channel.Channel/maxValue
            mapping = [[channelValues[pair[0]], pair[1]] for pair in mapping]            
            self.values[groupNumber].label = label
            self.values[groupNumber].channelMappings = mapping
        
        #unmute everything
        for (key, value) in prevRecordValues.items():
            if key in self.values:
                self.values[key].setRecordValue(value)
    
    def getCurrentPlaybackValues(self):
        result = {}
        for groupNumber, value in self.values.items():
            result['group'+str(groupNumber)] = value.playbackValue
        return result
    
    def changeLabel(self, groupName, newLabel):
        try:
            groupNumber = int(groupName.replace(GROUP,''))
        except:
            return
        self.values[groupNumber].label = newLabel
    
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
            