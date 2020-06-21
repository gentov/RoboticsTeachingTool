import tkinter as tk

class Module():
    def __init__(self, gui = None, title = None, description = None):
        # takes Module’s constructor
        self.title = title
        self.description = description
        self.completed = False
        self.gui = gui
        self.interactivePane = None
        self.visualizingPane = None

    def getCompleted(self):
        return self.completed

    # overload this function
    def updatePanes(self):
        pass

    def runModule(self):
        self.clearScreen()
        self.interactivePane = tk.Canvas(self.gui.win, width = 500, height = 500, bg = 'grey')
        self.visualizingPane = tk.Canvas(self.gui.win, width = 500, height = 500, bg = 'white')
        self.interactivePane.grid(row=0, column=0)
        self.visualizingPane.grid(row=0, column=1)
        self.interactivePane.create_text(150, 100, text = "INTERACTIVE COMPONENTS HERE")
        self.visualizingPane.create_text(150, 100, text = "VISUALIZING COMPONENTS HERE")

    def clearScreen(self):
        for widget in self.gui.win.winfo_children():
            widget.destroy()