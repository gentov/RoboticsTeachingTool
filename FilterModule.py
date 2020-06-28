from Module import *
import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
class FilterModule(Module):
    def __init__(self, gui = None, title = None):
        super(FilterModule, self).__init__(gui = gui, title = title)
        self.noisyImage = tk.PhotoImage(file = "noisy_data.png")

    def introPage(self):
        paragraph = "Here, we're going to cover the basics of filtering!\n" \
                    "First, we need to understand why filtering is important.\n"\
                    "Every measurement we take in the real world, has uncerainty.\n" \
                    "This means that we can never be too certain about the \n" \
                    "measurements we acquire. This is often why it is \n" \
                    "crucial to take multiple measurements in science! Filtering \n" \
                    "is a technique we use to get better measurements from our \n" \
                    "sensors."
        font = ('Comic Sans MS', 11, 'bold italic')
        self.visualizingPane.create_image(300,250,image = self.noisyImage, anchor = tk.CENTER)
        self.animateText(paragraph,self.interactivePane, font)
        self.placeNextButton(.7, .7, pane = self.interactivePane,
                             text = "Let's go!", font = font, command = self.movingAverage)
        self.placeBackButton(.1, .7, pane=self.interactivePane, command=self.gui.HomePage,
                             text="Main Menu", font=font)

    def movingAverage(self):
        """
        The idea here is to explain the disadvantages of the moving average
        Visualizing pane: matplotlib of moving avg
        interactive pane: how much history we care about (sliding thing maybe)

        Explain:
        + The moving avg is fine for short history or very noisy data
        - However on moving object, we can't use it to localize a robot
        """
        self.gui.clearScreen()
        self.makePanes()
        # MATPLOTLIB GRAPH
        f = Figure(figsize=(5,5), dpi = 100)
        a = f.add_subplot(111)
        a.plot([1,2,3,4,5,6,7,8],[5,6,1,3,8,9,3,5])
        canvas = FigureCanvasTkAgg(f, master = self.visualizingPane)
        canvas.get_tk_widget().grid(row=0, column=0)
    def particleFilter(self):
        pass

    def kalmanFilter(self):
        pass

    def runModule(self):
        self.gui.clearScreen()
        self.makePanes()
        self.introPage()

