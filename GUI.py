import tkinter as tk
from KinModule import KinModule as Mod

class GUI():
    def __init__(self):
        self.window = tk.Tk()
        self.moduleList = {}
        # Ideally this module will be in the module list
        m = Mod(gui=self)

    def addModule(self, module):
        self.moduleList[module.title] = module

g = GUI()
g.window.mainloop()