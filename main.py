import Controller.LogicController
import Model.DeskModel
import View.DeskView as DeskView


import asyncio
import tkinter
import threading    
import time

GUI_REFRESH = 0.1
async def run_tk(root, controller, interval=GUI_REFRESH):
    '''
    Runs the tkinter loop through the asyncio event loop.
    This allows us to use asyncio coroutines, which are good for e.g loading image thumbnails from URL 
    From: https://www.reddit.com/r/Python/comments/33ecpl/neat_discovery_how_to_combine_asyncio_and_tkinter/
    '''
    printDeltas = False
    try:
        timer = time.time()
        while True:
            # update gui
            newTime = time.time()
            delta = newTime - timer            
            if printDeltas:
                print (delta)
            root.update()
            
            # update logic if required.
            controller.update(delta)
                            
            await asyncio.sleep(interval)
            
            # keep track of deltaTimes for performance debugging

            timer = newTime
            
    except tkinter.TclError as e:
        if "application has been destroyed" not in e.args[0]:
            raise     
        
if __name__ == '__main__':
    model = Model.DeskModel.DeskModel()
    view = DeskView.DeskView()
    controller = Controller.LogicController.LogicController(model, view)
    
    # Start running the tkinter update() through an asyncio coroutine
    loop = asyncio.get_event_loop()
    loop.run_until_complete(run_tk(view, controller, 0.001))
    
    controller.sliderInput.stop()    
    print ("All Done - printing hanging threads")
    for t in threading.enumerate():
        if (t != threading.current_thread()):
            print (t)
            
