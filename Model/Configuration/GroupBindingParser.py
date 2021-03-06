'''
@author: alex-ong
@date 2017-05-07
'''
import json
import collections

def openFile(targetFile, numFaders):
    try:
        with open(targetFile, 'r') as f:
            result = json.load(f, object_pairs_hook=collections.OrderedDict)
        finalResult = {}
        for key, value in result.items():
            finalResult[int(key)] = value
        result = finalResult
    except:
        result = defaultFile(targetFile, numFaders)
        saveFile(result, targetFile)  # turns keys into strings...
        
    return result
 

def defaultFile(targetFile, numFaders):
    result = {x:{'name': 'Group' + str(x).zfill(2), 'channels':[]} 
              for x in range(1, numFaders + 1)}
    saveFile(result, targetFile)
    return result
    
def saveFile(bindings, targetFile):
    try:
        with open(targetFile, 'w') as f:
            json.dump(bindings, f, indent=4, sort_keys=True)
    except:
        print ("Error saving binding file to", targetFile)
    
