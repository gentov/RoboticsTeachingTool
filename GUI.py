import tkinter as tk
from Module import *
class GUI():
    def __init__(self):
        self.window = tk.Tk()
        self.moduleList = {}
        # Ideally this module will be in the module list
        m = Module(gui=self, title="test")

    def addModule(self, module):
        self.moduleList[module.title] = module

g = GUI()
g.window.mainloop()