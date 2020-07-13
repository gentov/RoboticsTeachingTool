from Module import *
import tkinter as tk
from PIL import Image, ImageTk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
class CVModule(Module):
    def __init__(self, gui = None, title = None):
        super(CVModule, self).__init__(gui = gui, title = title)
        self.cv_overview = tk.PhotoImage(file = "cv_home_example.png")
        self.cv_connections = tk.PhotoImage(file = "Computer-vision-apply-for-medical-image-processing.png")
        self.edge_detect = tk.PhotoImage(file = "edge_pepper_cropped5.png")
        # tk.Frame.__init__(self)
        # self.tk.Frame.master.bind('<Configure>', self.resize_image)

    def introPage(self):
        paragraph = "Now, we are going to introduce you to computer vision!\n" \
                    "Computer vision is a burgeoning field in the robotics\n"\
                    "community because it allows more sensing information.\n" \
                    "Traditional sensing methods, like LIDAR, only tell a \n" \
                    "portion of the story. Using RGBD cameras with CV allow\n" \
                    "for knowlege of the distance of the object, and in-depth \n" \
                    "procesing of the image that allows for the robot to recognize \n" \
                    "the object."
        font = ('Comic Sans MS', 11, 'bold italic')
        self.visualizingPane.create_image(300,250,image = self.cv_overview, anchor = tk.CENTER)
        self.animateText(275, 150, paragraph,self.interactivePane, font)
        self.placeNextButton(.7, .7, pane = self.interactivePane,
                             text = "Let's go!", font = font, command = self.connection)
        self.placeBackButton(.1, .7, pane=self.interactivePane, command=self.gui.HomePage,
                             text="Main Menu", font=font)

        # root = tk.Tk()
        # T = self.Text(root, height=2, width=30)
        # T.pack()
        # T.insert(tk.END, "Just a text Widget\nin two lines\n")
        # tk.mainloop()

    def connection(self):
        self.gui.clearScreen()
        self.makePanes()

        self.visualizingPane.create_image(300, 250, image=self.edge_detect, anchor=tk.CENTER)

    # def resize_image(self):
    #     new_width = self.master.winfo_width()
    #     new_height = self.master.winfo_height()
    #
    #     self.image = self.img_copy.resize((new_width, new_height))
    #
    #     self.background_image = ImageTk.PhotoImage(self.image)
    #     self.background.configure(image=self.background_image)

    # def movingAverage(self):
    #     """
    #     The idea here is to explain the disadvantages of the moving average
    #     Visualizing pane: matplotlib of moving avg
    #     interactive pane: how much history we care about (sliding thing maybe)
    #
    #     Explain:
    #     + The moving avg is fine for short history or very noisy data
    #     - However on moving object, we can't use it to localize a robot
    #     """
    #     self.gui.clearScreen()
    #     self.makePanes()
    #     # MATPLOTLIB GRAPH
    #     f = Figure(figsize=(5,5), dpi = 100)
    #     a = f.add_subplot(111)
    #     a.plot([1,2,3,4,5,6,7,8],[5,6,1,3,8,9,3,5])
    #     canvas = FigureCanvasTkAgg(f, master = self.visualizingPane)
    #     canvas.get_tk_widget().grid(row=0, column=0)

    def runModule(self):
        self.gui.clearScreen()
        self.makePanes()
        self.introPage()

