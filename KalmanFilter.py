from Module import *
import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import matplotlib.animation as animation
from statistics import mean

class KalmanFilter(Module):
    def __init__(self, gui = None, title = None):
        super(KalmanFilter, self).__init__(gui = gui, title = title)
        self.quizQuestionMark = tk.PhotoImage(file = "quizQuestionMark.png")
        self.quizPassedImage = tk.PhotoImage(file="passedQuiz.png")
        self.quizFailedImage = tk.PhotoImage(file="failedQuiz.png")
        self.font = ('Comic Sans MS', 11, 'bold italic')
        self.quizResultFont = ('Comic Sans MS', 15, 'bold italic')
        self.axis = None
        self.xData = [1, 2, 3, 4, 5, 6, 7, 8]
        self.xMovingAvgData = []
        self.yMovingAvgData = []
        self.yData = [5.5, 6.25, 5.25, 5.5, 5.75, 4.75, 5.25, 5.75]
        self.plotIterator = 0
        self.radioVarMovingAvgQ1 = tk.StringVar()
        self.radioVarMovingAvgQ2 = tk.StringVar()


    def KalmanFilter(self):
       pass