'''
@author alex-ong
Takes keyboard strings from tkinter, converts them into
tcp packets
'''
import json

CONVERSION = {'plus':'+',
            'minus':'-',
            'period':'.',
            '0':'0',
            '1':'1',
            '2':'2',
            '3':'3',
            '4':'4',
            '5':'5',
            '6':'6',
            '7':'7',
            '8':'8',
            '9':'9',
            'BackSpace':'<-',
            'at':'@',
            'B':'Back',
            'b':'Back',
            'p':'Clear',
            'P':'Clear',
            'c':'Cue',
            'C':'Cue',
            'd':'DBO',
            'D':'DBO',
            'Delete':'Delete',
            'Return':'Enter',
            'f':'Full',
            'F':'Full',
            'asciitilde':'Full',
            'g':'Group',
            'G':'Group',            
            'm':'Menu',
            'M':'Menu',
            'n':'Next',
            'N':'Next',
            'r':'Record',
            'R':'Record',
            'Escape':'Release',
            'F1':'S1',
            'F2':'S2',
            'F3':'S3',
            'F4':'S4',
            'greater':'Thru',
            'asterisk':'Thru',
            't':'Time',
            'T':'Time'
            }


import Networking.TCPClient as TCPClient 
class KeyboardDaemon(object):
    def __init__(self):
        self.client = TCPClient.CreateClient('localhost', 9999)
    
    def stop(self):
        self.client.stop()
        
    def convertKey(self, keysym):
        if keysym in CONVERSION:
            return CONVERSION[keysym]
        else:
            return None
         
    def handleKeyDown(self, event):
        converted = self.convertKey(event.keysym)
        if converted is not None:            
            self.client.sendMessage(json.dumps({converted: True}))
        self.client.sendMessage(json.dumps({'raw_'+str(event.keysym): True}))

    def handleKeyUp(self, event):
        converted = self.convertKey(event.keysym)
        if converted is not None:
            self.client.sendMessage(json.dumps({converted: False}))
        self.client.sendMessage(json.dumps({'raw_'+str(event.keysym): False}))
        
        