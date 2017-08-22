import tkinter as tk


import View.ViewStyle as VS
BG = '#000000'
FONT = (VS.FONT, VS.font_size(20))
FG = VS.COLOR_DIRECT

class DBOWidget(tk.Frame):
	def __init__(self, getPerc, *args):
		super().__init__(*args)
		self.config(bg=BG)
		self.columnconfigure(0, weight=1)
		self.columnconfigure(1, weight=0,minsize=VS.pixel_size(50))
		self.columnconfigure(2, weight=1)
		self.rowconfigure(0, weight=1)
		self.label1 = tk.Label(self, text='Grandmaster', bg=BG, fg=FG, font=FONT)
		self.label1.grid(sticky=tk.W)
		self.percVar = tk.StringVar()
		self.percVar.set('100%')
		self.label2 = tk.Label(self, textvariable=self.percVar, bg=BG, fg=FG, font=FONT)
		self.label2.grid(row=0, column=2, sticky=tk.E)

def _fakePerc():
	return 1.0

if __name__ == '__main__':
	root = tk.Tk()	
	widget = DBOWidget(_fakePerc, root)
	widget.grid()
	root.mainloop() 
