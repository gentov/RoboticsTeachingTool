from Module import *
import tkinter as tk

class FilterModule(Module):
    def __init__(self, gui = None, title = None):
        super(FilterModule, self).__init__(gui = gui, title = title)
        pass

    def introPage(self):
        paragraph = "Here, we're going to cover the basics of filtering!\n" \
                    "First, we need to understand why filtering is important.\n"\
                    "Every measurement we take in the real world, has uncerainty.\n" \
                    "This means that we can never be too certain about the \n" \
                    "measurements we acquire. This is often why it is \n" \
                    "crucial to take multiple measurements in science! Filtering \n" \
                    "is a technique we use to get better measurements from our \n" \
                    "sensors."
        font = ('Comic Sans MS', 11, 'bold italic')
        self.animateText(paragraph,self.interactivePane, font)
        self.placeNextButton(.7, .7, pane = self.interactivePane,
                             text = "Let's go!", font = font)
        self.placeBackButton(.1, .7, pane=self.interactivePane, command=self.gui.HomePage,
                             text="Main Menu", font=font)

    def movingAverage(self):
        pass

    def particleFilter(self):
        pass

    def kalmanFilter(self):
        pass

    def runModule(self):
        self.gui.clearScreen()
        self.interactivePane = tk.Canvas(self.gui.win, width = 500, height = 500, bg = 'grey')
        self.visualizingPane = tk.Canvas(self.gui.win, width = 500, height = 500, bg = 'white')
        self.interactivePane.grid(row=0, column=0)
        self.visualizingPane.grid(row=0, column=1)
        self.introPage()

