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
        self.pidGraph = tk.PhotoImage(file="images/pidcontroller.png")
        self.pidEq = tk.PhotoImage(file="images/PIDEquation.png")
        self.pidControlBlock = tk.PhotoImage(file="images/pidcontrolblock.png")
        self.pGraph = tk.PhotoImage(file="images/proportionalController.png")
        self.piGraph = tk.PhotoImage(file="images/PI.png")
        self.motionImage = tk.PhotoImage(file="images/drawingRobot.png")
        self.complianceImage = tk.PhotoImage(file="images/impedance.png")
        self.forceImage = tk.PhotoImage(file="images/atluslift.png")
        self.controlSysDiagImage = tk.PhotoImage(file="images/controlSystemDiagram.png")
        self.stepResponseImage = tk.PhotoImage(file="images/stepresponse.png")
        self.simpBlocksImage = tk.PhotoImage(file="images/simplificationOfSysBlocks.png")
        self.simpBlockPracticeImage = tk.PhotoImage(file="images/simplifyPractice.png")
        self.passQuizSmall = tk.PhotoImage(file="images/passedQuizSmall.png")

        self.kpLabel = None
        self.kdLabel = None
        self.kiLabel = None

        self.kpEntry = None
        self.kdEntry = None
        self.kiEntry = None

        self.kp = 10
        self.kd = 0.5
        self.ki = 0.05

        self.qddes = 0
        self.eint = 0
        self.qd = 10
        self.totalError = 0
        self.prevError = 0
        self.prevTime = 0
        self.dt = .1
        self.totalTime = 1
        self.current = 0
        self.xData = np.linspace(0, self.totalTime, 100)
        self.yData = [0]
        self.fig = None
        self.line = None
        self.ax = None
        self.drone = SimpleDrone(.5, 0)
        self.qprev = self.drone.pos
        self.quizResultFont = ('Comic Sans MS', 15, 'bold italic')

        self.btnFont = ('Comic Sans MS', 11, 'bold italic')
        self.font = ('Comic Sans MS', 11)

        self.axis = None
        self.signalGraph = None
        self.droneGraph = None
        self.runButton = None
        self.suggestedGainsButton = None
        self.plotIterator = 0
        # self.xData = []

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
                             text="Motion", font=font, command=self.motionControl)
        self.placeBackButton(.1, .7, pane=self.interactivePane, command=self.gui.HomePage,
                             text="Main Menu", font=font)
        paragraph = "Let’s talk about control. You want to be able to control the motion of any system you create. " \
                    "There are quite a few control strategies that can be used depending on the application such as " \
                    "motion control, impedance control, force control. Let’s go over what each of these are. "
        formattedPara = self.formatParagraph(paragraph, self.cpl)
        self.visualizingPane.create_image(250, 250, image=self.pidGraph, anchor=tk.CENTER)
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

        self.visualizingPane.create_image(250, 250, image=self.forceImage, anchor=tk.CENTER)
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
        self.visualizingPane.create_image(250, 250, image=self.complianceImage, anchor=tk.CENTER)
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
        self.interactivePane.create_text(235, 265, text=question2, font=self.font)
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
                             command=lambda: self.checkTest(correctAnswers, self.controlTypeQuiz,
                                                            self.controlBlockDiagrams))
        self.placeBackButton(.075, .75, pane=self.interactivePane, command=self.impedanceControl,
                             text="", font=self.font)

    def controlBlockDiagrams(self):
        self.gui.clearScreen()
        self.makePanes()
        font = ('Comic Sans MS', 10, 'bold italic')
        self.placeNextButton(.7, .7, pane=self.interactivePane,
                             text="Step Response", font=font, command=self.simpBlockDiagrams)
        self.placeBackButton(.1, .7, pane=self.interactivePane, command=self.controlTypeQuiz,
                             text="Back", font=font)

        paragraph = "Control system block diagrams are an easy and intuitive way to understand how a system works. In " \
                    "the figure you can see blocks connected by arrows. The arrow represents the flow of information " \
                    "in the system and each block represents a function. In this simple generic block diagram you can " \
                    "see that the input enters the controller, which outputs the inputs to the actuators. The change " \
                    "in the environment is measured by sensors and used by the controller. The circles are junctions " \
                    "that show how the intersecting signals interact. For example if the sensors are measuring the " \
                    "current position, then you can subtract it from the position before the controller to get the " \
                    "error. If simplified this control block diagram can show the transfer function of the system. A " \
                    "transfer function is just a mathematical function that shows the output given an input."
        formattedPara = self.formatParagraph(paragraph, 55)
        self.visualizingPane.create_image(250, 250, image=self.controlSysDiagImage, anchor=tk.CENTER)
        self.animateText(250, 175, formattedPara, self.interactivePane, font)

    def simpBlockDiagrams(self):
        self.gui.clearScreen()
        self.makePanes()
        font = ('Comic Sans MS', 11, 'bold italic')
        self.placeNextButton(.7, .7, pane=self.interactivePane,
                             text="Step Response", font=font, command=self.stepResponse)
        self.placeBackButton(.1, .7, pane=self.interactivePane, command=self.gui.HomePage,
                             text="Block\nDiagram", font=font)
        paragraph = "Here's a brief guide on how to simplify these simple control block diagrams. Keep in mind " \
                    "this is in the frequency domain. So to find the transfer function in the time domain, " \
                    "you will need to take the inverse laplace transform of the transfer function. Two blocks in " \
                    "series can be simplified by just multiplying the contents of the block. To remove a feedback " \
                    "loop, you must use the equation G(s)/(1+G(s)*H(s)). In some cases, the feedback H(s) will " \
                    "just be an arrow, this is called Unity feedback and to simplify you treat H(s) as 1. Using " \
                    "this transfer function, you can find a lot of information about the system such as the rise " \
                    "time, percentage overshoot, etc."
        formattedPara = self.formatParagraph(paragraph, self.cpl)
        self.visualizingPane.create_image(250, 250, image=self.simpBlocksImage, anchor=tk.CENTER)
        self.animateText(250, 175, formattedPara, self.interactivePane, font)

    def stepResponse(self):
        self.gui.clearScreen()
        self.makePanes()
        font = ('Comic Sans MS', 10, 'bold italic')
        self.placeNextButton(.7, .7, pane=self.interactivePane,
                             text="Quiz", font=font, command=self.ControlQuiz)
        self.placeBackButton(.1, .7, pane=self.interactivePane, command=self.controlBlockDiagrams,
                             text="Block\nDiagram", font=font)

        paragraph = "When we look at these controllers, we want to bring the error down to 0 and reach a desired " \
                    "response. While there are many different types of signal responses we will only be covering step " \
                    "response in this module." \
                    "When you look at a step response, you'll want to look for a few characteristics. Rise time is " \
                    "the time that it takes the error to reach 0 from the starting error. Overshoot is a measure of " \
                    "how much the system overcompensates after reaching the setpoint." \
                    "And settling time is the time it takes for the amplitude to start " \
                    "staying within a threshold of the setpoint known as the error band. Generally you want the rise " \
                    "time and the settling " \
                    "time to be very fast " \
                    "while also having as little overshoot as possible."

        formattedPara = self.formatParagraph(paragraph, 55)
        self.visualizingPane.create_image(250, 250, image=self.stepResponseImage, anchor=tk.CENTER)
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

    def ControlQuiz(self):
        question1 = "1) What is the settling time in terms of signal response?"
        question2 = "2) What is the transfer function of the diagram on the right?"
        q2Formatted = self.formatParagraph(question2, self.cpl)
        self.gui.clearScreen()
        self.makePanes()
        self.radioVarControlQ1.set(-1)
        self.radioVarControlQ2.set(-1)
        self.visualizingPane.create_image(250, 250, image=self.simpBlockPracticeImage, anchor=tk.CENTER)

        # QUESTION 1
        self.interactivePane.create_text(230, 90, text=question1, font=self.font)
        A1 = tk.Radiobutton(self.interactivePane, text="A) The time taken to meet the setpoint initially.",
                            padx=2, value="A1", bg="grey", variable=self.radioVarControlQ1)
        A1.place(relx=.1, rely=.2)
        B1 = tk.Radiobutton(self.interactivePane, text="B) The time taken to completely reach the setpoint.",
                            padx=2, value="B1", bg="grey", variable=self.radioVarControlQ1)
        B1.place(relx=.1, rely=.25)
        C1 = tk.Radiobutton(self.interactivePane, text="C) The time taken to reach the error-band.",
                            padx=2, value="C1", bg="grey", variable=self.radioVarControlQ1)
        C1.place(relx=.1, rely=.3)

        # QUESTION 2
        self.interactivePane.create_text(210, 230, text=q2Formatted, font=self.font)
        A2 = tk.Radiobutton(self.interactivePane, text="A) 1/(s+4+K)",
                            padx=2, value="A2", bg="grey", variable=self.radioVarControlQ2)
        A2.place(relx=.1, rely=.45)
        B2 = tk.Radiobutton(self.interactivePane, text="B) s/(s+2+K)",
                            padx=2, value="B2", bg="grey", variable=self.radioVarControlQ2)
        B2.place(relx=.1, rely=.5)
        C2 = tk.Radiobutton(self.interactivePane, text="C) K/(s+4+K)",
                            padx=2, value="C2", bg="grey", variable=self.radioVarControlQ2)
        C2.place(relx=.1, rely=.55)
        correctAnswers = [[self.radioVarControlQ1, "C1"], [self.radioVarControlQ2, "C2"]]
        self.placeBackToMenuButton(self.visualizingPane)
        self.placeNextButton(.675, .75, pane=self.interactivePane,
                             text="Submit Quiz", font=self.font,
                             command=lambda: self.checkTest(correctAnswers, self.ControlQuiz, self.explainPIDControl))
        self.placeBackButton(.075, .75, pane=self.interactivePane, command=self.stepResponse,
                             text="", font=self.font)

    def explainPIDControl(self):
        self.gui.clearScreen()
        self.makePanes()
        paragraph = "PID control is a way to command a system to setpoints using error as feedback. It is very " \
                    "commonly used as it is simple and sufficient to command a robot to positions in most motion " \
                    "control problems. PID is short for Proportional Integral Derivative, which all process system " \
                    "error differently and add to create the control signal. The top image is the control block " \
                    "diagram and below is the PID equation. Let's look at the proportional term (Kp) first."
        formattedPara = self.formatParagraph(paragraph, self.cpl)
        font = ('Comic Sans MS', 11, 'bold italic')
        self.visualizingPane.create_image(250, 150, image=self.pidControlBlock, anchor=tk.CENTER)
        self.visualizingPane.create_image(250, 400, image=self.pidEq, anchor=tk.CENTER)
        self.animateText(250, 150, formattedPara, self.interactivePane, font)
        self.placeNextButton(.7, .7, pane=self.interactivePane,
                             text="Kp\nTerm", font=font, command=self.explainP)
        self.placeBackButton(.1, .7, pane=self.interactivePane, command=self.ControlQuiz,
                             text="Quiz", font=font)

    def explainP(self):
        self.gui.clearScreen()
        self.makePanes()
        font = ('Comic Sans MS', 11, 'bold italic')
        self.placeNextButton(.7, .7, pane=self.interactivePane,
                             text="Ki\nTerm", font=font, command=self.explainPI)
        self.placeBackButton(.1, .7, pane=self.interactivePane, command=self.explainPIDControl,
                             text="PID\nIntro", font=font)
        paragraph = "The proportional term is comprised of " \
                    "the error between the desired setpoint " \
                    "and the current position, and a constant gain," \
                    "Kp. This term is meant to close the distance " \
                    "to the setpoint quickly. So the larger the error " \
                    "the faster the rise time. " \
                    "However, the problem with just P control, is that it requires an error to keep the response at a " \
                    "certain setpoint. Another way to look at this is that the proportional term is only concerned " \
                    "with the present. What if we also took the past errors into account?"
        formattedPara = self.formatParagraph(paragraph, self.cpl)
        self.visualizingPane.create_image(250, 250, image=self.pGraph, anchor=tk.CENTER)
        self.animateText(250, 200, formattedPara, self.interactivePane, font)

    def explainPI(self):
        self.gui.clearScreen()
        self.makePanes()
        font = ('Comic Sans MS', 11, 'bold italic')
        self.placeNextButton(.7, .7, pane=self.interactivePane,
                             text="Kd\nTerm", font=font, command=self.explainPID)
        self.placeBackButton(.1, .7, pane=self.interactivePane, command=self.explainP,
                             text="Kp\nTerm", font=font)
        paragraph = "A solution to the steady-state error problem we mentioned before, we can incorporate past " \
                    "data. Let's say for example that we integrate the error from the start to the current time. " \
                    "Eventually, when the proportional term does not have enough of an error to power itself, " \
                    "the memory will keep the signal steady, instead of oscillating like a P controller does. " \
                    "This can have its drawbacks though. If the system overshoots it will take a little longer " \
                    "for the system to correct and over time with noise it could cause some instability as it " \
                    "drifts slowly from the set-point until the P term kicks back in. Let's see what else we can " \
                    "do to reduce the overshoot."
        formattedPara = self.formatParagraph(paragraph, self.cpl)
        self.visualizingPane.create_image(250, 250, image=self.piGraph, anchor=tk.CENTER)
        self.animateText(250, 200, formattedPara, self.interactivePane, font)

    def explainPID(self):
        self.gui.clearScreen()
        self.makePanes()
        font = ('Comic Sans MS', 11, 'bold italic')
        self.placeNextButton(.7, .7, pane=self.interactivePane,
                             text="Activity", font=font, command=self.dronePID)
        self.placeBackButton(.1, .7, pane=self.interactivePane, command=self.explainPI,
                             text="Ki\nTerm", font=font)
        paragraph = "To reduce the overshoot, let's try to predict the future error. We find the change in error " \
                    "between the current state and the last state and apply the difference to the controller output. " \
                    "Since the error velocity is decreasing, it will dampen the signal and if the constant Kd is " \
                    "tuned properly, it will reduce the overshoot almost completely."
        formattedPara = self.formatParagraph(paragraph, self.cpl)

        self.visualizingPane.create_image(250, 250, image=self.pidGraph, anchor=tk.CENTER)
        self.animateText(250, 200, formattedPara, self.interactivePane, font)

    def dronePID(self):
        """
        Show response using graph when you set certain kp,kd,ki
        Visualizing pane: matplotlib of PID going to a setpoint
        interactive pane: Gain changing

        """

        # self.interactivePane.create_text(260, 50, text=quizPrompt, font=self.font)

        self.gui.clearScreen()
        self.makePanes()
        font = ('Comic Sans MS', 11)
        self.placeNextButton(.7, .7, pane=self.interactivePane,
                             text="Quiz", font=font, command=self.PIDQuiz)
        self.placeBackButton(.1, .7, pane=self.interactivePane, command=self.explainPID,
                             text="Kd Term", font=font)
        paragraph = "Get this drone to hover at 10m. Try some Kp, Ki, " \
                    "and Kd values to best achieve this. Since it's a simulation you may even find that a well tuned " \
                    "P gain is all you need. First set the Kp gain value that oscillates consistently, then tune Ki " \
                    "and Kd. Be careful with Ki, it should be very small if anything. Kd should be larger than Ki but " \
                    "still much smaller than Kp. Please hit the run button to test. Try the suggested " \
                    "gains button if you're stuck. "
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

        self.suggestedGainsButton = tk.Button(self.interactivePane, height=2, width=7, text="Suggested\nGains",
                                              font=('Comic Sans MS', 10, 'bold italic'), bg="white",
                                              command=self.setSuggestedGains)
        self.suggestedGainsButton.place(relx=.80, rely=.65, anchor='center')

        self.kpText = tk.StringVar()
        self.kdText = tk.StringVar()
        self.kiText = tk.StringVar()

        self.kpText.set(0)
        self.kdText.set(0)
        self.kiText.set(0)
        #
        self.kpEntry = tk.Entry(self.interactivePane, textvariable=self.kpText)
        self.kdEntry = tk.Entry(self.interactivePane, textvariable=self.kdText)
        self.kiEntry = tk.Entry(self.interactivePane, textvariable=self.kiText)
        self.kpEntry.place(relx=.55, rely=.45, anchor='center')
        self.kiEntry.place(relx=.55, rely=.5, anchor='center')
        self.kdEntry.place(relx=.55, rely=.55, anchor='center')

        ## Configure the Plot(s)
        self.f = Figure(figsize=(5, 5), dpi=100)
        self.f.subplots_adjust(hspace=.5)
        self.signalGraph = self.f.add_subplot(211)
        # self.signalGraph.set_ylim([0, 30])
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
        self.drawDrone(5, self.droneGraph)
        print("configured")
        self.animateText(250, 120, formattedPara, self.interactivePane, font)

    def drawDrone(self, y, axis):
        self.dronePic = patches.Rectangle((-1, y), 2, 1, linewidth=1, edgecolor='black',
                                          facecolor='black')
        leftProp = patches.Rectangle((-1.5, y + 1), 1, .3, linewidth=1, edgecolor='black',
                                     facecolor='white')
        rightProp = patches.Rectangle((.5, y + 1), 1, .3, linewidth=1, edgecolor='black',
                                      facecolor='white')

        axis.add_patch(self.dronePic)
        axis.add_patch(leftProp)
        axis.add_patch(rightProp)

    def runPID(self):
        print("Running PID")
        try:
            self.kp = float(self.kpText.get())
        except:
            self.kp = 0
            self.kpText.set("0")

        try:
            self.kd = float(self.kdText.get())
        except:
            self.kd = 0
            self.kdText.set("0")

        try:
            self.ki = float(self.kiText.get())
        except:
            self.ki = 0
            self.kiText.set("0")
        self.eint = 0
        self.qd = 10
        self.totalError = 0
        self.prevError = 0
        self.prevTime = 0
        self.drone.pos = 0
        self.qprev = self.drone.pos
        print(self.kp)
        print(self.ki)
        print(self.kd)
        self.plotIterator = 0
        self.f = Figure(figsize=(5, 5), dpi=100)
        self.f.subplots_adjust(hspace=.5)
        self.signalGraph = self.f.add_subplot(211)
        # self.signalGraph.set_ylim([0, 15])
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
        try:
            self.ani.event_source.stop()
        except:
            pass
        del self.yData[1:]
        print(self.yData)
        for i in self.xData:
            self.PID()
            self.yData.append(self.drone.pos)
            # print(self.drone.pos)
        self.ani = animation.FuncAnimation(self.f, self.runPlots, interval=1)

    def runPlots(self, event):
        self.signalGraph.clear()
        self.droneGraph.clear()
        self.f = Figure(figsize=(5, 5), dpi=100)
        self.f.subplots_adjust(hspace=.5)
        # self.signalGraph.set_ylim([0, 30])
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
            if (self.checkRight()):
                self.visualizingPane.create_image(300, 250, image=self.quizPassedImage, anchor=tk.CENTER)
                mainMenuButton = tk.Button(self.visualizingPane, relief=tk.FLAT)
                mainMenuButton.config(image=self.passQuizSmall, compound='center')
                mainMenuButton.place(relx=.87, rely=.025)
            else:
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
        self.drone.fly(u, self.dt)

    def PIDQuiz(self):
        quizPrompt = "The Final Quiz!"
        question1 = "1) What is the purpose of Ki in a PID system?"
        question2 = "2) You hold a drone down to the ground as you tell it to fly to a setpoint with PID control. It " \
                    "spins it's propellers faster and faster until you let it go and it and it zips up in the air and " \
                    "overshoots dramatically. What most likely happened? "
        q2Formatted = self.formatParagraph(question2, self.cpl)
        self.gui.clearScreen()
        self.makePanes()
        self.radioVarControlQ1.set(-1)
        self.radioVarControlQ2.set(-1)
        self.interactivePane.create_text(250, 50, text=quizPrompt, font=self.font)

        self.visualizingPane.create_image(250, 250, image=self.quizQuestionMark, anchor=tk.CENTER)

        # QUESTION 1
        self.interactivePane.create_text(240, 90, text=question1, font=self.font)
        A1 = tk.Radiobutton(self.interactivePane, text="A) To add stability",
                            padx=20, value="A1", bg="grey", variable=self.radioVarControlQ1)
        A1.place(relx=.1, rely=.2)
        B1 = tk.Radiobutton(self.interactivePane, text="B) To reduce steady-state error",
                            padx=20, value="B1", bg="grey", variable=self.radioVarControlQ1)
        B1.place(relx=.1, rely=.25)
        C1 = tk.Radiobutton(self.interactivePane, text="C) To increase speed",
                            padx=20, value="C1", bg="grey", variable=self.radioVarControlQ1)
        C1.place(relx=.1, rely=.3)

        # QUESTION 2
        self.interactivePane.create_text(250, 230, text=q2Formatted, font=self.font)
        A2 = tk.Radiobutton(self.interactivePane, text="A) Too much error accumulated in Integral term",
                            padx=20, value="A2", bg="grey", variable=self.radioVarControlQ2)
        A2.place(relx=.1, rely=.6)
        B2 = tk.Radiobutton(self.interactivePane, text="B) The Kd gain wasn't high enough",
                            padx=20, value="B2", bg="grey", variable=self.radioVarControlQ2)
        B2.place(relx=.1, rely=.65)
        C2 = tk.Radiobutton(self.interactivePane, text="C) The Kp gain was too high",
                            padx=20, value="C2", bg="grey", variable=self.radioVarControlQ2)
        C2.place(relx=.1, rely=.70)
        correctAnswers = [[self.radioVarControlQ1, "B1"], [self.radioVarControlQ2, "A2"]]
        self.placeBackToMenuButton(self.visualizingPane)
        self.placeNextButton(.675, .75, pane=self.interactivePane,
                             text="Submit Quiz", font=self.font,
                             command=lambda: self.checkTestLast(correctAnswers, self.PIDQuiz, self.gui.HomePage))
        self.placeBackButton(.075, .75, pane=self.interactivePane, command=self.dronePID,
                             text="Drone", font=self.font)

    def checkTestLast(self, correctAnswers, previousPage, nextPage):
        for answer in correctAnswers:
            if (answer[0].get() == answer[1]):
                pass
            else:
                print("Quiz Failed.")
                self.quizFailed(previousPage)
                return
        print("Quiz Passed.")
        self.quizPassedLast(nextPage)
        pass

    def quizPassedLast(self, nextPage):
        self.completed = True
        self.gui.clearScreen()
        canvas = tk.Canvas(self.gui.win, width=1000, height=500, bg='grey')
        canvas.grid(row=0, column=0)
        canvas.create_image(500, 250, image=self.quizPassedImage, anchor=tk.CENTER)
        canvas.create_text(500, 50, text="Quiz Passed!", font=self.quizResultFont)
        self.placeBackToMenuButton(canvas)
        self.placeNextButton(.7, .7, pane=canvas, command=nextPage, text="Home",
                             font=self.font)

    def runModule(self):
        self.gui.clearScreen()
        self.makePanes()
        self.introPage()

    def checkRight(self):
        if (self.drone.pos > 9.5) and (self.drone.pos < 10.5):
            return True
        else:
            return False

    def setSuggestedGains(self):
        self.kpText.set("10")
        self.kdText.set(".2")
        self.kiText.set(".05")

    def formatParagraph(self, paragraph, charsPerLine):
        unformattedText = textwrap.dedent(paragraph).strip()
        formattedText = textwrap.fill(unformattedText, width=charsPerLine)
        return formattedText
