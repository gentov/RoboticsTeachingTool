from Module import *
from MovingAverageFIlter import *
from KalmanFilterToy import *
from KalmanFilter import*
import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import matplotlib.animation as animation
from statistics import mean

class FilterModule(Module):
    def __init__(self, gui = None, title = None):
        super(FilterModule, self).__init__(gui = gui, title = title)
        self.movingAverageModule = MovingAverageFilter(gui = gui, mainModule=self)
        self.kalmanFilterToy = KalmanFilterToy(gui = gui, mainModule = self)
        self.kalmanFilter = KalmanFilter(gui=gui, mainModule=self)
        self.font = ('Comic Sans MS', 11)
        self.noisyImage = tk.PhotoImage(file = "noisy_data.png")

    def introPage(self):
        self.gui.clearScreen()
        self.makePanes()
        paragraph = "Here, we're going to cover the basics of filtering!\n" \
                    "First, we need to understand why filtering is important.\n"\
                    "Every measurement we take in the real world, has uncerainty.\n" \
                    "This means that we can never be too certain about the \n" \
                    "measurements we acquire. This is often why it is \n" \
                    "crucial to take multiple measurements in science! Filtering \n" \
                    "is a technique we use to get better measurements from our \n" \
                    "sensors."
        self.visualizingPane.create_image(300,250,image = self.noisyImage, anchor = tk.CENTER)
        self.animateText(275, 150, paragraph,self.interactivePane, self.font)
        self.placeNextButton(.7, .7, pane = self.interactivePane,
                             text = "Let's go!", font = self.font, command = self.movingAverageModule.movingAverage)
        self.placeBackButton(.1, .7, pane=self.interactivePane, command=self.gui.HomePage,
                             text="Main Menu", font=self.font)
        self.placeBackToMenuButton(self.visualizingPane)

    def runModule(self):
        self.gui.clearScreen()
        self.makePanes()
        self.kalmanFilter.kalmanPrediction()
        #self.kalmanFilter.formKalmanFMatrix()
