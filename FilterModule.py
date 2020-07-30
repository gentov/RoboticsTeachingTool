from Module import *
from MovingAverageFIlter import *
from KalmanFilterToy import *
from KalmanFilter import*
import tkinter as tk
from enum import Enum
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import matplotlib.animation as animation
from statistics import mean


# This is an enumeration of all the pages
# so that we have better variable names
# instead of numbers
class FilterModulePages(Enum):
    INTROPAGE = 1
    MOVING_AVERAGE = 2
    MOVING_AVERAGE_QUIZ = 3
    INTRO_KF_TOY = 4
    KF_PRINCIPLE = 5
    KF_TOY_TABLE = 6
    KF_TOY_GAIN = 7
    MATRIX_FORM = 8
    KALMAN_TOY_QUIZ = 9
    INTRO_KF = 10
    KALMAN_PREDICTION = 11
    KALMAN_MEASURE_UPDATE = 12
    KALMAN_MATRIX_QUIZ = 13
    KALMAN_FORM_F = 14
    KALMAN_FORM_H = 15
    KALMAN_FORM_X = 16
    RUN_KALMAN = 17

class FilterModule(Module):
    def __init__(self, gui = None, title = None):
        super(FilterModule, self).__init__(gui = gui, title = title)
        self.movingAverageModule = MovingAverageFilter(gui = gui, mainModule=self)
        self.kalmanFilterToy = KalmanFilterToy(gui = gui, mainModule = self)
        self.kalmanFilter = KalmanFilter(gui=gui, mainModule=self)
        self.font = ('Comic Sans MS', 11)
        self.noisyImage = tk.PhotoImage(file = "noisy_data.png")
        # I make an object to hold the enumeration
        self.FilterModulePages = FilterModulePages
        try:
            self.lastPage = pickle.load(open(str(title) + "_SaveFile.pkl", "rb"))
            self.progressFile = str(title) + "_SaveFile.pkl"
        except:
            self.progressFile = str(title) + "_SaveFile.pkl"
            self.lastPage = None


        #the enumeration points to a function via a dictionary
        self.pageDictionary = {
            self.FilterModulePages.INTROPAGE: self.introPage,
            self.FilterModulePages.MOVING_AVERAGE: self.movingAverageModule.movingAverage,
            self.FilterModulePages.MOVING_AVERAGE_QUIZ: self.movingAverageModule.movingAvgQuiz,
            self.FilterModulePages.INTRO_KF_TOY: self.kalmanFilterToy.introToKalmanFilter,
            self.FilterModulePages.KF_PRINCIPLE: self.kalmanFilterToy.kalmanFilterPrinciple,
            self.FilterModulePages.KF_TOY_TABLE: self.kalmanFilterToy.kalmanFilterToyTable,
            self.FilterModulePages.KF_TOY_GAIN: self.kalmanFilterToy.kalmanGainToy,
            self.FilterModulePages.MATRIX_FORM: self.kalmanFilterToy.matrixFormExplanation,
            self.FilterModulePages.KALMAN_TOY_QUIZ: self.kalmanFilterToy.kalmanToyQuiz,
            self.FilterModulePages.INTRO_KF: self.kalmanFilter.introPage,
            self.FilterModulePages.KALMAN_PREDICTION: self.kalmanFilter.kalmanPrediction,
            self.FilterModulePages.KALMAN_MEASURE_UPDATE: self.kalmanFilter.kalmanMeasureAndUpdate,
            self.FilterModulePages.KALMAN_MATRIX_QUIZ: self.kalmanFilter.kalmanMatricesQuiz,
            self.FilterModulePages.KALMAN_FORM_F: self.kalmanFilter.formKalmanFMatrix,
            self.FilterModulePages.KALMAN_FORM_H: self.kalmanFilter.formKalmanHMatrix,
            self.FilterModulePages.KALMAN_FORM_X: self.kalmanFilter.formKalmanXMatrix,
            self.FilterModulePages.RUN_KALMAN: self.kalmanFilter.runKalmanFilter
        }
        self.lastPage = FilterModulePages.INTROPAGE

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
        try:
            self.lastPage = pickle.load(open(self.progressFile, "rb"))
        except:
            pass
        print(self.lastPage)
        self.pageDictionary[self.lastPage]()
