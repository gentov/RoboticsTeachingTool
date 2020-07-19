#@TODO: Use grids instead of "place relx rely"
from tkinter import *
from tkinter import simpledialog
from Module import *
from FilterModule import *
from KinModule import *
from PIDModule import *
from CVModule import *
class GUI():
    def __init__(self):
        self.win = Tk()
        self.win.title("Robotics Teaching Tool")
        self.moduleDict = {
            "PID": PIDModule(gui = self, title="PID"),
            "FK/IK": KinModule(gui=self),
            "Filters": FilterModule(gui = self, title = "Filters"),
            "Computer Vision": CVModule(gui=self, title="Computer Vision")
        }
        self.moduleDict["PID"].completed = True
        
    def HomePage(self):
        self.clearScreen()
        self.win.configure(background="grey")
        #self.canvas = Canvas(self.win, width=700, height=800, bg="grey", highlightthickness=0)
        # I want four different frames for buttons and widgets, in each of the corners
        # @TODO: Replace with frames
        finishedTopicsFrame = Frame(self.win, bg="green", width=500, height=250)
        finishedTopicsFrame.grid(row = 0, column = 0)
        additionalResourcesFrame = Canvas(self.win, bg="blue", width=500, height=250)
        additionalResourcesFrame.grid(row=1, column=0)
        recommendedTopicsFrame = Frame(self.win, bg="yellow", width=500, height=500)
        recommendedTopicsFrame.grid(row=0, column=1, rowspan = 2)

        # POPULATE RECOMMENDED FRAME AND FINISHED FRAME
        # make a button for each module
        # clicking on the button takes you to the module's panes
        buttonNum = 0
        completedAtLeastOneModule = False
        completedAllTopics = True
        for module in self.moduleDict.values():
            if(module.completed):
                completedAtLeastOneModule = True
                moduleButton = Button(finishedTopicsFrame, height=2, text=module.title,
                                       font=('Comic Sans MS', 10, 'bold italic'), bg="white", command=module.runModule)
                moduleButton.place(relx=.5, rely=.2 + (.21 * buttonNum), anchor=CENTER)
            else:
                completedAllTopics = False
                moduleButton = Button(recommendedTopicsFrame, height=2,text = module.title,font=('Comic Sans MS', 10, 'bold italic'), bg="white", command=module.runModule)
                moduleButton.place(relx=.5, rely=.5+(.12*buttonNum), anchor = CENTER)
            buttonNum+=1

        # Labels for finished and unfinished courses
        if(completedAllTopics):
            recommendedTopicsLabel = Label(recommendedTopicsFrame, text="You've learned all the topics! Great Job!!",
                                       font=('Comic Sans MS', 15, 'bold italic'), bg="yellow")
            recommendedTopicsLabel.place(relx=.5, rely=.5, anchor=CENTER)
        else:
            recommendedTopicsLabel = Label(recommendedTopicsFrame, text="Soak up the skills! Topics left:",
                                       font=('Comic Sans MS', 15, 'bold italic'), bg="yellow")
            recommendedTopicsLabel.place(relx=.5, rely=.2, anchor=CENTER)

        #  Finished label
        if(not completedAtLeastOneModule):
            finishedTopicLabel = Label(finishedTopicsFrame, text = "You haven't finished any topics!!",
                                       font=('Comic Sans MS', 15, 'bold italic'), bg = "green")
            finishedTopicLabel.place(relx=.5, rely=.5, anchor=CENTER)
        else:
            finishedTopicLabel = Label(finishedTopicsFrame, text="You're a rockstar! Here's what you've learned:",
                                       font=('Comic Sans MS', 12, 'bold italic'), bg="green")
            finishedTopicLabel.place(relx=.4, rely=.1, anchor=CENTER)

        # POPULATE ADDITIONAL RESOURCES FRAME

    def clearScreen(self):
        for widget in self.win.winfo_children():
            widget.destroy()

    def addModule(self, module):
        self.moduleList[module.title] = module

g = GUI()
g.HomePage()
g.win.mainloop()
