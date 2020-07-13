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
        self.gui.clearScreen()
        self.makePanes()
        with open('cv_intro.txt', 'r') as file:
            data = file.read().replace('\n', '')
            paragraph = data
        font = ('Comic Sans MS', 11, 'bold italic')
        self.visualizingPane.create_image(300, 250,image = self.cv_overview, anchor = tk.CENTER)
        self.showText(275, 150, paragraph,self.interactivePane, font)
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
        with open('connections.txt', 'r') as file:
            data = file.read().replace('\n', '')
            paragraph = data
        font = ('Comic Sans MS', 11, 'bold italic')
        self.showText(275, 150, paragraph,self.interactivePane, font)
        w = self.visualizingPane.winfo_width()
        h = self.visualizingPane.winfo_height()
        # img = Image.open("Computer-vision-apply-for-medical-image-processing.png")  # PIL solution
        # img = img.resize((300, 250), Image.BOX)  # The (250, 250) is (height, width)
        # img = ImageTk.PhotoImage(img)  # convert to PhotoImage

        im_temp = Image.open("Computer-vision-apply-for-medical-image-processing.png")
        im_temp = im_temp.resize((300, 250), Image.ANTIALIAS)
        im_temp.save("test.png", "png")

        #int(300 * float(w / 2)),int(300 * float(h / 2))
        self.visualizingPane.create_image(int(300 * float(w / 2)),int(300 * float(h / 2)), image=tk.PhotoImage(file = "test.png"), anchor=tk.CENTER)

        self.placeNextButton(.7, .7, pane=self.interactivePane,
                             text="Edge \n Detection", font=font, command=self.edge_detection)
        self.placeBackButton(.1, .7, pane=self.interactivePane, command=self.introPage,
                             text="Overview", font=font)

    def edge_detection(self):
        self.gui.clearScreen()
        self.makePanes()
        with open('edge_detection.txt', 'r') as file:
            data = file.read().replace('\n', '')
            paragraph = data
        font = ('Comic Sans MS', 11, 'bold italic')
        self.showText(275, 150, paragraph,self.interactivePane, font)
        self.visualizingPane.create_image(300, 250, image=self.edge_detect, anchor=tk.CENTER)
        # self.placeNextButton(.7, .7, pane=self.interactivePane,
        #                      text="Let's go!", font=font, command=self.edge_detection)
        self.placeBackButton(.1, .7, pane=self.interactivePane, command=self.connection,
                             text="CV vs ML", font=font)
        self.placeNextButton(.7, .7, pane=self.interactivePane,
                             text="Main Menu", font=font, command=self.gui.HomePage)
        self.gui.moduleDict["Computer Vision"].completed = True

    def runModule(self):
        self.gui.clearScreen()
        self.makePanes()
        self.introPage()

