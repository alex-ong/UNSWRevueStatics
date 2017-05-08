'''
Ability to bind either a group or a channel to a fader
'''
import json
import collections
import math
DEFAULT_FADER_COUNT = 27

def openFile(targetFile, numFaders, numChannels):
    try:
        with open(targetFile, 'r') as f:
            result = json.load(f, object_pairs_hook=collections.OrderedDict)
        finalResult = {}
        for key, value in result.items():
            finalResult[int(key)] = value
        result = finalResult
    except:
        result = defaultFile(targetFile,numFaders,numChannels)
        saveFile(result, targetFile) #turns keys into strings...
        
    return result
 

def defaultFile(targetFile, numFaders, numChannels):
    # create numChannels/numFaders worth of faderPages,
    # then one page of groups
    result = []
    numPages = math.ceil(numChannels/numFaders)    
    for pageNum in range(numPages):
        page = {}
        for x in range(numFaders):
            binding = pageNum * numFaders + x + 1
            if binding > numChannels:
                break
            page[x+1] = binding 
        result.append(page) 
    result.append({x:'group'+str(x) for x in range(1,numFaders+1)})
    
    saveFile(result, targetFile)
    return result
    
def saveFile(bindings, targetFile):
    try:
        with open(targetFile, 'w') as f:
            json.dump(bindings, f, indent=4,sort_keys=True)
    except:
        print ("Error saving binding file to", targetFile)
    
