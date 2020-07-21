from Module import *
import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import matplotlib.animation as animation
import matplotlib.patches as patches
from statistics import mean

class KalmanFilter(Module):
    def __init__(self, gui = None, title = None, mainModule = None):
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
        self.mainModule = mainModule
        self.car = None

    def introToKalmanFilter(self):
        self.gui.clearScreen()
        self.makePanes()
        whyKalmanFilter = \
                    "So far it seems as though the moving average is the only \n" \
                    "thing we need to be experts at filtering. It's true, the moving \n"\
                    "average is a pretty simple way to take care of really noisy data, \n"\
                    "but it's not always the tool for the job. Suppose, for example, \n"\
                    "we are building an autonomous car! We are given GPS data, but \n"\
                    "it's very noisy. Let's see what happens when we apply a moving \n" \
                    "average. For the purposes of this example, we are looking at \n" \
                    "the car from a bird's eye view."
        # create Matplotlib figure
        self.interactivePane.create_text(265, 150, text = whyKalmanFilter, font = self.font)
        f = Figure(figsize=(5, 5), dpi=100)
        self.axis = f.add_subplot(111)
        self.axis.set_ylim([0, 10])
        self.axis.set_xlim([0, 10])
        figureCanvas = FigureCanvasTkAgg(f, master=self.visualizingPane)
        figureCanvas.get_tk_widget().grid(row=0, column=0)

        #VROOM VROOM
        self.car = patches.Rectangle((2,2),2,1, linewidth=1,edgecolor='g',facecolor='g')
        self.axis.add_patch(self.car)

########################## MISC
    # def moveCar(self, event):
    #     # plot the moving average here, x stays the same
    #     if (self.plotIterator >= int(history)):
    #         self.yMovingAvgData.append(mean(self.yData[self.plotIterator - int(history):self.plotIterator]))
    #         self.xMovingAvgData.append(self.xData[self.plotIterator - 1])
    #         self.axis.plot(self.xMovingAvgData, self.yMovingAvgData,
    #                        marker='o', markersize=10.0, linestyle='None', color='b')
    #     self.plotIterator = self.plotIterator + 1
    #     if (self.plotIterator > len(self.xData)):
    #         self.ani.event_source.stop()