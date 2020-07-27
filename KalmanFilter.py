from Module import *
import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import matplotlib.animation as animation
import matplotlib.patches as patches
from statistics import mean
import random
import numpy as np

class KalmanFilter(Module):
    def __init__(self, gui = None, title = None, mainModule = None):
        super(KalmanFilter, self).__init__(gui = gui, title = title)
        self.mainModule = mainModule
        self.bigFont = ('Comic Sans MS', 14, 'bold italic')
        self.font = ('Comic Sans MS', 11, 'bold italic')
        self.smallFont = ('Comic Sans MS', 9, 'bold italic')
        self.quizResultFont = ('Comic Sans MS', 15, 'bold italic')
        self.quizQuestionMark = tk.PhotoImage(file="quizQuestionMark.png")
        self.quizPassedImage = tk.PhotoImage(file="passedQuiz.png")
        self.quizFailedImage = tk.PhotoImage(file="failedQuiz.png")
        self.radioVarMovingAvgQ1 = tk.StringVar()
        self.radioVarMovingAvgQ2 = tk.StringVar()
        self.kalmanXError = []
        self.kalmanVError = []
        self.dt_sec = .1
        self.ani = None
        # Initial State
        self.x = np.matrix([[0.],
                            [0.]])

        # Uncertainity Matrix (0 being we trust the state completely)
        self.P = np.matrix([[1000, 0.],
                            [0., 1000]])

        # Next State Function
        self.F = np.matrix([[1., self.dt_sec],
                            [0., 1.]])

        # Measurement Function
        self.H = np.matrix([[1., 0.]])

        # Measurement Uncertainty (0 being we trust the state completely)
        self.R = np.matrix([[0.7]])

        # Identity Matrix
        self.I = np.matrix([[1., 0.],
                            [0., 1.]])

        self.Q = np.matrix([[.1, 0.],
                            [0., .1]])

    def introPage(self):
        self.gui.clearScreen()
        canvas = tk.Canvas(self.gui.win, width = 1000, height = 500, bg = 'grey')
        canvas.grid(row = 0, column = 0)
        self.placeBackToMenuButton(canvas)
        self.placeSaveButton(canvas)
        self.placeNextButton(.85, .75, pane=canvas,
                             text="KF Prediction", font=self.font, command = self.kalmanPrediction)
        title = "The Kalman Filter: "
        theKalmanEquations = \
                          "We can finally start talking about designing a real KF! " \
                          "We know that the kalman filter is a prediction-based filter. \n" \
                          "When a new measurement is made, the KF updates and corrects " \
                          "its prediction. The following are all of the equations in both \n" \
                          "the prediction and update steps. Don't get discouraged! We'll go" \
                          " through each one!\n" \
                          "     Prediction: \n" \
                          "                                     x = F*x\n" \
                          "                                     P = F*P*F' + Q \n" \
                          "     Measure and Update: \n" \
                          "                                     Y = Z - H*x \n" \
                          "                                     K = (P*H')/((H*P*H') + R)\n" \
                          "                                     x = x + K*Y\n" \
                          "                                     P = (I - K*H)*P \n" \
                          "Although this lesson will not be deriving each one of these " \
                          "equations from scratch, you'll know what the matrices mean, and\n" \
                          "how to design them! \n\n"

        disclaimer = "Note: The matrices Q and R are matrices " \
                      "we can not design. Usually, we must find the values of these " \
                      "matrices experimentally."
        canvas.create_text(100, 55, text = title, font = self.bigFont)
        canvas.create_text(500, 250, text=theKalmanEquations, font=self.font)
        canvas.create_text(450, 400, text=disclaimer, font=self.smallFont)

    def kalmanPrediction(self):
        self.gui.clearScreen()
        self.makePanes()
        self.visualizingPane.config(bg = "grey")
        self.placeBackToMenuButton(self.visualizingPane)
        self.placeNextButton(.7, .75, pane=self.visualizingPane,
                             text="KF Measure \n & Update", font=self.font, command=self.kalmanMeasureAndUpdate)
        self.placeBackButton(.05, .75, pane=self.visualizingPane,
                             text="KF Equations", font=self.font, command=self.introPage)
        thePredictionStep = \
                          "Believe it or not, we've done some of this! We just \n" \
                          "didn't use all of the fancy letters that the previous page did.\n" \
                          "Let's look at the prediction step equations again:\n" \
                          "Prediction: \n" \
                          "                        x = F*x\n" \
                          "                      P = F*P*F' + Q \n" \
                          "'x' is just our state matrix. In our previous examples, our \n" \
                          "state was just position and velocity (X and v). The state \n" \
                          "gives us information about our robot at any time. If we cared \n" \
                          "about the robot's orientation then our state may look something \n" \
                          "like this:\n" \
                          "                           [X]\n" \
                          "                           [v]\n" \
                          "                         [theta]\n"\
                          "The state is always a single dimension (n x 1). So what is F? \n" \
                          "F is the state transition matrix! It tells us how to get from \n" \
                          "one state to the next. In our previous examples, this F was:\n" \
                          "                         [1 dt] \n" \
                          "                         [0  1] \n" \
                          "The state transition matrix is always n x n, where n is the\n" \
                          "number of elements in your state matrix (or vector). "
        self.interactivePane.create_text(260, 240, text=thePredictionStep, font=self.font)
        thePredictionStepCont = \
                          "Next comes the P matrix. This is a matrix that explains\n" \
                          "how uncertain we are about our estimate of each element of the\n" \
                          "state vector that we've just made using the first equation.\n" \
                          "This matrix (usually) has values on its diagonal. The larger\n" \
                          "the values, the less certain we are about our estimate. Because\n" \
                          "the P matrix gives us the uncertainty of state estimate, its \n" \
                          "dimension will always be n x n. P might look something like: \n " \
                          "                         [100 0]\n" \
                          "                          [0 100]\n" \
                          "in our case.\n" \
                          "So now we know about the P matrix, and all that is left in the \n" \
                          "prediction step is the Q matrix. Q is our 'Process Noise\n" \
                          "Covariance' matrix. As the KF runs, P becomes more certain. Q\n" \
                          "allows us to add a little bit of uncertainty back into P. Q is\n" \
                          "also n x n, with values on the diagonal. Q might look like: \n " \
                          "                          [.001 0]\n" \
                          "                           [0 .001]"
        self.visualizingPane.create_text(260, 220, text=thePredictionStepCont, font=self.font)
        pass

    def kalmanMeasureAndUpdate(self):
        self.gui.clearScreen()
        self.makePanes()
        self.visualizingPane.config(bg = "grey")
        self.placeBackToMenuButton(self.visualizingPane)
        theMeasureAndUpdateStep = \
            "Now, let's look at the measure and update step equations again:\n" \
            "Measure and Update: \n" \
            "                         Y = Z - H*x \n" \
            "                    K = (P*H')/((H*P*H') + R)\n" \
            "                          x = x + K*Y\n" \
            "                        P = (I - K*H)*P \n"\
            "We need to look at the matrices a bit out of order. We'll start \n" \
            "the matrix H. H is the 'measurement function' matrix. It is \n" \
            "used to extract from the current state, the element we're trying \n" \
            "to measure. Suppose we are trying to measure velocity. In this\n" \
            "case, H would try to extract only 'v' from our state vector. It \n" \
            "may look something like:\n" \
            "                           H = [0 1]\n" \
            "Since H*x would yeild just v. H is always m x n, where m is the\n" \
            "number of measurements, and n is the number of elements in the\n" \
            "state vector.\n" \
            "   The Z matrix, we actually saw when we were filling in our KF \n" \
            "table in our previous section. Z is the actual 'Measurement\n" \
            "Vector'. If we were measuring velocity, Z might look like: \n" \
            "                           Z = [2.1]\n" \
            "This is the data coming from our sensor. It should \n" \
            "always be a m x 1 vector."
        self.interactivePane.create_text(255, 250, text=theMeasureAndUpdateStep, font=self.font)

        theMeasureAndUpdateStepCont = "Y is simply the difference between the actual and the \n" \
                                   "predicted measurement. K may look familiar to you as well! In the \n" \
                                   "previous activity we've manually adjusted K in order to 'tune' our\n" \
                                   "kalman filter. Now, K is computed using matrices H, and P, which\n" \
                                   "we've talked about, but what about R?\n" \
                                   "    R, similar to Q, which we've mentioned previously, is noise.\n" \
                                   "Unlike Q which is process noise covariance, R is measurement\n" \
                                   "noise covariance. Like Q and P, the values are (usually) on the\n" \
                                   "diagonal. The less accurate a sensor is, the larger the values\n" \
                                   "are. The matrix is m x m. For our velocity example, it may \n" \
                                   "look like: \n" \
                                   "                             R = [.2]                    \n" \
                                   "The only matrix left to discuss is I. I is actually just the \n" \
                                   "identity matrix, which is always n x n. For our example, since\n" \
                                   "we have two elements in our state, n is 2. Thus I is:\n" \
                                   "                              [1 0] \n" \
                                   "                              [0 1] "
        self.visualizingPane.create_text(255, 220, text=theMeasureAndUpdateStepCont, font=self.font)
        self.placeNextButton(.7, .75, pane=self.visualizingPane,
                             text="Quiz!", font=self.font, command = self.kalmanMatricesQuiz)
        self.placeBackButton(.05, .75, pane=self.visualizingPane,
                             text="KF Prediction", font=self.font, command = self.kalmanPrediction)

        pass

    def kalmanMatricesQuiz(self):
        quizPrompt = "Let's put the knowlege you learned to the test!\n" \
                     "Here are two questions to make sure you're understanding\n" \
                     "the material so far.\n\n"
        question1 = "1) Suppose we had a 5 element state, what might P look like?\n"
        question2 = "2) And H? Suppose we need three measurements"
        self.gui.clearScreen()
        self.makePanes()
        self.radioVarMovingAvgQ1.set(-1) # I think this makes it so that none are selected. Nice.
        self.radioVarMovingAvgQ2.set(-1) # I think this makes it so that none are selected. Nice.
        self.interactivePane.create_text(240, 60, text = quizPrompt, font = self.font)

        # QUESTION 1
        self.interactivePane.create_text(240, 90, text=question1, font=self.font)
        self.visualizingPane.create_image(250, 250, image=self.quizQuestionMark, anchor=tk.CENTER)
        A1 = tk.Radiobutton(self.interactivePane, text="A) [10 0 0 0 0]\n"
                                                        "   [0 10 0 0 0]\n"
                                                        "   [0 0 10 0 0]\n"
                                                        "   [0 0 0 10 0]\n"
                                                        "   [0 0 0 0 10]",
                            padx=20, value = "A1", bg = "grey", variable = self.radioVarMovingAvgQ1)
        A1.place(relx = .01, rely = .2)
        B1 = tk.Radiobutton(self.interactivePane, text="B) [100 0]\n"
                                                        "   [0 100]",
                            padx=20, value = "B1", bg = "grey", variable = self.radioVarMovingAvgQ1)
        B1.place(relx = .01, rely = .4)
        C1 = tk.Radiobutton(self.interactivePane, text="C) [100 0 0]\n"
                                                        "   [0 100 0]\n"
                                                        "   [0 0 100]",
                            padx=20, value = "C1", bg = "grey", variable = self.radioVarMovingAvgQ1)
        C1.place(relx = .01, rely = .5)

        #
        # # QUESTION 2
        self.interactivePane.create_text(190, 320, text=question2, font=self.font)
        A2 = tk.Radiobutton(self.interactivePane, text="A) [0 1 1 1 0]",
                            padx=20, value="A2", bg="grey", variable=self.radioVarMovingAvgQ2)
        A2.place(relx=.01, rely=.65)
        B2 = tk.Radiobutton(self.interactivePane, text="B) [0 1 1 0 0]\n"
                                                       "   [0 0 0 1 0]",
                            padx=20, value="B2", bg="grey", variable=self.radioVarMovingAvgQ2)
        B2.place(relx=.01, rely=.7)
        C2 = tk.Radiobutton(self.interactivePane, text="C) [0 1 0 0 0]\n"
                                                       "   [0 0 1 0 0]\n"
                                                       "   [0 0 0 1 0]",
                            padx=20, value="C2", bg="grey", variable=self.radioVarMovingAvgQ2)
        C2.place(relx=.01, rely=.8)
        correctAnswers = [[self.radioVarMovingAvgQ1, "A1"],[self.radioVarMovingAvgQ2, "C2"]]
        self.placeBackToMenuButton(self.visualizingPane)
        self.placeNextButton(.675, .75, pane=self.visualizingPane,
                             text="Submit Quiz", font=self.font, command=lambda: self.checkTest(correctAnswers))
        self.placeBackButton(.05, .75, pane=self.visualizingPane, command=self.kalmanMeasureAndUpdate,
                             text="", font=self.font)

    def formKalmanFMatrix(self):
        self.gui.clearScreen()
        self.makePanes()
        assignmentExplanation =       "It's time to practice! In the pages that follow,\n" \
                                      "you will fill in each of the matrices in the Kalman Filter. The\n" \
                                      "noise matrices P, Q, and R, have been done for you. When \n" \
                                      "you think you've got it right, go ahead and hit the 'Check my \n" \
                                      "work! button, and if your matrix looks good, you can move on,\n" \
                                      "otherwise, you'll have to try again! Take a look at the image\n" \
                                      "on the right if you need a refresher!\n" \
                                      " We'll start with the F matrix. Assume that our state is: \n" \
                                      "                             [X]\n" \
                                      "                             [v]\n" \
                                      "and our state transition equation is: X_n+1 = X_n + v*dt "
        self.interactivePane.create_text(260, 150, text = assignmentExplanation, font = self.font)
        # make the table
        tableCanvas = tk.Canvas(self.interactivePane, bg="white", width=400, height=200)
        tableCanvas.place(relx=.5, rely=.6, anchor=tk.CENTER)
        numRows = 2
        numCols = 2
        for i in range(numRows):  # Rows
            for j in range(numCols):  # Columns
                # populate measurements
                b = tk.Entry(tableCanvas, text="", width=10)
                b.grid(row=i, column=j)
        pass
        self.interactivePane.create_text(170, 300, text = "F = ", font = self.font)
        checkAssignmentButton = tk.Button(self.interactivePane, text = "Check my work!",
                                          command = lambda:
                                          self.checkMatrix(tableCanvas, self.F, rows = 2, columns = 2,
                                                           nextPage = self.formKalmanHMatrix))
        checkAssignmentButton.place(relx = .5, rely = .7, anchor = tk.CENTER)

    def formKalmanHMatrix(self):
        self.gui.clearScreen()
        self.makePanes()
        assignmentExplanation =       "Now we'll try the H matrix. In this case, we will\n" \
                                      "be measuring the position using a GPS. When you \n" \
                                      "think you've got it right, go ahead and hit the 'Check my \n" \
                                      "work! button, and if your matrix looks good, you can move on,\n" \
                                      "otherwise, you'll have to try again! Take a look at the image\n" \
                                      "on the right if you need a refresher!\n "

        self.interactivePane.create_text(260, 150, text = assignmentExplanation, font = self.font)
        # make the table
        tableCanvas = tk.Canvas(self.interactivePane, bg="white", width=400, height=200)
        tableCanvas.place(relx=.5, rely=.5, anchor=tk.CENTER)
        numRows = 1
        numCols = 2
        for i in range(numRows):  # Rows
            for j in range(numCols):  # Columns
                # populate measurements
                b = tk.Entry(tableCanvas, text="", width=10)
                b.grid(row=i, column=j)
        pass
        self.interactivePane.create_text(175, 250, text = "H = ", font = self.font)
        checkAssignmentButton = tk.Button(self.interactivePane, text = "Check my work!",
                                          command = lambda:
                                          self.checkMatrix(tableCanvas, self.H, rows = 1,
                                                           columns = 2, nextPage=self.formKalmanXMatrix))
        checkAssignmentButton.place(relx = .5, rely = .55, anchor = tk.CENTER)

    def formKalmanXMatrix(self):
        self.gui.clearScreen()
        self.makePanes()
        assignmentExplanation =       "Good Job! Now let's do the state vector. In this case, we \n" \
                                      "can assume we start at X = 0, v = 0. When you think you've \n " \
                                      "got it right, go ahead and hit the 'Check my work! button, \n" \
                                      "and if your matrix looks good you can move on, otherwise, \n" \
                                      "you'll have to try again! Take a look at the image on the right \n" \
                                      "if you need a refresher!\n "

        self.interactivePane.create_text(260, 150, text = assignmentExplanation, font = self.font)
        # make the table
        tableCanvas = tk.Canvas(self.interactivePane, bg="white", width=400, height=200)
        tableCanvas.place(relx=.5, rely=.5, anchor=tk.CENTER)
        numRows = 2
        numCols = 1
        for i in range(numRows):  # Rows
            for j in range(numCols):  # Columns
                # populate measurements
                b = tk.Entry(tableCanvas, text="", width=10)
                b.grid(row=i, column=j)
        pass
        self.interactivePane.create_text(200, 250, text = "x = ", font = self.font)
        checkAssignmentButton = tk.Button(self.interactivePane, text = "Check my work!",
                                          command = lambda:
                                          self.checkMatrix(tableCanvas, self.x, rows = 2,
                                                           columns = 1, nextPage=self.runKalmanFilter))
        checkAssignmentButton.place(relx = .5, rely = .58, anchor = tk.CENTER)

    def runKalmanFilter(self):
        self.gui.clearScreen()
        self.makePanes()
        self.placeBackToMenuButton(self.visualizingPane)
        dataPoints = 100
        self.xData = [i for i in range(dataPoints)]
        noise = [random.randint(-100,100)/1500 for i in range(dataPoints)]
        self.xMeasurements = [a + b for a, b in zip(self.xData, noise)]
        aboutKalmanGain = "We're ready to put it all together. So, what have\n" \
                          "we learned? Well, we've learned about the moving\n" \
                          "average, which constantly calculates an average\n" \
                          "of the last n points, and uses that as a measurement.\n" \
                          "We've learned that unlike the moving average, the \n" \
                          "Kalman Filter (KF), estimates the future state of \n" \
                          "the system, and computes a Kalman Gain, K, to weigh\n" \
                          "old and new measurements. Furthermore, we've learned\n" \
                          "about the daunting matrices in a kalman filter, and \n" \
                          "formed them. Now, it's time to see the kalman filter\n" \
                          "in action! Go ahead and push the plot button when you're\n" \
                          "ready. Good job on completing this module!"

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
        run = tk.Button(self.interactivePane, text = "Run Kalman Filter!",command = lambda:self.startKalmanFilterAni(self.xMeasurements))
        run.place(relx = .5, rely = .64, anchor = tk.CENTER)
        self.mainModule.completed = True
        self.placeNextButton(.7, .75, pane=self.interactivePane,
                             text="You did it!", font=self.font, command=self.gui.HomePage)
        self.placeBackButton(.05, .75, pane=self.interactivePane,
                             text="Take me back!", font=self.font, command=self.formKalmanXMatrix)
        pass

################### MISC
        # Pass the list containing the correct answer objects (multiple choice)
    def checkTest(self, correctAnswers):
            for answer in correctAnswers:
                if (answer[0].get() == answer[1]):
                    pass
                else:
                    print("Quiz Failed.")
                    self.quizFailed(self.kalmanMatricesQuiz)
                    return
            print("Quiz Passed.")
            self.quizPassed(self.mainModule.kalmanFilter.formKalmanFMatrix)


    def quizPassed(self, nextPage):
        self.gui.clearScreen()
        canvas = tk.Canvas(self.gui.win, width=1000, height=500, bg='grey')
        canvas.grid(row=0, column=0)
        canvas.create_image(500, 250, image=self.quizPassedImage, anchor=tk.CENTER)
        canvas.create_text(500, 50, text="Quiz Passed!", font=self.quizResultFont)
        self.placeBackToMenuButton(canvas)
        self.placeNextButton(.7, .7, pane=canvas, command=nextPage, text="Next Topic!",
                             font=self.font)

    def quizFailed(self, previousPage):
        self.gui.clearScreen()
        canvas = tk.Canvas(self.gui.win, width=1000, height=500, bg='grey')
        canvas.grid(row=0, column=0)
        canvas.create_image(500, 250, image=self.quizFailedImage, anchor=tk.CENTER)
        canvas.create_text(500, 50, text="Quiz Failed!", font=self.quizResultFont)
        self.placeBackToMenuButton(canvas)
        self.placeBackButton(.1, .7, pane=canvas, command=previousPage, text="To Quiz",
                             font=self.font)
    def checkMatrix(self, table, trueMatrix, rows, columns, nextPage):
        for i in range(rows):
            for j in range(columns):
                value = table.grid_slaves(row=i, column=j)[0].get()
                if(value == ''):
                    value = 0
                elif(value == 'dt' or value == 't'):
                    value = self.dt_sec
                if(float(value) != trueMatrix[i,j]):
                    print(table.grid_slaves(row=i, column=j)[0].get(), trueMatrix[i,j])
                    return False
        print("YES")
        self.placeNextButton(.7, .75, pane=self.interactivePane,
                             text="You got it!", font=self.font, command=nextPage)
        return True

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

    def predict(self):
        # Predict next x
        self.x = self.F * self.x

        # Update uncertainty matrix
        self.P = self.F * self.P * np.transpose(self.F) + self.Q

    def measureAndUpdate(self, measurements):
        # Equations for kalman filter
        Z = np.matrix(measurements)
        y = np.transpose(Z) - self.H * self.x
        S = self.H * self.P * np.transpose(self.H) + self.R
        K = self.P * np.transpose(self.H) * np.linalg.inv(S)
        self.x = self.x + K * y
        self.P = (self.I - K * self.H) * self.P

    def startKalmanFilterAni(self, measurements):
        self.plotIterator = 0
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
        del self.kalmanXError[:]
        del self.kalmanVError[:]
        for i in range(len(measurements)):
            self.predict()
            self.measureAndUpdate(measurements[i])
            self.kalmanXError.append(self.x[0,0] - self.xData[i])
            self.kalmanVError.append(self.x[1, 0] - 1/self.dt_sec)
        self.ani = animation.FuncAnimation(f, self.moveCarKalmanFilter, interval=self.dt_sec*1000)

    def moveCarKalmanFilter(self, event):
        self.carAxisKF.clear()
        self.carAxisKF.set_ylim([0, 5])
        self.carAxisKF.set_xlim([0, len(self.xData) + 2])
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
        self.drawCar(self.xData[self.plotIterator], 1.5, self.carAxisKF)
        # plot the moving average here, y stays the same
        if (self.plotIterator >= 2):
            # plots moving average data
            self.xPosErrorKF.plot(self.xData[0:self.plotIterator - 1],
                                  self.kalmanXError[0:self.plotIterator - 1],
                                  marker='o', markersize=1.0, color='b')
            self.vErrorKF.plot(self.xData[0:self.plotIterator - 1],
                               self.kalmanVError[0:self.plotIterator - 1],
                               marker='o', markersize=1.0, color='b')

        self.plotIterator = self.plotIterator + 1

        if (self.plotIterator > len(self.xData) - 1):
            self.ani.event_source.stop()
            self.placeBackToMenuButton(self.visualizingPane)