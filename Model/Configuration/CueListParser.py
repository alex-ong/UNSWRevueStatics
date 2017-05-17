'''
@author: alex-ong
@date 2017-05-16
'''
import json
import collections
from libs.sorted_containers.sorteddict import SortedDict
from Model.CueList import fromDict

def openFile(targetFile):
    try:
        with open(targetFile, 'r') as f:
            result = json.load(f)
    except:
        result = defaultFile(targetFile)
        saveFile(result, targetFile) #turns keys into strings...        
        
    return result
 

def defaultFile(targetFile):
    result = {}
    saveFile(result, targetFile)
    return result
    
def saveFile(data, targetFile):
    print ("Writing ", type(data))
    try:
        with open(targetFile, 'w') as f:
            json.dump(data, f, indent=4)
    except:
        print ("Error saving binding file to", targetFile)
    
