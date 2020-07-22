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
        self.carImage = tk.PhotoImage(file="carImage.png")
        self.kalmanExampleImage = tk.PhotoImage(file="kalmanExampleImage.png")
        self.font = ('Comic Sans MS', 11, 'bold italic')
        self.quizResultFont = ('Comic Sans MS', 15, 'bold italic')
        self.axis = None
        self.xData = [0,1,2,3,4,5,6,7,8,9]
        self.xMovingAvgData = []
        self.yMovingAvgData = []
        self.yData = [2,2,2,2,2,2,2,2,2,2]
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
        self.interactivePane.create_text(260, 100, text = whyKalmanFilter, font = self.font)
        f = Figure(figsize=(5, 5), dpi=100)
        self.axis = f.add_subplot(111)
        self.axis.set_ylim([0, 10])
        self.axis.set_xlim([0, 12])
        figureCanvas = FigureCanvasTkAgg(f, master=self.visualizingPane)
        figureCanvas.get_tk_widget().grid(row=0, column=0)

        #VROOM VROOM
        self.drawCar(0, 1.5)

        movingAverageGPS = tk.Button(self.interactivePane, relief=tk.RAISED, command=lambda: self.startCarMovAvgAni(),
                                  text="Filter GPS Data")
        movingAverageGPS.place(relx=.5, rely=.42, anchor=tk.CENTER)
        self.placeNextButton(.675, .7, pane = self.interactivePane,
                             text = "The KF", font = self.font, command = self.kalmanFilterPrinciple)
        self.placeBackToMenuButton(self.visualizingPane)

    def kalmanFilterPrinciple(self):
        """
        Have them calculate the velocity and from there see if the prediction lines up
        """
        self.gui.clearScreen()
        self.makePanes()
        howKalmanFilterWorks = \
                    "   The working principle of the Kalman Filter is quite different \n" \
                    "than that of the moving average filter. Imagine we are given GPS \n" \
                    "coordinates, X and Y. Assume also that at each measurement, \n" \
                    "we take a time-stamp. This means that we have some raw XY \n" \
                    "data, and some time data. How can we use this?\n" \
                    "   If we can model our system, we can make a prediction \n" \
                    "about the future state of the car, based on our current \n" \
                    "state. For those of you who have taken physics, the \n" \
                    "following equations might look familiar: \n" \
                    "                           v = d/t              \n" \
                    "                       xf = x0 + v*t        \n" \
                    "In the first equation 'd' is distance, 'v' is velocity, and \n" \
                    "'t' is time. In the second equation, 'xf' is final position, and \n" \
                    "'x0' is initial position. We will call this our system! If we can \n" \
                    "calculate our current 'v' or velocity, we can estimate where the\n" \
                    "car will be in the next measurement!"
        self.interactivePane.create_text(260, 190, text = howKalmanFilterWorks, font = self.font)
        self.placeNextButton(.675, .7, pane = self.interactivePane,
                             text = "Let's see it!", font = self.font)#, command = self.kalmanFilterPrinciple)
        self.placeBackToMenuButton(self.visualizingPane)
        self.visualizingPane.create_image(200, 250, image=self.kalmanExampleImage, anchor=tk.CENTER)
        self.visualizingPane.create_image(350, 450, image=self.carImage, anchor=tk.CENTER)
        pass
########################## MISC
    def moveCar(self, event):
        history = 4
        self.axis.clear()
        self.axis.set_ylim([0, 10])
        self.axis.set_xlim([0, len(self.xData) + 2])

        # move the car
        self.drawCar(self.xData[self.plotIterator], 1.5)

        # plot the moving average here, y stays the same
        if (self.plotIterator >= int(history)):
            self.xMovingAvgData.append(mean(self.xData[self.plotIterator - int(history):self.plotIterator]))
            self.yMovingAvgData.append(self.yData[self.plotIterator - 1])
            # plots moving average data
            self.axis.plot(self.xMovingAvgData, self.yMovingAvgData,
                           marker='o', markersize=10.0, linestyle='None', color='b')

        self.plotIterator = self.plotIterator + 1

        if (self.plotIterator > len(self.xData) - 1):
            self.ani.event_source.stop()
        self.placeBackToMenuButton(self.visualizingPane)

    def drawCar(self, x,y):
        carHeight = 1
        carWidth = 2
        # move the car
        self.car = patches.Rectangle((x, y), carWidth, carHeight, linewidth=1, edgecolor='g',
                                     facecolor='g')
        carFrontRightWheel = patches.Rectangle((x + carWidth - .5, y + carHeight), .5, .25, linewidth=1, edgecolor='black',
                                     facecolor='black')
        carFrontLeftWheel = patches.Rectangle((x + carWidth - .5, y - .25), .5, .25, linewidth=1, edgecolor='black',
                                               facecolor='black')
        carBackRightWheel = patches.Rectangle((x, y - .25), .5, .25, linewidth=1, edgecolor='black',
                                               facecolor='black')
        carBackLeftWheel = patches.Rectangle((x, y + carHeight), .5, .25, linewidth=1, edgecolor='black',
                                               facecolor='black')
        self.axis.add_patch(self.car)
        self.axis.add_patch(carBackLeftWheel)
        self.axis.add_patch(carBackRightWheel)
        self.axis.add_patch(carFrontLeftWheel)
        self.axis.add_patch(carFrontRightWheel)

        pass

    def startCarMovAvgAni(self):
        self.plotIterator = 0
        # create Matplotlib figure
        f = Figure(figsize=(5, 5), dpi=100)
        self.axis = f.add_subplot(111)
        del self.yMovingAvgData[:]
        del self.xMovingAvgData[:]
        self.axis.set_xlim([0, len(self.xData) + 1])
        figureCanvas = FigureCanvasTkAgg(f, master=self.visualizingPane)
        figureCanvas.get_tk_widget().grid(row=0, column=0)
        self.ani = animation.FuncAnimation(f, self.moveCar, interval=500)
        poorFilteringExplanation = \
            "The blue dots represent the average position of the car, using \n" \
            "a moving average filter. What do we notice about the data? The \n" \
            "moving average filter gives us a position estimate far from where \n" \
            "the car really is. If only there was another way.... Enter, \n" \
            "the Kalman Filter (KF)! \n"

        self.interactivePane.create_text(260, 290, text = poorFilteringExplanation, font = self.font)
