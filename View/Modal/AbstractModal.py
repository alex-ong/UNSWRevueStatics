import tkinter as tk

class AbstractModal(tk.Toplevel):
    def __init__(self, data, keyboardHandler, *args):
        self.keyboardHandler = keyboardHandler
        super().__init__(*args)
        self.bind("<KeyPress>", self.keyboardHandler)
        self.data = data
        self.closeCallback = None
        self.isVisible = False
        
        self.subClassSetup()
        
        self.centreOnScreen()  
        self.overrideredirect(True)        
        self.hide()
        
    def subClassSetup(self):
        pass
    
    def refresh(self):
        if self.isVisible:
            self.subclassRefresh()
            
    def subclassRefresh(self):
        pass
    
    # called only once, when the form is shown.
    # override and call this first to add functionality
    def showRefresh(self):
        self.reset()
        self.refresh()
        
    def show(self, data):
        self.data = data
        self.deiconify()
        self.overrideredirect(True)
        self.isVisible = True
        self.showRefresh()
    
    def hide(self):
        self.overrideredirect(False)
        self.withdraw()
        self.isVisible = False
        
    def done(self, result):
        self.closeCallback(result)
        
    def centreOnScreen(self):
        self.update_idletasks()  # refresh widget to get correct size
        w = self.winfo_width()
        h = self.winfo_height()
        geoString = '%dx%d+%d+%d' % (w, h,
                                     int(self.winfo_screenwidth() / 2 - 0.5 * w),
                                     int(self.winfo_screenheight() / 2 - 0.5 * h))        
        self.geometry(geoString)
        
