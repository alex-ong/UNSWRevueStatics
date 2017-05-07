'''
@author: alex-ong
@date 2017-05-07
'''
import json
import collections

DEFAULT_NUM_CHANNELS = 84  # default value for science theatre

def openFile(targetFile):
    try: 
        with open(targetFile, 'r') as f:
            result = json.load(f, object_pairs_hook=collections.OrderedDict)
        #json turns int keys into strings.
        finalResult = {}
        for key, value in result:
            finalResult[int(key)] = value
        result = finalResult
    except:
        result = defaultFile(targetFile)
        saveFile(result, targetFile) #turns keys into strings...
        
    return result
 

def defaultFile(targetFile=None):
    result = {x:x for x in range(1, DEFAULT_NUM_CHANNELS+1)}
    saveFile(result, targetFile)
    return result
    
def saveFile(bindings, targetFile):
    try:
        with open(targetFile, 'w') as f:
            json.dump(bindings, f, indent=4,sort_keys=True)
    except:
        print ("Error saving binding file to", targetFile)
    
