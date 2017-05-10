'''
@author: alex-ong
@date 2017-05-07
'''
import json
import collections

DEFAULT_FADERS = 27
DEFAULT_CHANNELS = 84

def openFile(targetFile):
    try:
        with open(targetFile, 'r') as f:
            result = json.load(f, object_pairs_hook=collections.OrderedDict)
    except:
        result = defaultFile(targetFile)
        saveFile(result, targetFile)  # turns keys into strings...
        
    return result
 
    
def defaultFile(targetFile=None):
    result = {'channels':DEFAULT_CHANNELS,
              'faders':DEFAULT_FADERS,
              'lastFaderPage': 0}
    saveFile(result, targetFile)
    return result
    
def saveFile(bindings, targetFile):
    try:
        with open(targetFile, 'w') as f:
            json.dump(bindings, f, indent=4, sort_keys=True)
    except:
        print ("Error saving binding file to", targetFile)
    
