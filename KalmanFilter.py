from Module import *
import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import matplotlib.animation as animation
from statistics import mean

class KalmanFilter(Module):
    def __init__(self, gui = None, title = None, mainModule = None):
        super(KalmanFilter, self).__init__(gui = gui, title = title)
        self.mainModule = mainModule
        self.bigFont = ('Comic Sans MS', 14, 'bold italic')
        self.font = ('Comic Sans MS', 11, 'bold italic')
        self.smallFont = ('Comic Sans MS', 9, 'bold italic')


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
                          "When a new measurement is made, the KF updates and corrects" \
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
                          "prediction step is the Q matrix. This matrix is our 'Process Noise\n" \
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
                             text="Quiz!", font=self.font, command = self.kalmanMeasureAndUpdate)
        self.placeBackButton(.05, .75, pane=self.visualizingPane,
                             text="KF Prediction", font=self.font, command = self.kalmanPrediction)

        pass




