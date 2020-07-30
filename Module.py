import tkinter as tk
import time
import dill as pickle

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
        self.mainMenuButtonImage = None
        self.saveButtonImage = None

    def getCompleted(self):
        return self.completed

    # overload this function
    def updatePanes(self):
        pass

    def runModule(self):
        self.gui.clearScreen()
        self.makePanes()

    # Can we make this non-blocking? Probably not critical...
    def animateText(self, x, y, text, canvasOfText, font):
        characterArray = list(text)
        canvasOfText.create_text(x,y , text="",
                                         font=font)
        animatedText = ""
        self.gui.win.update()
        for char in characterArray:
            animatedText += char
            canvasOfText.delete(tk.ALL)
            canvasOfText.create_text(x, y, text=animatedText,
                                             font=font)
            self.gui.win.update()
            time.sleep(.003)

    def showText(self, x, y, text, canvasOfText, font):
        canvasOfText.create_text(x, y, text=text, font=font, width = 400)
        self.gui.win.update()

    def makePanes(self):
        self.interactivePane = tk.Canvas(self.gui.win, width=500, height=500, bg='grey')
        self.visualizingPane = tk.Canvas(self.gui.win, width=500, height=500, bg='white')
        self.interactivePane.grid(row=0, column=0)
        self.visualizingPane.grid(row=0, column=1)
    """
    Places the button to go to the next page.
    x: relative location in pane where you want it (from 0 to 1)
    y: relative location in pane where you want it (from 0 to 1)
    text: text you want on the button
    command: callback function for the button
    font: the font you want
    """
    def placeNextButton(self, x,y,pane, text = None,command = None, font = None):
        nextButton = tk.Button(pane, bg=pane["background"], relief=tk.FLAT, command=command)
        self.nextButtonImage = tk.PhotoImage(file="next.png")
        nextButton.config(image=self.nextButtonImage, compound='center', text=text, font=font)
        nextButton.place(relx=x, rely=y)


    def placeBackToMenuButton(self, pane):
        mainMenuButton = tk.Button(pane, bg=pane["background"], relief=tk.FLAT, command=self.gui.HomePage)
        self.mainMenuButtonImage = tk.PhotoImage(file="mainMenu.png")
        mainMenuButton.config(image=self.mainMenuButtonImage, compound='center')
        mainMenuButton.place(relx=.87, rely=.025) # I figured the top right corner was ok, but maybe we want params

    """
    Places the button to go to the previous page.
    x: relative location in pane where you want it (from 0 to 1)
    y: relative location in pane where you want it (from 0 to 1)
    text: text you want on the button
    command: callback function for the button
    font: the font you want
    """
    def placeBackButton(self, x,y,pane, text = None,command = None, font = None):
        backButton = tk.Button(pane, bg=pane["background"], relief=tk.FLAT, command=command)
        self.backButtonImage = tk.PhotoImage(file="back.png")
        backButton.config(image=self.backButtonImage, compound='center', text=text, font=font)
        backButton.place(relx=x, rely=y)

    def placeSaveButton(self, pane,progressFile, page):
        saveButton = tk.Button(pane, bg=pane["background"], relief=tk.FLAT, command=lambda:
                                            self.saveModuleProgress(progressFile,page))
        self.saveButtonImage = tk.PhotoImage(file="saveButtonImage.png")
        saveButton.config(image=self.saveButtonImage, compound='center')
        saveButton.place(relx=.87, rely=.85) # I figured the top left corner was ok, but maybe we want params

    def saveModuleProgress(self, progressFile, page):
        pickle.dump(page, open(progressFile, "wb"))
