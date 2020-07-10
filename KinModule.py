# Owen Smith
# 6/16/2020

from Module import Module as Mod
from PIL import ImageTk

class KinModule(Mod):
    def __init__(self, gui=None):
        description = 'Empty\nempty'
        try:
            f = open("kineticDesc.txt", "r")
            try:
                if f.mode == 'r':
                    description = f.read()
            finally:
                f.close()
        except FileNotFoundError:
            print("No description resource provided for Kinematic Module")

        super().__init__(gui, "Robot Kinematics", description)
        self.XPAD = 20
        self.font = ('Comic Sans MS', 11, 'bold italic')

    def runModule(self):
        self.gui.clearScreen()
        self.makePanes()
        #self.interactivePane.config(bg="gainsboro")
        image = ImageTk.PhotoImage(file = "BluePurpleGradient.png")

        self.interactivePane.create_image(0, 0, image=image, anchor="nw")
        title = self.visualizingPane.create_text(self.XPAD, 20, anchor="nw", font=("Purisa", 20),
                                                 text="Forward Kinematics")
        self.visualizingPane.create_line(17, 55, 265, 55)
        self.visualizingPane.create_text(self.XPAD, 60, anchor="nw", font=("Purisa", 11), text=self.description,
                                         fill="sky blue")
        self.visualizingPane.create_text(self.XPAD, 110, anchor="nw", font=("Purisa", 16), text="Frame Transformations")
        self.intro_page()
        # self.visualizingPane.create

    def intro_page(self):

        self.placeBackButton(.1, .7, self.interactivePane, command=self.gui.HomePage, text="Main Menu", font=self.font)

        self.place_intro_title('Robot Kinematics')
        self.interactivePane.create_text(255, 225, text="This module covers the breadth of topics necessary to\n "
                                                       "form an introductory understanding of forward and\n"
                                                       "inverse position kinematics for serial (i.e. armed) robots.\n"
                                                       "It begins with a discussion of basic frame transformations\n"
                                                       "and transitions to a discussion of transformation matrices.\n"
                                                       "These form the basis needed to dive into forward kinematics\n"
                                                       "and to introduce Denavit-Hartenburg (DH) parameters. Finally,\n"
                                                       "geometric inverse kinematics are covered using the law of\n"
                                                       "cosines and the atan2 function.", font=self.font)

    def place_intro_title(self, text):
        title_font = ('Courier', 30, 'bold italic')
        rainbow_fill = ['red', 'dark orange', 'gold', 'green3', 'blue', 'dark violet']
        for i in range(0, len(text)):
            char = text[i]
            color = rainbow_fill[i%len(rainbow_fill)]
            self.interactivePane.create_text(20+(25*i), 50, anchor="nw", font=title_font, text=char, fill=color)

