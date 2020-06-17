import tkinter as tk

class Module():
    def __init__(self, gui = None, title = None, description = None):
        # takes Module’s constructor
        self.title = title
        self.description = description
        self.completed = False
        #self.interactivePane = tk.Canvas(gui.win, width = 500, height = 500, bg = 'grey')
        #self.visualizingPane = tk.Canvas(gui.win, width = 500, height = 500, bg = 'white')
        #self.interactivePane.grid(row=0, column=0)
        #self.visualizingPane.grid(row=0, column=1)
        #self.interactivePane.create_text(150, 100, text = "INTERACTIVE COMPONENTS HERE")
        #self.visualizingPane.create_text(150, 100, text = "VISUALIZING COMPONENTS HERE")

    def getCompleted(self):
        return self.completed

    # overload this function
    def updatePanes(self):
        pass
