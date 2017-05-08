import json
import Model.Configuration.DMXBindingParser as DMXBindingParser
import Model.Configuration.FaderBindingParser as FaderBindingParser
import Model.Configuration.GeneralSettingParser as GeneralSettingParser
import Model.Configuration.GroupBindingParser as GroupBindingParser
DMX_BINDING = 'dmxBinding'
SETTING_BINDING = 'settings'
GROUP_BINDINGS = 'groupBindings'
FADER_BINDINGS = 'faderBindings'
    
class ConfigReader(object):
    def __init__(self, metaConfigPath):
        self.metaConfigPath = metaConfigPath
        self.paths = self._openConfig()
        

    def resetAll(self):
        pass
        
    def writeBackup(self):
        pass
    
    def restoreBackup(self):
        pass
    
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
                FADER_BINDINGS: 'config/faderBindings.json'}
        
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
        
