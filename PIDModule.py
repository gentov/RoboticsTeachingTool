from Module import *
import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import matplotlib.animation as animation
import matplotlib.patches as patches
from SimpleDrone import *
import textwrap
import numpy as np
import math
from matplotlib.animation import FuncAnimation


class PIDModule(Module):
    def __init__(self, gui=None, title=None):
        self.cpl = 50  # char per line
        super(PIDModule, self).__init__(gui=gui, title=title)
        self.pidGraph = tk.PhotoImage(file="images/pidgraph.png")
        self.pGraph = tk.PhotoImage(file="images/pController.png")
        self.motionImage = tk.PhotoImage(file="images/drawingRobot.png")
        self.controlSysDiagImage = tk.PhotoImage(file="images/controlSystemDiagram.png")
        self.stepResponseImage = tk.PhotoImage(file="images/stepresponse.png")
        self.kpLabel = None
        self.kdLabel = None
        self.kiLabel = None

        self.kpEntry = None
        self.kdEntry = None
        self.kiEntry = None

        self.kp = 1
        self.kd = 0
        self.ki = 0.0000

        self.eint = 0
        self.qd = 25
        self.totalError = 0
        self.prevError = 0
        self.prevTime = 0
        self.dt = .1
        self.totalTime = 10
        self.current = 0
        self.xData = np.linspace(0,self.totalTime,np.floor(self.totalTime/self.dt))
        self.yData = []
        self.fig = None
        self.line = None
        self.ax = None
        self.drone = SimpleDrone(.1, 0)
        self.qprev = self.drone.pos
        self.quizResultFont = ('Comic Sans MS', 15, 'bold italic')

        self.drone = SimpleDrone(.2, 0)
        self.axis = None
        self.signalGraph = None
        self.droneGraph = None
        self.runButton = None
        self.plotIterator = 0
        # self.xData = []
        # self.yMovingAvgData = []
        self.yData = [5.5, 6.25, 5.25, 5.5, 5.75, 4.75, 5.25, 5.75]
        self.font = ('Comic Sans MS', 11)
        self.radioVarControlQ1 = tk.StringVar()
        self.radioVarControlQ2 = tk.StringVar()
        self.quizQuestionMark = tk.PhotoImage(file="images/quizQuestionMark.png")
        self.quizPassedImage = tk.PhotoImage(file="images/passedQuiz.png")
        self.quizFailedImage = tk.PhotoImage(file="images/failedQuiz.png")

    def introPage(self):
        self.gui.clearScreen()
        self.makePanes()
        font = ('Comic Sans MS', 11, 'bold italic')
        self.placeNextButton(.7, .7, pane=self.interactivePane,
                             text="Motion", font=font, command=self.dronePID)
        self.placeBackButton(.1, .7, pane=self.interactivePane, command=self.gui.HomePage,
                             text="Main Menu", font=font)
        paragraph = "Let’s talk about control. You want to be able to control the motion of any system you create. " \
                    "There are quite a few control strategies that can be used depending on the application such as " \
                    "motion control, impedance control, force control. Let’s go over what each of these are. "
        formattedPara = self.formatParagraph(paragraph, self.cpl)
        self.visualizingPane.create_image(300, 250, image=self.pidGraph, anchor=tk.CENTER)
        self.animateText(250, 150, formattedPara, self.interactivePane, font)

    def motionControl(self):
        self.gui.clearScreen()
        self.makePanes()
        font = ('Comic Sans MS', 11, 'bold italic')
        self.placeNextButton(.7, .7, pane=self.interactivePane,
                             text="Force", font=font, command=self.forceControl)
        self.placeBackButton(.1, .7, pane=self.interactivePane, command=self.introPage,
                             text="Back", font=font)
        paragraph = "If you’re only interested in the trajectories that your robot takes, you’ll want motion control. " \
                    "With this type of controller, you’re most likely going to want to specify either the position, " \
                    "velocity, or acceleration of the robot at any given point in time. For example, if you had a " \
                    "manipulator that needed to draw something, you would have to specify the positions at a given " \
                    "time to make it draw the shape. "
        formattedPara = self.formatParagraph(paragraph, self.cpl)
        self.visualizingPane.create_image(300, 250, image=self.motionImage, anchor=tk.CENTER)
        self.animateText(250, 150, formattedPara, self.interactivePane, font)

    def forceControl(self):
        self.gui.clearScreen()
        self.makePanes()
        font = ('Comic Sans MS', 11, 'bold italic')
        self.placeNextButton(.7, .7, pane=self.interactivePane,
                             text="Let's go!", font=font, command=self.impedanceControl)
        self.placeBackButton(.1, .7, pane=self.interactivePane, command=self.motionControl,
                             text="Back", font=font)
        paragraph = "Force controllers on the other hand would be used to do things like manipulating objects. It is " \
                    "used to control the force your robot exerts on the environment." \
                    "Typically the force is measured using sensors like an FSR (Force Strain Resistor) or by " \
                    "measuring the current draw at each actuator. For " \
                    "example, if a robot was assembling something fragile in an assembly line. It should be as gentle " \
                    "as it needs to be, but use enough force to do the task. "
        formattedPara = self.formatParagraph(paragraph, self.cpl)

        self.visualizingPane.create_image(300, 250, image=self.pidGraph, anchor=tk.CENTER)
        self.animateText(250, 150, formattedPara, self.interactivePane, font)

    def impedanceControl(self):
        self.gui.clearScreen()
        self.makePanes()
        font = ('Comic Sans MS', 11, 'bold italic')
        self.placeNextButton(.7, .7, pane=self.interactivePane,
                             text="Quiz time", font=font, command=self.controlTypeQuiz)
        self.placeBackButton(.1, .7, pane=self.interactivePane, command=self.forceControl,
                             text="Back", font=font)

        paragraph = "Unlike force controllers, impedance controllers are more concerned with controlling the dynamics " \
                    "of contact between the robot and the environment. The goal is to change the motion as a function " \
                    "of external forces. So if your robot makes unexpected contact with " \
                    "something, it becomes compliant and causes little to no damage. This can be done programmatically " \
                    "using some complex math or with specialty compliant actuators. "
        formattedPara = self.formatParagraph(paragraph, self.cpl)
        self.visualizingPane.create_image(300, 250, image=self.pidGraph, anchor=tk.CENTER)
        self.animateText(250, 150, formattedPara, self.interactivePane, font)

    def controlTypeQuiz(self):
        quizPrompt = "Here's a quick couple of questions to make sure\n" \
                     "you're following along.\n\n"
        question1 = "1) A robot arm is swinging quickly across the workspace and\n" \
                    "a human operator steps in its path. The operator feels a gentle\n" \
                    "touch as the arm touches makes contact with him.\n" \
                    "What controller was the arm using most likely?\n"
        question2 = "2) Your manipulator must conduct for an orchestra, which\n" \
                    "type of control should you use?\n"
        self.gui.clearScreen()
        self.makePanes()
        self.radioVarControlQ1.set(-1)  # I think this makes it so that none are selected. Nice.
        self.radioVarControlQ2.set(-1)  # I think this makes it so that none are selected. Nice.
        self.interactivePane.create_text(260, 50, text=quizPrompt, font=self.font)

        self.visualizingPane.create_image(250, 250, image=self.quizQuestionMark, anchor=tk.CENTER)

        # QUESTION 1
        self.interactivePane.create_text(250, 120, text=question1, font=self.font)
        A1 = tk.Radiobutton(self.interactivePane, text="A) Motion",
                            padx=20, value="A1", bg="grey", variable=self.radioVarControlQ1)
        A1.place(relx=.1, rely=.3)
        B1 = tk.Radiobutton(self.interactivePane, text="B) Force ",
                            padx=20, value="B1", bg="grey", variable=self.radioVarControlQ1)
        B1.place(relx=.1, rely=.35)
        C1 = tk.Radiobutton(self.interactivePane, text="C) Impedance",
                            padx=20, value="C1", bg="grey", variable=self.radioVarControlQ1)
        C1.place(relx=.1, rely=.4)

        # QUESTION 2
        self.interactivePane.create_text(250, 265, text=question2, font=self.font)
        A2 = tk.Radiobutton(self.interactivePane, text="A) Motion",
                            padx=20, value="A2", bg="grey", variable=self.radioVarControlQ2)
        A2.place(relx=.1, rely=.55)
        B2 = tk.Radiobutton(self.interactivePane, text="B) Force",
                            padx=20, value="B2", bg="grey", variable=self.radioVarControlQ2)
        B2.place(relx=.1, rely=.6)
        C2 = tk.Radiobutton(self.interactivePane, text="C) Impedance",
                            padx=20, value="C2", bg="grey", variable=self.radioVarControlQ2)
        C2.place(relx=.1, rely=.65)
        correctAnswers = [[self.radioVarControlQ1, "C1"], [self.radioVarControlQ2, "A2"]]
        self.placeBackToMenuButton(self.visualizingPane)
        self.placeNextButton(.675, .75, pane=self.interactivePane,
                             text="Submit Quiz", font=self.font,
                             command=lambda: self.checkTest(correctAnswers, self.explainPID, self.controlBlockDiagrams))
        self.placeBackButton(.075, .75, pane=self.interactivePane, command=self.gui.HomePage,
                             text="", font=self.font)

    def controlBlockDiagrams(self):
        self.gui.clearScreen()
        self.makePanes()
        font = ('Comic Sans MS', 11, 'bold italic')
        self.placeNextButton(.7, .7, pane=self.interactivePane,
                             text="Step Response", font=font, command=self.stepResponse)
        self.placeBackButton(.1, .7, pane=self.interactivePane, command=self.gui.HomePage,
                             text="Back", font=font)

        paragraph = "Control system block diagrams are an easy and intuitive way to understand how a system works. In " \
                    "the figure you can see blocks connected by arrows. The arrow represents the flow of information " \
                    "in the system and each block represents a function. In this simple generic block diagram you can " \
                    "see that the input enters the controller, which outputs the inputs to the actuators. The change " \
                    "in the environment is measured by sensors and used by the controller. The circles are junctions " \
                    "that show how the intersecting signals interact. For example if the sensors are measuring the " \
                    "current position, then you can subtract it from the position before the controller to get the " \
                    "error."
        formattedPara = self.formatParagraph(paragraph, self.cpl)
        self.visualizingPane.create_image(300, 250, image=self.controlSysDiagImage, anchor=tk.CENTER)
        self.animateText(250, 150, formattedPara, self.interactivePane, font)

    def stepResponse(self):
        self.gui.clearScreen()
        self.makePanes()
        font = ('Comic Sans MS', 11, 'bold italic')
        self.placeNextButton(.7, .7, pane=self.interactivePane,
                             text="Quiz time", font=font, command=self.explainPIDControl)
        self.placeBackButton(.1, .7, pane=self.interactivePane, command=self.controlBlockDiagrams,
                             text="Back", font=font)

        paragraph = "When we look at these controllers, we want to bring the error down to 0 and reach a desired " \
                    "response. While there are many different types of signal responses we will only be covering step " \
                    "response in this module." \
                    "When you look at a step response, you'll want to look for a few characteristics. Rise time is " \
                    "the time that it takes the error to reach 0 from the starting error. Overshoot is a measure of " \
                    "how much the system overcompensates after reaching the setpoint." \
                    "And settling time is the time it takes for the amplitude to start " \
                    "staying within a threshold of the setpoint. Generally you want the rise time and the settling " \
                    "time to be very fast " \
                    "while also having as little overshoot as possible."

        formattedPara = self.formatParagraph(paragraph, self.cpl)
        self.visualizingPane.create_image(300, 250, image=self.stepResponseImage, anchor=tk.CENTER)
        self.animateText(250, 150, formattedPara, self.interactivePane, font)

    def checkTest(self, correctAnswers, previousPage, nextPage):
        for answer in correctAnswers:
            if (answer[0].get() == answer[1]):
                pass
            else:
                print("Quiz Failed.")
                self.quizFailed(previousPage)
                return
        print("Quiz Passed.")
        self.quizPassed(nextPage)
        pass

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

    def explainPIDControl(self):
        self.gui.clearScreen()
        self.makePanes()
        paragraph = "The PID controller equation can be expressed as\n" \
                    "the equation on the right. \n" \
                    "u is the controller output and \n" \
                    "each of the terms have a different\n" \
                    "effect on the output of the system.\n" \
                    "Let's take a look at the proportional term first.\n"
        font = ('Comic Sans MS', 11, 'bold italic')
        self.visualizingPane.create_image(300, 250, image=self.pidGraph, anchor=tk.CENTER)
        self.animateText(275, 150, paragraph, self.interactivePane, font)
        self.placeNextButton(.7, .7, pane=self.interactivePane,
                             text="Proportional\nTerm", font=font, command=self.explainP)
        self.placeBackButton(.1, .7, pane=self.interactivePane, command=self.explainPID,
                             text="Main Menu", font=font)

    def explainP(self):
        self.gui.clearScreen()
        self.makePanes()
        font = ('Comic Sans MS', 11, 'bold italic')
        self.placeNextButton(.7, .7, pane=self.interactivePane,
                             text="Integral\nterm", font=font, command=self.explainPI)
        self.placeBackButton(.1, .7, pane=self.interactivePane, command=self.explainPIDControl,
                             text="Main Menu", font=font)
        paragraph = "The proportional term is comprised of" \
                    "the error between the desired setpoint." \
                    "and the current position, and a constant gain," \
                    "Kp. This term is meant to close the distance" \
                    "to the setpoint quickly. So the larger the error" \
                    "the faster the rise time." \
                    "However, the problem with just P control, is that it requires an error to keep the response at a " \
                    "certain setpoint. Another way to look at this is that the proportional term is only concerned " \
                    "with the present. What if we also took the past into account?"
        formattedPara = self.formatParagraph(paragraph, self.cpl)
        self.visualizingPane.create_image(300, 250, image=self.pGraph, anchor=tk.CENTER)
        self.animateText(275, 200, formattedPara, self.interactivePane, font)

    def explainPI(self):
        self.gui.clearScreen()
        self.makePanes()
        font = ('Comic Sans MS', 11, 'bold italic')
        self.placeNextButton(.7, .7, pane=self.interactivePane,
                             text="Derivative\nterm", font=font, command=self.explainPID)
        self.placeBackButton(.1, .7, pane=self.interactivePane, command=self.explainP,
                             text="Main Menu", font=font)
        paragraph = "A solution to the steady-state error problem we mentioned before, we can incorporate past " \
                    "data. Let's say for example that we integrate the error from the start to the current time. " \
                    "Eventually, when the proportional term does not have enough of an error to power itself, " \
                    "the memory will keep the signal steady, instead of oscillating like a P controller does. " \
                    "This can have it's drawbacks though. If the system overshoots it will take a little longer " \
                    "for the system to correct and overtime with noise it could cause some instability as it " \
                    "drifts slowly from the set-point until the P term kicks back in. Let's see what else we can " \
                    "do to reduce the overshoot."
        formattedPara = self.formatParagraph(paragraph, self.cpl)
        self.visualizingPane.create_image(300, 250, image=self.pGraph, anchor=tk.CENTER)
        self.animateText(275, 200, formattedPara, self.interactivePane, font)

    def explainPID(self):
        self.gui.clearScreen()
        self.makePanes()
        font = ('Comic Sans MS', 11, 'bold italic')
        self.placeNextButton(.7, .7, pane=self.interactivePane,
                             text="Derivative\nterm", font=font, command=self.dronePID)
        self.placeBackButton(.1, .7, pane=self.interactivePane, command=self.explainPI,
                             text="Main Menu", font=font)
        paragraph = "To reduce the overshoot, let's try to predict the future error. We find the change in error " \
                    "between the current state and the last state and apply the difference to the controller output. " \
                    "Since the error velocity is decreasing, it will dampen the signal and if the constant Kd is " \
                    "tuned properly, it will reduce the overshoot almost completely."
        formattedPara = self.formatParagraph(paragraph, self.cpl)

        self.visualizingPane.create_image(300, 250, image=self.pGraph, anchor=tk.CENTER)
        self.animateText(275, 200, formattedPara, self.interactivePane, font)

    def dronePID(self):
        """
        Show response using graph when you set certain kp,kd,ki
        Visualizing pane: matplotlib of PID going to a setpoint
        interactive pane: Gain changing

        """
        quizPrompt = "Here's a quick couple of questions to make sure\n" \
                     "you're following along.\n\n"

        self.interactivePane.create_text(260, 50, text=quizPrompt, font=self.font)

        self.gui.clearScreen()
        self.makePanes()
        font = ('Comic Sans MS', 11, 'bold italic')
        self.placeNextButton(.7, .7, pane=self.interactivePane,
                             text="Quiz", font=font, command=self.explainP)
        self.placeBackButton(.1, .7, pane=self.interactivePane, command=self.explainPID,
                             text="Kd Term", font=font)
        paragraph = "Please select a Kp and click Run."
        formattedPara = self.formatParagraph(paragraph, self.cpl)


        self.kpLabel = tk.Label(self.interactivePane, text="KP:", font=('Comic Sans MS', 10, 'bold italic'))
        self.kiLabel = tk.Label(self.interactivePane, text="KI:", font=('Comic Sans MS', 10, 'bold italic'))
        self.kdLabel = tk.Label(self.interactivePane, text="KD:", font=('Comic Sans MS', 10, 'bold italic'))

        self.kpLabel.place(relx=.35, rely=.45, anchor='center')
        self.kiLabel.place(relx=.35, rely=.5, anchor='center')
        self.kdLabel.place(relx=.35, rely=.55, anchor='center')

        self.runButton = tk.Button(self.interactivePane, height=2, text="Run",
                                   font=('Comic Sans MS', 10, 'bold italic'), bg="white", command=self.runPID)
        self.runButton.place(relx=.55, rely=.65, anchor='center')

        kpText = tk.StringVar()
        kdText = tk.StringVar()
        kiText = tk.StringVar()
        #
        self.kpEntry = tk.Entry(self.interactivePane, command=self.setKP(), textvariable=kpText)
        self.kdEntry = tk.Entry(self.interactivePane, command=self.setKD(), textvariable=kdText)
        self.kiEntry = tk.Entry(self.interactivePane, command=self.setKI(), textvariable=kiText)
        self.kpEntry.place(relx=.55, rely=.45, anchor='center')
        self.kiEntry.place(relx=.55, rely=.5, anchor='center')
        self.kdEntry.place(relx=.55, rely=.55, anchor='center')

        # self.kpEntry.grid(row=0, column=1)
        # self.kdEntry.grid(row=1, column=1)
        # self.kiEntry.grid(row=2, column=1)

        ## Configure the Plot(s)
        self.f = Figure(figsize=(5, 5), dpi=100)
        self.f.subplots_adjust(hspace=.5)
        self.signalGraph = self.f.add_subplot(211)
        self.signalGraph.set_ylim([0, 30])
        self.signalGraph.set_xlim([0, self.totalTime])
        self.signalGraph.set_title("Drone Position vs Time")
        self.signalGraph.set_xlabel("Time (s)")
        self.signalGraph.set_ylabel("Y Position (m)")
        self.droneGraph = self.f.add_subplot(212)
        self.droneGraph.set_xlim([-10,10])
        self.droneGraph.set_ylim([0, 30])
        self.droneGraph.set_title("Drone Vertical Position")
        self.droneGraph.set_xlabel("X Position (m)")
        self.droneGraph.set_ylabel("Y Position (m)")
        figureCanvas = FigureCanvasTkAgg(self.f, master=self.visualizingPane)
        figureCanvas.get_tk_widget().grid(row=0, column=0)
        self.drawDrone(5, self.droneGraph)
        print("configured")
        self.animateText(275, 100, formattedPara, self.interactivePane, font)



    def drawDrone(self, y, axis):
        self.car = patches.Rectangle((-1, y), 2, 1, linewidth=1, edgecolor='black',
                                     facecolor='black')
        leftProp = patches.Rectangle((-1.5, y + 1), 1, .3, linewidth=1, edgecolor='black',
                                     facecolor='white')
        rightProp = patches.Rectangle((.5, y + 1), 1, .3, linewidth=1, edgecolor='black',
                                               facecolor='white')

        axis.add_patch(self.car)
        axis.add_patch(leftProp)
        axis.add_patch(rightProp)

    def runPlots(self, event):
        self.signalGraph.clear()
        self.droneGraph.clear()
        self.f = Figure(figsize=(5, 5), dpi=100)
        self.f.subplots_adjust(hspace=.5)
        self.signalGraph.set_ylim([0, 30])
        self.signalGraph.set_xlim([0, self.totalTime])
        self.signalGraph.set_title("Drone Position vs Time")
        self.signalGraph.set_xlabel("Time (s)")
        self.signalGraph.set_ylabel("Y Position (m)")
        self.droneGraph.set_xlim([-10, 10])
        self.droneGraph.set_ylim([0, 30])
        self.droneGraph.set_title("Drone Vertical Position")
        self.droneGraph.set_xlabel("X Position (m)")
        self.droneGraph.set_ylabel("Y Position (m)")

        self.drawDrone(self.yData[self.plotIterator], self.droneGraph)
        if (self.plotIterator >= 2):
            self.signalGraph.plot(self.xData[0:self.plotIterator - 1],
                                  self.yData[0:self.plotIterator - 1],
                                  linestyle='-', marker='o', markersize=1.0, color='b')

        self.plotIterator = self.plotIterator + 1

        if (self.plotIterator > len(self.xData) - 1):
            self.ani.event_source.stop()
            self.placeBackToMenuButton(self.visualizingPane)

    def PID(self):
        # Set desired velocity to zero
        qdotd = 0

        # Get current position
        q = self.drone.pos

        # calculate the derivative of position
        qdot = (q - self.qprev) / self.dt
        self.qprev = q

        # Calculate error from current position to desired position
        e = self.qd - q

        # Calculate difference between desired and current velocity
        edot = qdotd - qdot

        # Calculate integral of error
        self.eint = self.eint + e * self.dt

        # Create the output signal
        u = self.kp * e + self.kd * edot + self.ki * self.eint
        self.drone.fly(u,self.dt)

    def runPID(self):
        print("Running PID")
        self.f = Figure(figsize=(5, 5), dpi=100)
        self.f.subplots_adjust(hspace=.5)
        self.signalGraph = self.f.add_subplot(211)
        self.signalGraph.set_ylim([0, 30])
        self.signalGraph.set_xlim([0, self.totalTime])
        self.signalGraph.set_title("Drone Position vs Time")
        self.signalGraph.set_xlabel("Time (s)")
        self.signalGraph.set_ylabel("Y Position (m)")
        self.droneGraph = self.f.add_subplot(212)
        self.droneGraph.set_xlim([-10, 10])
        self.droneGraph.set_ylim([0, 30])
        self.droneGraph.set_title("Drone Vertical Position")
        self.droneGraph.set_xlabel("X Position (m)")
        self.droneGraph.set_ylabel("Y Position (m)")
        figureCanvas = FigureCanvasTkAgg(self.f, master=self.visualizingPane)
        figureCanvas.get_tk_widget().grid(row=0, column=0)
        # try:
        #     self.ani.event_source.stop()
        # except:
        #     pass
        del self.yData[:]
        for i in self.xData:
            self.PID()
            self.yData.append(self.drone.pos)
            #print(self.drone.pos)
        self.ani = animation.FuncAnimation(self.f, self.runPlots, interval=1)

    def runModule(self):
        self.gui.clearScreen()
        self.makePanes()
        self.introPage()

    def setKP(self):
        # self.kp = type(float(self.kpEntry.get()))
        print("set kp")

    def setKD(self):
        pass

    def setKI(self):
        pass

    def formatParagraph(self, paragraph, charsPerLine):
        unformattedText = textwrap.dedent(paragraph).strip()
        formattedText = textwrap.fill(unformattedText, width=charsPerLine)
        return formattedText
