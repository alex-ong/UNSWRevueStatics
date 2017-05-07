'''
@author: alex-ong
@date 2017-05-07
'''
import tkinter as tk
import tkinter.ttk as ttk
import View.Widgets.ChannelFrame as ChannelFrame

class DeskView(tk.Frame):
    def __init__(self):
        root = tk.Tk()
        root.geometry('1400x500')
        super().__init__(root)
        self.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.config(bg='red')
        root.wm_title("UNSW Revue Statics")
        
        # this stops widgets using style elements overwriting other widgets also using styles
        self.style = ttk.Style(root)
        self.style.theme_use("winnative")
        
    def setupChannels(self, channels):
        cf = ChannelFrame.ChannelFrame(channels, self)
        cf.pack()
