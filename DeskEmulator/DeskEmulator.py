import tkinter as tk
import sys
from _collections import OrderedDict
sys.path.append('../Networking')  # hack

import TopPanel
import LeftPanel
import RightPanel
import time
import asyncio
import TCPClient
import json
import collections

GUI_REFRESH = 0.01

class DeskEmulator(tk.Frame):
    def __init__(self, *args):
        super().__init__(*args)        
        self.grid()        
        
        self.topPanel = TopPanel.TopPanel(self)
        self.topPanel.grid(row=0, columnspan=2)
        
        self.leftPanel = LeftPanel.LeftPanel(self)
        self.leftPanel.grid(row=1)
        
        self.rightPanel = RightPanel.RightPanel(self)
        self.rightPanel.grid(row=1, column=1)
    
    def getState(self):
        result = OrderedDict()
        result.update(self.topPanel.getState())
        result.update(self.leftPanel.getState())
        result.update(self.rightPanel.getState())        
        return result
    
class Controller(object):
    def __init__(self, deskView, host='localhost', port=9999):
        self.deskView = deskView        
        self.lastState = self.deskView.getState()
        self.client = TCPClient.CreateClient(host, port)
        
    def update(self):
        state = self.deskView.getState()
        if (state != self.lastState):
            print (state)
            self.lastState = state
            self.client.sendMessage(json.dumps(state))

async def run_tk(root, controller, interval=GUI_REFRESH):
    '''
    Runs the tkinter loop through the asyncio event loop.
    This allows us to use asyncio coroutines, which are good for e.g loading image thumbnails from URL 
    From: https://www.reddit.com/r/Python/comments/33ecpl/neat_discovery_how_to_combine_asyncio_and_tkinter/
    '''
    printDeltas = False
    try:
        timer = time.time() * 1000
        while True:
            # update gui
            root.update()
            
            # update logic if required.
            controller.update()
                            
            await asyncio.sleep(interval)
            
            # keep track of deltaTimes for performance debugging
            newTime = time.time() * 1000            
            if printDeltas:
                print (newTime - timer)
            timer = newTime
            
    except tk.TclError as e:
        if "application has been destroyed" not in e.args[0]:
            raise  
    
if __name__ == '__main__':
    
    root = tk.Tk()
    de = DeskEmulator(root)
    controller = Controller(de)
    
    # Start running the tkinter update() through an asyncio coroutine
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run_tk(root, controller, 0.001))
