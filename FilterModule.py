from Module import *
from MovingAverageFIlter import *
import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import matplotlib.animation as animation
from statistics import mean

class FilterModule(Module):
    def __init__(self, gui = None, title = None):
        super(FilterModule, self).__init__(gui = gui, title = title)
        self.movingAverageModule = MovingAverageFilter(gui = gui)
        self.font = ('Comic Sans MS', 11, 'bold italic')
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


    def movingAverage(self):
        """
        The idea here is to explain the disadvantages of the moving average
        Visualizing pane: matplotlib of moving avg
        interactive pane: how much history we care about (sliding thing maybe)

        Explain:
        + The moving avg is fine for short history or very noisy data
        - However on moving object, we can't use it to localize a robot
        """
        i = 0
        aboutMovingAvg = \
                    "One of the most basic forms of filtering data is with a\n" \
                    "technique called the moving average. Similar to a normal\n" \
                    "average, the moving average tries to smooth out any outliers.\n" \
                    "The moving average keeps track of a 'history' as defined by\n" \
                    "the filter designer. The shorter the history, the less samples \n"\
                    "at a time the filter will average. Let's take a look at an example.\n" \
                    "The graph on the right shows how a moving average would look \n" \
                    "without a history at all. That is, no filtering occurs. \n" \
                    "Go ahead and change the history and run the filter again."
        self.gui.clearScreen()
        self.makePanes()
        #self.animateText(260, 150,text = aboutMovingAvg, canvasOfText=self.interactivePane, font = self.font)
        self.interactivePane.create_text(260, 150, text = aboutMovingAvg, font = self.font)
        # create Matplotlib figure
        f = Figure(figsize=(5, 5), dpi=100)
        self.axis = f.add_subplot(111)
        self.axis.set_ylim([0, 10])
        self.axis.set_xlim([0, len(self.xData) + 1])
        figureCanvas = FigureCanvasTkAgg(f, master=self.visualizingPane)
        figureCanvas.get_tk_widget().grid(row=0, column=0)

        history = tk.Entry(self.interactivePane)
        history.place(relx = .5, rely = .7, anchor = tk.CENTER)
        historyLabel = tk.Label(self.interactivePane, text = "History:", bg = 'grey')
        historyLabel.place(relx = .5, rely = .65, anchor = tk.CENTER)
        tryNewHistory = tk.Button(self.interactivePane, relief=tk.RAISED, command=lambda: self.rePlot(history.get()),
                                  text =  "Plot!")
        tryNewHistory.place(relx = .5, rely = .75, anchor = tk.CENTER)
        self.axis.plot(self.xData, self.yData, marker='o', markersize=10.0, linestyle='None', color='g')
        self.placeNextButton(.675, .7, pane = self.interactivePane,
                             text = "Continue", font = self.font, command = self.movingAvgQuiz)
        self.placeBackButton(.075, .7, pane=self.interactivePane, command=self.introPage,
                             text="Intro Page", font=self.font)
        self.placeBackToMenuButton(self.visualizingPane)

    def movingAvgQuiz(self):
        quizPrompt = "Let's put the knowlege you learned to the test!\n" \
                     "Here are two questions to make sure you're understanding\n" \
                     "The material so far.\n"
        question1 = "1) Why do we need to use filters for sensor data?"
        question2 = "2) Given the following data and a history of three, how many\n" \
                    "moving average values are we going to have, and what are they?\n"
        self.gui.clearScreen()
        self.makePanes()
        self.radioVarMovingAvgQ1.set(-1) # I think this makes it so that none are selected. Nice.
        self.radioVarMovingAvgQ2.set(-1) # I think this makes it so that none are selected. Nice.
        self.interactivePane.create_text(260, 50, text = quizPrompt, font = self.font)

        # QUESTION 1
        self.interactivePane.create_text(200, 90, text=question1, font=self.font)
        self.visualizingPane.create_image(250, 250, image=self.quizQuestionMark, anchor=tk.CENTER)
        A1 = tk.Radiobutton(self.interactivePane, text="A) To make the sensors more power efficient",
                            padx=20, value = "A1", bg = "grey", variable = self.radioVarMovingAvgQ1)
        A1.place(relx = .1, rely = .2)
        B1 = tk.Radiobutton(self.interactivePane, text="B) To bias the sensor data into something desirable ",
                            padx=20, value = "B1", bg="grey",variable = self.radioVarMovingAvgQ1)
        B1.place(relx=.1, rely=.25)
        C1 = tk.Radiobutton(self.interactivePane, text="C) To remove some noise and outliers from the sensor data",
                            padx=20, value = "C1", bg="grey", variable = self.radioVarMovingAvgQ1)
        C1.place(relx=.1, rely=.3)
        D1 = tk.Radiobutton(self.interactivePane, text="D) None of the above",
                            padx=20, value = "D1", bg="grey", variable = self.radioVarMovingAvgQ1)
        D1.place(relx=.1, rely=.35)

        # QUESTION 2
        self.interactivePane.create_text(250, 235, text=question2, font=self.font)
        self.interactivePane.create_text(190, 255, text="Data: [5, 5.25, 4.75, 4.8, 5.2, 5.5, 5, 4.75]",
                                         font=self.font)
        A2 = tk.Radiobutton(self.interactivePane, text="A) 6, Values: [5, 4.93, 4.91, 5.16, 5.23, 5.08]",
                            padx=20, value="A2", bg="grey", variable=self.radioVarMovingAvgQ2)
        A2.place(relx=.1, rely=.525)
        B2 = tk.Radiobutton(self.interactivePane, text="B) 6, Values: [5, 5, 4.91, 5.26, 5, 5.15]",
                            padx=20, value="B2", bg="grey", variable=self.radioVarMovingAvgQ2)
        B2.place(relx=.1, rely=.575)
        C2 = tk.Radiobutton(self.interactivePane, text="C) 5, Values: [5, 4.93, 4.91, 5.23, 5.08]",
                            padx=20, value="C2", bg="grey", variable=self.radioVarMovingAvgQ2)
        C2.place(relx=.1, rely=.625)
        D2 = tk.Radiobutton(self.interactivePane, text="D) 3, Values: [4.93, 5.16, 5.08]",
                            padx=20, value="D2", bg="grey", variable=self.radioVarMovingAvgQ2)
        D2.place(relx=.1, rely=.675)
        correctAnswers = [[self.radioVarMovingAvgQ1, "C1"],[self.radioVarMovingAvgQ2, "A2"]]
        self.placeBackToMenuButton(self.visualizingPane)
        self.placeNextButton(.675, .75, pane=self.interactivePane,
                             text="Submit Quiz", font=self.font, command=lambda: self.checkTest(correctAnswers))
        self.placeBackButton(.075, .75, pane=self.interactivePane, command=self.movingAverage,
                             text="", font=self.font)


    def runModule(self):
        self.gui.clearScreen()
        self.makePanes()
        #self.movingAvgQuiz()
        self.introPage()


