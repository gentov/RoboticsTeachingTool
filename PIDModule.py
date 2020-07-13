from Module import *
import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from SimpleDrone import *
from matplotlib.animation import FuncAnimation
class PIDModule(Module):
    def __init__(self, gui = None, title = None):
        super(PIDModule, self).__init__(gui = gui, title = title)
        self.pidGraph = tk.PhotoImage(file = "pidgraph.png")
        self.kpLabel = None
        self.kdLabel = None
        self.kiLabel = None

        self.kpEntry = None
        self.kdEntry = None
        self.kiEntry = None

        self.kp = 10;
        self.kd = 0;
        self.ki = 0;

        self.drone = SimpleDrone(.2, 0)
        self.axis = None
        self.xData = [1, 2, 3, 4, 5, 6, 7, 8]
        #self.xData = []
        #self.yMovingAvgData = []
        self.yData = [5.5, 6.25, 5.25, 5.5, 5.75, 4.75, 5.25, 5.75]
    def introPage(self):
        paragraph = "Let's talk about control.\n" \
                    "You want to be able to control the motion of \n" \
                    "any system you create.\n"\
                    "Here we'll talk about \n" \
                    "Proportional Integral Derivative (PID) controllers .\n"
        font = ('Comic Sans MS', 11, 'bold italic')
        self.visualizingPane.create_image(300,250,image = self.pidGraph, anchor = tk.CENTER)
        self.animateText(275, 150, paragraph,self.interactivePane, font)
        self.placeNextButton(.7, .7, pane = self.interactivePane,
                             text = "Let's go!", font = font, command = self.dronePID)
        self.placeBackButton(.1, .7, pane=self.interactivePane, command=self.gui.HomePage,
                             text="Main Menu", font=font)

    def dronePID(self):
        """
        Show response using graph when you set certain kp,kd,ki
        Visualizing pane: matplotlib of PID going to a setpoint
        interactive pane: Gain changing

        """
        self.gui.clearScreen()
        self.makePanes()
        # MATPLOTLIB GRAPH
        f = Figure(figsize=(5,5), dpi = 100)
        a = f.add_subplot(111)
        self.plotP(a)
        self.kpLabel = tk.Label(self.interactivePane, text="KP: ").grid(row=0)
        self.kdLabel = tk.Label(self.interactivePane, text="KD: ").grid(row=1)
        self.kiLabel = tk.Label(self.interactivePane, text="KI: ").grid(row=2)
        kpText = tk.StringVar()
        kdText = tk.StringVar()
        kiText = tk.StringVar()

        self.kpEntry = tk.Entry(self.interactivePane, command=self.setKP(), textvariable = kpText)
        self.kdEntry = tk.Entry(self.interactivePane, command=self.setKD(), textvariable = kdText)
        self.kiEntry = tk.Entry(self.interactivePane, command=self.setKI(), textvariable = kiText)

        kpText.set("0")
        kdText.set("0")
        kiText.set("0")

        self.kpEntry.grid(row=0, column=1)
        self.kdEntry.grid(row=1, column=1)
        self.kiEntry.grid(row=2, column=1)

        canvas = FigureCanvasTkAgg(f, master = self.visualizingPane)
        canvas.get_tk_widget().grid(row=0, column=0)

    # Give axes to plot a simple P controller
    def plotP(self, a):
        a.plot([1, 2, 3, 4, 5, 6, 7],[1, 3, 7, 8, 7.5, 7, 8])

    def PID(self):
        pass

    def runModule(self):
        self.gui.clearScreen()
        self.makePanes()
        self.introPage()

    def setKP(self):
        #self.kp = type(float(self.kpEntry.get()))
        print("set kp")

    def setKD(self):
        pass

    def setKI(self):
        pass