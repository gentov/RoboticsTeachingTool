import tkinter as tk
import time

class Module():
    def __init__(self, gui = None, title = None, description = None):
        # takes Module’s constructor
        self.title = title
        self.description = description
        self.completed = False
        self.gui = gui
        self.interactivePane = tk.Canvas()
        self.visualizingPane = tk.Canvas()
        self.nextButtonImage = None
        self.backButtonImage = None

    def getCompleted(self):
        return self.completed

    # overload this function
    def updatePanes(self):
        pass

    def runModule(self):
        self.gui.clearScreen()
        self.interactivePane = tk.Canvas(self.gui.win, width = 500, height = 500, bg = 'grey')
        self.visualizingPane = tk.Canvas(self.gui.win, width = 500, height = 500, bg = 'white')
        self.interactivePane.grid(row=0, column=0)
        self.visualizingPane.grid(row=0, column=1)
        self.interactivePane.create_text(150, 100, text = "INTERACTIVE COMPONENTS HERE")
        self.visualizingPane.create_text(150, 100, text = "VISUALIZING COMPONENTS HERE")

    # Can we make this non-blocking? Probably not critical...
    def animateText(self, text, canvasOfText, font):
        characterArray = list(text)
        canvasOfText.create_text(300,150 , text="",
                                         font=font)
        animatedText = ""
        self.gui.win.update()
        for char in characterArray:
            animatedText += char
            self.interactivePane.delete(tk.ALL)
            self.interactivePane.create_text(275, 150, text=animatedText,
                                             font=font)
            self.gui.win.update()
            time.sleep(.003)

    """
    Places the button to go to the next page.
    x: relative location in pane where you want it (from 0 to 1)
    y: relative location in pane where you want it (from 0 to 1)
    text: text you want on the button
    command: callback function for the button
    font: the font you want
    """
    def placeNextButton(self, x,y,pane, text = None,command = None, font = None):
        nextButton = tk.Button(pane, bg='grey', relief=tk.FLAT, command=command)
        self.nextButtonImage = tk.PhotoImage(file="next.png")
        nextButton.config(image=self.nextButtonImage, compound='center', text=text, font=font)
        nextButton.place(relx=x, rely=y)

    """
    Places the button to go to the previous page.
    x: relative location in pane where you want it (from 0 to 1)
    y: relative location in pane where you want it (from 0 to 1)
    text: text you want on the button
    command: callback function for the button
    font: the font you want
    """
    def placeBackButton(self, x,y,pane, text = None,command = None, font = None):
        backButton = tk.Button(pane, bg='grey', relief=tk.FLAT, command=command)
        self.backButtonImage = tk.PhotoImage(file="back.png")
        backButton.config(image=self.backButtonImage, compound='center', text=text, font=font)
        backButton.place(relx=x, rely=y)