import json
import Model.Configuration.DMXBindingParser as DMXBindingParser
import Model.Configuration.FaderBindingParser as FaderBindingParser
import Model.Configuration.GeneralSettingParser as GeneralSettingParser
import Model.Configuration.GroupBindingParser as GroupBindingParser
import Model.Configuration.CueListParser as CueListParser
import os
import shutil

DMX_BINDING = 'dmxBinding'
SETTING_BINDING = 'settings'
GROUP_BINDINGS = 'groupBindings'
FADER_BINDINGS = 'faderBindings'
CUE_LIST = 'cueList'

class ConfigReader(object):
    def __init__(self, metaConfigPath):
        self.metaConfigPath = metaConfigPath
        self.paths = self._openConfig()
        

    def resetAll(self):
        for fileName in os.listdir('config'):
            if fileName.endswith('.json'):
                self.deleteSingleFile('config' + '/' + fileName)                                    
    
    def deleteSingleFile(self, path):
        try:
            os.remove(path)
        except Exception as e:
            print ("Error removing " + path + ":", str(e))
    
    def copySingleFile(self, path1, folder):
        try:
            shutil.copy2(path1, folder)
        except Exception as e:
            print ("Error copying file:" + str(e))
            
    def resetPatch(self):
        self.deleteSingleFile(self.paths[DMX_BINDING])
        self.deleteSingleFile(self.paths[FADER_BINDINGS])
        self.deleteSingleFile(self.paths[GROUP_BINDINGS])        
    
    def writeBackup(self):
        self.copySingleFile(self.paths[DMX_BINDING], 'configBackup/')
        self.copySingleFile(self.metaConfigPath, 'configBackup/')
        self.copySingleFile(self.paths[CUE_LIST], 'configBackup/')
        self.copySingleFile(self.paths[FADER_BINDINGS], 'configBackup/')
        self.copySingleFile(self.paths[GROUP_BINDINGS], 'configBackup/')
        self.copySingleFile(self.paths[SETTING_BINDING], 'configBackup/')        
    
    def restoreBackup(self):
        #naively copies from configBackup/
        for fileName in os.listdir('configBackup'):
            self.copySingleFile('configBackup/'+ fileName, 'config/')
        
    
    def _openConfig(self):
        try:
            with open(self.metaConfigPath, 'r') as f:
                data = json.load(f)
        except:  # e.g. metaconfigpath is inaccessible.
            data = self.defaultConfig()
            self.paths = data
            self.writeConfig()
    
        # write defaults for items that might be missing
        default = self.defaultConfig()
        default.update(data)
        data = default
        return data
            
    def writeConfig(self):        
        try:
            with open(self.metaConfigPath, 'w') as f:
                json.dump(self.paths, f, indent=4)
        except:
            print("Error Writing config file!")
   
    def defaultConfig(self):
        return {DMX_BINDING:'config/dmxBinding.json',
                SETTING_BINDING:'config/settings.json',
                GROUP_BINDINGS: 'config/groupBindings.json',
                FADER_BINDINGS: 'config/faderBindings.json',
                CUE_LIST: 'config/cueList.json'}
        
    def readDMXBindings(self, numChannels):
        return DMXBindingParser.openFile(self.paths[DMX_BINDING], numChannels)
    
    def writeDMXBindings(self, bindingDict):
        DMXBindingParser.saveFile(bindingDict, self.paths[DMX_BINDING]) 
        
    def readFaderBindings(self, numFaders, numChannels):
        return FaderBindingParser.openFile(self.paths[FADER_BINDINGS], numFaders, numChannels)
    
    def writeFaderBindings(self, bindingDict):
        FaderBindingParser.saveFile(bindingDict, self.paths[FADER_BINDINGS]) 

    def readGroupBindings(self, numFaders):
        return GroupBindingParser.openFile(self.paths[GROUP_BINDINGS], numFaders)
    
    def writeGroupBindings(self, bindingDict):
        GroupBindingParser.saveFile(bindingDict, self.paths[GROUP_BINDINGS])
            
    def readGeneralSettings(self):
        return GeneralSettingParser.openFile(self.paths[SETTING_BINDING])
    
    def writeGeneralSettings(self, bindingDict):
        GeneralSettingParser.saveFile(bindingDict, self.paths[SETTING_BINDING])
        
    def readCueList(self):
        return CueListParser.openFile(self.paths[CUE_LIST])
    
    def writeCueList(self, cueList):
        CueListParser.saveFile(cueList, self.paths[CUE_LIST])
