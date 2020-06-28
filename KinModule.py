# Owen Smith
# 6/16/2020

from Module import Module as Mod


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



    def runModule(self):
        self.gui.clearScreen()
        self.makePanes()
        self.interactivePane.config(bg="red")

        title = self.visualizingPane.create_text(self.XPAD, 20, anchor="nw", font=("Purisa", 20), text="Forward Kinematics")
        self.visualizingPane.create_line(17, 55, 265, 55)
        self.visualizingPane.create_text(self.XPAD, 60, anchor="nw", font=("Purisa", 11), text=self.description,
                                         fill="sky blue")
        self.visualizingPane.create_text(self.XPAD, 110, anchor="nw", font=("Purisa", 16), text="Frame Transformations")

        self.placeBackButton(.1, .1, self.interactivePane, command=self.gui.HomePage)

        self.animateText(275, 25, "hello world asdfasdgdfgnaodfnfv goa dejgofhgoah dfnjoiganfg nf", self.interactivePane, font=None)
        #self.visualizingPane.create
