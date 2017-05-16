'''
@author: alex-ong
@date 2017-05-16
'''
import json
import collections
from libs.sorted_containers.sorteddict import SortedDict
from Model.CueList import fromDict

def openFile(targetFile, groupValues, channelValues):
    try:
        with open(targetFile, 'r') as f:
            result = json.load(f)
        
        result = fromDict(result,groupValues,channelValues)
    except:
        result = defaultFile(targetFile,numChannels)
        saveFile(result, targetFile) #turns keys into strings...
        result = fromDict(result, groupValues,channelValues)
        
    return result
 

def defaultFile(targetFile, numChannels):
    result = {}
    saveFile(result, targetFile)
    return result
    
def saveFile(data, targetFile):
    try:
        with open(targetFile, 'w') as f:
            json.dump(data, f, indent=4,sort_keys=True)
    except:
        print ("Error saving binding file to", targetFile)
    
