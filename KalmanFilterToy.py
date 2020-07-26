from Module import *
import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import matplotlib.animation as animation
import matplotlib.patches as patches
from statistics import mean
import random

class KalmanFilterToy(Module):
    def __init__(self, gui = None, title = None, mainModule = None):
        super(KalmanFilterToy, self).__init__(gui = gui, title = title)
        self.quizQuestionMark = tk.PhotoImage(file = "quizQuestionMark.png")
        self.quizPassedImage = tk.PhotoImage(file="passedQuiz.png")
        self.quizFailedImage = tk.PhotoImage(file="failedQuiz.png")
        self.carImage = tk.PhotoImage(file="carImage.png")
        self.kalmanExampleImage = tk.PhotoImage(file="kalmanExampleImage.png")
        self.font = ('Comic Sans MS', 11, 'bold italic')
        self.smallFont = ('Comic Sans MS', 9, 'bold italic')
        self.quizResultFont = ('Comic Sans MS', 15, 'bold italic')
        self.axis = None
        self.carAxisKF = None
        self.xErrorKF = None
        self.vErrorKF = None
        self.xData = [0,1,2,3,4,5]
        self.xDataKalmanGainToy = None
        self.xMovingAvgData = []
        self.yMovingAvgData = []
        self.xKalmanToyData = []
        self.yData = [2,2,2,2,2,2]
        self.velKalmanToy = 0
        self.plotIterator = 0
        self.radioVarMovingAvgQ1 = tk.StringVar()
        self.radioVarMovingAvgQ2 = tk.StringVar()
        self.mainModule = mainModule
        self.car = None
        self.xErrorData = None
        self.vErrorData = None
        self.dtKalmanGainToy_sec = .1
        self.matrixMultImage = tk.PhotoImage(file="matrixMultImage.png")

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
        ## Configure the Plot(s)
        f = Figure(figsize=(5, 5), dpi=100)
        self.axis = f.add_subplot(111)
        self.axis.set_ylim([0, 10])
        self.axis.set_xlim([0, 12])
        self.axis.set_title("Car Position (Y vs X)")
        figureCanvas = FigureCanvasTkAgg(f, master=self.visualizingPane)
        figureCanvas.get_tk_widget().grid(row=0, column=0)

        #VROOM VROOM
        self.drawCar(0, 1.5, self.axis)

        movingAverageGPS = tk.Button(self.interactivePane, relief=tk.RAISED, command=lambda: self.startCarMovAvgAni(),
                                  text="Filter GPS Data")
        movingAverageGPS.place(relx=.5, rely=.42, anchor=tk.CENTER)
        self.placeNextButton(.675, .7, pane = self.interactivePane,
                             text = "The KF", font = self.font, command = self.kalmanFilterPrinciple)
        self.placeBackToMenuButton(self.visualizingPane)

    def kalmanFilterPrinciple(self):
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
                    "'x0' is initial position. We can call this our 'state transition\n" \
                    "equation'. If we can calculate our current 'v' or velocity, we can \n" \
                    "estimate where the car will be in the next measurement!"
        self.interactivePane.create_text(255, 180, text = howKalmanFilterWorks, font = self.font)
        self.placeNextButton(.675, .7, pane = self.interactivePane,
                             text = "Let's see it!", font = self.font, command = self.kalmanFilterToyTable)
        self.placeBackButton(.05, .7, pane=self.interactivePane,
                             text="Take me back!", font=self.font, command=self.introToKalmanFilter)
        self.placeBackToMenuButton(self.visualizingPane)
        self.visualizingPane.create_image(200, 250, image=self.kalmanExampleImage, anchor=tk.CENTER)
        self.visualizingPane.create_image(350, 450, image=self.carImage, anchor=tk.CENTER)
        pass

    def kalmanFilterToyTable(self):
        """
        I'm going to give the user a table of KNOWN measurements
        Since I haven't yet introduced the kalman gain, I want them
        to calculate the dt and determine the velocity using difference
        in position. Then I want them to make a prediction of the car's state.

        if the prediction doesn't line up well then the filter is wrong.

        Then, I will have them "tune" a kalman gain which determines how much weight
        is put into new and old predictions
        """
        asssignmentIntro = "    Let's work through the most simple kalman filter \n" \
                           "example. This is not yet a true kalman filter, but it \n" \
                           "applies some principles of the kalman filter. \n" \
                           "    The table below shows measured values from the GPS,\n" \
                           "but as we've learned this sensor has some noise. The real\n" \
                           "kalman filter,as we'll learn, can deal with this noise, but the\n" \
                           "point of this activity is to understand the prediction step.\n" \
                           "Using the measured value, calculate the velocity of the car, \n" \
                           "and make a 'prediction' about where the car will be at the next\n" \
                           "measurement. Assume that the time between measurements is \n" \
                           "500 ms. We will denote measurements as 'Z', and we'll denote \n" \
                           "the predictions as 'X_n'."
        equationReminder = "As a reminder: \n" \
                           "                   v = d/t  and \n" \
                           "                X_n = X_i + v*t"
        self.gui.clearScreen()
        self.makePanes()
        self.placeBackToMenuButton(self.visualizingPane)
        self.interactivePane.create_text(250, 140, text = asssignmentIntro, font = self.font)
        self.interactivePane.create_text(100, 460, text=equationReminder, font=self.smallFont)

        # Add the car
        ## Configure the Plot(s)
        f = Figure(figsize=(5, 5), dpi=100)
        self.axis = f.add_subplot(111)
        self.axis.set_ylim([0, 10])
        self.axis.set_xlim([0, 12])
        self.axis.set_title("Car Position (Y vs X)")

        figureCanvas = FigureCanvasTkAgg(f, master=self.visualizingPane)
        figureCanvas.get_tk_widget().grid(row=0, column=0)
        self.placeBackButton(.05, .6, pane=self.interactivePane,
                             text="Take me back!", font=self.font, command=self.kalmanFilterPrinciple)
        # VROOM VROOM
        self.drawCar(0, 1.5, self.axis)

        # make the table
        tableCanvas = tk.Canvas(self.interactivePane,bg="white", width=400, height=200)
        tableCanvas.place(relx = .5,rely = .7, anchor = tk.CENTER)
        numRows = 5
        numCols = 3
        measurements = [0,1.1,2.15,3.05,4.1]
        for i in range(numRows):  # Rows
            for j in range(numCols):  # Columns
                # populate measurements
                if(i == 0 and j != 0):
                    b = tk.Label(tableCanvas, text="", width=8)
                elif(j == 0):
                    b = tk.Label(tableCanvas, text=str(measurements[j+i]), width=8)
                else:
                    b = tk.Entry(tableCanvas, text="", width = 10)
                b.grid(row=i, column=j)
        zLabel = tk.Label(self.interactivePane, text = "Z", font = self.font, bg = "grey")
        zLabel.place(relx = .37, rely = .54)
        vLabel = tk.Label(self.interactivePane, text = "V", font = self.font, bg = "grey")
        vLabel.place(relx = .49, rely = .54)
        xLabel = tk.Label(self.interactivePane, text=  "X_n", font=self.font, bg="grey")
        xLabel.place(relx=.60, rely=.54)
        checkAssignmentButton = tk.Button(self.interactivePane, text = "Check my work!",
                                          command = lambda: self.checkKFTable(tableCanvas, measurements))
        checkAssignmentButton.place(relx = .5, rely = .84, anchor = tk.CENTER)


    def kalmanGainToy(self):
        self.gui.clearScreen()
        self.makePanes()
        self.placeBackToMenuButton(self.visualizingPane)
        dataPoints = 100
        self.xDataKalmanGainToy = [i for i in range(dataPoints)]
        noise = [random.randint(-100,100)/1500 for i in range(dataPoints)]
        self.xKalmanToyData = [a + b for a, b in zip(self.xDataKalmanGainToy, noise)]
        print(self.xKalmanToyData)
        aboutKalmanGain = "    We've now see that a prediction algorithm such \n" \
                           "as a basic kalman filter, produces much better results \n" \
                           "than the moving average filter. However, before we can\n" \
                           "implement a real one dimensional kalman filter, we need \n" \
                           "to understand the kalman gain. Although these lessons on \n" \
                           "the kalman filter won't derive all of the related equations,\n" \
                           "you should have an intuition on what all of the components do.\n" \
                           "   In a kalman filter, the kalman gain, K, will determine how \n" \
                           "much the estimate will change given a new measurement. The \n" \
                           "larger this value, the more your estimate will change with \n" \
                           "new measurements. Go ahead an change the kalman gain, and see \n" \
                           "how the system responds! "

        # Add the car
        ## Configure the Plot(s)
        f = Figure(figsize=(5, 5), dpi=100)
        f.subplots_adjust(wspace=.5)
        self.carAxisKF = f.add_subplot(211)
        self.carAxisKF.set_ylim([0, 5])
        self.carAxisKF.set_xlim([0, len(self.xData) + 2])
        self.carAxisKF.set_title("Car Position (Y vs X)")
        self.xPosErrorKF = f.add_subplot(223)
        self.xPosErrorKF.set_ylim([-5, 5])
        self.xPosErrorKF.set_xlabel("Time")
        self.xPosErrorKF.set_ylabel("X Error")
        self.vErrorKF = f.add_subplot(224)
        self.vErrorKF.set_ylim([-5, 5])
        self.vErrorKF.set_xlabel("Time")
        self.vErrorKF.set_ylabel("V Error")


        figureCanvas = FigureCanvasTkAgg(f, master=self.visualizingPane)
        figureCanvas.get_tk_widget().grid(row=0, column=0)

        self.interactivePane.create_text(260, 140, text=aboutKalmanGain, font=self.font)
        self.drawCar(0,1.5,self.carAxisKF)
        K = tk.Scale(self.interactivePane, from_=1, to=0.01, resolution = .001)
        K.set(.5)
        K.place(relx = .5, rely = .7, anchor = tk.CENTER)
        changeKalmanGain = tk.Button(self.interactivePane, text = "Try this Kalman Gain!",
                                     command=lambda :self.startCarKalmanGainToyAni(K.get()))
        changeKalmanGain.place(relx = .5, rely = .84, anchor = tk.CENTER)
        self.placeNextButton(.7, .75, pane=self.interactivePane,
                             text="Let's move!", font=self.font, command=self.matrixFormExplanation)
        self.placeBackButton(.05, .75, pane=self.interactivePane,
                             text="Take me back!", font=self.font, command=self.kalmanFilterToyTable)
        pass

    def matrixFormExplanation(self):
        self.gui.clearScreen()
        self.makePanes()
        self.placeBackToMenuButton(self.visualizingPane)
        aboutMatrixForm = "Before we can move onto implementing a real one dimensional\n" \
                          "kalman, we need to understand how to express information \n" \
                          "compactly in matrix form. For example, let's look at our state \n" \
                          "transition equations, how can we put those into matrix form? \n" \
                          "Our state transition equation was: \n" \
                          "                     X_n = X + v*dt \n" \
                          "Matrices multiply row by column. So, if the state of our robot \n" \
                          "is given as: [x;v], which is a 2 x 1 matrix, then our state\n" \
                          "transition matrix will be a 2 x 2 matrix. In fact, our matrix will \n" \
                          "be [1 dt; 0 1]. What this means is: 'To get X_n, multiply our\n" \
                          "X by 1, then add v*dt. To get the new velocity, just mulitply\n" \
                          "v by 1. The visual on the right will help show this a bit \n" \
                          "better."
        self.interactivePane.create_text(260, 145, text=aboutMatrixForm, font=self.font)
        self.placeNextButton(.7, .75, pane=self.interactivePane,
                             text="I get it!", font=self.font)#, command=self.matrixFormExplanation)
        self.visualizingPane.create_image(200, 250, image=self.matrixMultImage, anchor=tk.CENTER)
        self.placeBackButton(.05, .75, pane=self.interactivePane,
                             text="Take me back!", font=self.font, command=self.kalmanGainToy)
        pass
########################## MISC
    def moveCarMovingAverage(self, event):
        history = 4
        self.axis.clear()
        self.axis.set_ylim([0, 10])
        self.axis.set_xlim([0, len(self.xData) + 2])
        self.axis.set_title("Car Position (Y vs X)")

        # move the car
        self.drawCar(self.xData[self.plotIterator], 1.5, self.axis)

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

    def moveCarKalmanToy(self, event):
        self.axis.clear()
        self.axis.set_ylim([0, 10])
        self.axis.set_xlim([0, len(self.xData) + 2])
        self.axis.set_title("Car Position (Y vs X)")


        # move the car
        self.drawCar(self.xData[self.plotIterator], 1.5, self.axis)

        # plot the moving average here, y stays the same
        if (self.plotIterator >= 2):
            # plots moving average data
            self.axis.plot(self.xKalmanToyData[0:self.plotIterator - 1], self.yData[0:self.plotIterator - 1],
                           marker='o', markersize=10.0, linestyle='None', color='b')

        self.plotIterator = self.plotIterator + 1

        if (self.plotIterator > len(self.xData) - 1):
            self.ani.event_source.stop()
        self.placeBackToMenuButton(self.visualizingPane)

    def moveCarKalmanGainToy(self, event):
        self.carAxisKF.clear()
        self.carAxisKF.set_ylim([0, 5])
        self.carAxisKF.set_xlim([0, len(self.xDataKalmanGainToy) + 2])
        self.carAxisKF.set_title("Car Position (Y vs X)")
        self.xPosErrorKF.clear()
        self.xPosErrorKF.set_ylim([-5, 5])
        self.xPosErrorKF.set_xlabel("Time")
        self.xPosErrorKF.set_ylabel("X Error")
        self.vErrorKF.clear()
        self.vErrorKF.set_ylim([-5, 5])
        self.vErrorKF.set_xlabel("Time")
        self.vErrorKF.set_ylabel("V Error")
        # move the car
        self.drawCar(self.xDataKalmanGainToy[self.plotIterator], 1.5, self.carAxisKF)
        # plot the moving average here, y stays the same
        if (self.plotIterator >= 2):
            # plots moving average data
            self.xPosErrorKF.plot(self.xDataKalmanGainToy[0:self.plotIterator - 1], self.xErrorData[0:self.plotIterator - 1],
                           marker='o', markersize=1.0, color='b')
            self.vErrorKF.plot(self.xDataKalmanGainToy[0:self.plotIterator - 1], self.vErrorData[0:self.plotIterator - 1],
                                  marker='o', markersize=1.0, color='b')



        self.plotIterator = self.plotIterator + 1

        if (self.plotIterator > len(self.xDataKalmanGainToy) - 1):
            self.ani.event_source.stop()
            self.placeBackToMenuButton(self.visualizingPane)

    def startCarMovAvgAni(self):
        self.plotIterator = 0
        # create Matplotlib figure
        ## Configure the Plot(s)
        f = Figure(figsize=(5, 5), dpi=100)
        self.axis = f.add_subplot(111)
        self.axis.set_title("Car Position (Y vs X)")
        del self.yMovingAvgData[:]
        del self.xMovingAvgData[:]
        self.axis.set_xlim([0, len(self.xData) + 1])
        figureCanvas = FigureCanvasTkAgg(f, master=self.visualizingPane)
        figureCanvas.get_tk_widget().grid(row=0, column=0)
        self.ani = animation.FuncAnimation(f, self.moveCarMovingAverage, interval=500)
        poorFilteringExplanation = \
            "The blue dots represent the average position of the car, using \n" \
            "a moving average filter. What do we notice about the data? The \n" \
            "moving average filter gives us a position estimate far from where \n" \
            "the car really is. If only there was another way.... Enter, \n" \
            "the Kalman Filter (KF)! \n"

        self.interactivePane.create_text(260, 290, text = poorFilteringExplanation, font = self.font)

    def startCarKalmanToyAni(self):
        self.plotIterator = 0
        # create Matplotlib figure
        ## Configure the Plot(s)
        f = Figure(figsize=(5, 5), dpi=100)
        self.axis = f.add_subplot(111)
        self.axis.set_xlim([0, len(self.xData) + 1])
        self.axis.set_title("Car Position (Y vs X)")
        figureCanvas = FigureCanvasTkAgg(f, master=self.visualizingPane)
        figureCanvas.get_tk_widget().grid(row=0, column=0)
        self.ani = animation.FuncAnimation(f, self.moveCarKalmanToy, interval=500)

    def startCarKalmanGainToyAni(self, k):
        self.plotIterator = 0
        self.velKalmanToy = 0
        ## Configure the Plot(s)
        f = Figure(figsize=(5, 5), dpi=100)
        f.subplots_adjust(wspace=.5)
        self.carAxisKF = f.add_subplot(211)
        self.carAxisKF.set_ylim([0, 5])
        self.carAxisKF.set_xlim([0, len(self.xDataKalmanGainToy) + 2])
        self.carAxisKF.set_title("Car Position (Y vs X)")
        self.xPosErrorKF = f.add_subplot(223)
        self.xPosErrorKF.set_ylim([-5, 5])
        self.xPosErrorKF.set_xlabel("Time")
        self.xPosErrorKF.set_ylabel("X Error")
        self.vErrorKF = f.add_subplot(224)
        self.vErrorKF.set_ylim([-5, 5])
        self.vErrorKF.set_xlabel("Time")
        self.vErrorKF.set_ylabel("V Error")
        figureCanvas = FigureCanvasTkAgg(f, master=self.visualizingPane)
        figureCanvas.get_tk_widget().grid(row=0, column=0)
        self.xErrorData, self.vErrorData = self.makeKalmanFilterToyLists(self.xKalmanToyData, k)
        self.ani = animation.FuncAnimation(f, self.moveCarKalmanGainToy, interval=self.dtKalmanGainToy_sec*1000)

    def makeKalmanFilterToyLists(self, measurements, K):
        xError = []
        vError = []
        for i in range(len(measurements)):
            if(i > 0):
                v = (measurements[i] - measurements[i-1])/(self.dtKalmanGainToy_sec)
                self.velKalmanToy += K*(v - self.velKalmanToy)
                xEst = (measurements[i] + self.velKalmanToy*self.dtKalmanGainToy_sec)
                vError.append(self.velKalmanToy - (1/self.dtKalmanGainToy_sec))
                xError.append(xEst - (i+1))
        return [xError, vError]

    def drawCar(self, x,y, axis):
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
        axis.add_patch(self.car)
        axis.add_patch(carBackLeftWheel)
        axis.add_patch(carBackRightWheel)
        axis.add_patch(carFrontLeftWheel)
        axis.add_patch(carFrontRightWheel)

    def checkKFTable(self, table, measurements):
        # make a list with the calculated X values, which are just the predictions
        # If they line up with what the user put, fine --> plot it and ship it.
        # if they don't, then plot it and show how the estimate is not quite right
        vTrue = []
        xEstTrue = []

        vUser = []
        xEstUser = []

        for i in range(len(measurements)):
            if(i > 0):
                # won't run if entry is empty
                vTrue.append((measurements[i] - measurements[i-1])/(.5))
                xEstTrue.append(measurements[i] + vTrue[i-1]*.5)
                vUserFromTable = table.grid_slaves(row=i, column=1)[0]
                xEstUserFromTable = table.grid_slaves(row=i, column=2)[0]
                if(vUserFromTable.get() == ''):
                    vUser.append(0)
                else:
                    vUser.append(float(vUserFromTable.get()))
                if(xEstUserFromTable.get() == ''):
                    xEstUser.append(0)
                else:
                    xEstUser.append(float(xEstUserFromTable.get()))


        self.xKalmanToyData = xEstUser
        self.startCarKalmanToyAni()
        tolerance = .01
        isCorrect = (self.isCloseEnough(xEstTrue, xEstUser, tolerance) & self.isCloseEnough(vTrue, vUser, tolerance))
        # If their math was correct, then they get to move on
        if(isCorrect):
            self.placeNextButton(.7, .75, pane=self.interactivePane,
                                 text="You got it!", font=self.font, command = self.kalmanGainToy)
        print(vTrue, xEstTrue)
        print(vUser, xEstUser)
        # print(t, t.get())


    def isCloseEnough(self, listA, listB, tolerance):
        for i in range(len(listA)):
            if(abs(listA[i] - listB[i]) > tolerance):
                print(listA[i] - listB[i])
                return False
        return True
