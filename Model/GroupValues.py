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
    def __init__(self, groupsConfiguration): 
        print (groupsConfiguration)       
        self.values = OrderedDict([(key,Group.Group(key, value['name'], value['channels']))
                                    for key, value in groupsConfiguration.items()]) 
        
    
    def __iter__(self):
        return iter(self.values)
    
    def __getitem__(self, i):
        return self.values[i]
    
    def __len__(self):
        return len(self.values)
    
    def resetValues(self):
        for value in self.values:
            value.reset()
            
