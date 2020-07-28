from Module import *
import tkinter as tk
from PIL import Image, ImageTk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from edge_detection import *

class CVModule(Module):
    def __init__(self, gui = None, title = None):
        super(CVModule, self).__init__(gui = gui, title = title)
        self.cv_overview = tk.PhotoImage(file = "cv_home_example.png")
        self.cv_connections = tk.PhotoImage(file = "Computer-vision-apply-for-medical-image-processing.png")
        self.edge_detect = tk.PhotoImage(file = "edge_pepper_cropped5.png")
        self.img_for_ed_interactive = tk.PhotoImage(file = "single_rose_medium_sqare.png")
        # tk.Frame.__init__(self)
        # self.tk.Frame.master.bind('<Configure>', self.resize_image)

        self.quizQuestionMark = tk.PhotoImage(file="quizQuestionMark.png")
        self.quizPassedImage = tk.PhotoImage(file="passedQuiz.png")
        self.quizFailedImage = tk.PhotoImage(file="failedQuiz.png")
        self.radioVarCVQ1 = tk.StringVar()
        self.radioVarCVQ2 = tk.StringVar()

        self.font = ('Comic Sans MS', 11, 'bold italic')


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

        # im_temp = Image.open("Computer-vision-apply-for-medical-image-processing.png")
        # im_temp = im_temp.resize((300, 250), Image.ANTIALIAS)
        # im_temp.save("test.png", "png")

        #int(300 * float(w / 2)),int(300 * float(h / 2))
        self.visualizingPane.create_image(0,0, image=tk.PhotoImage(file = "test.png"), anchor=tk.CENTER)

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
        # self.placeNextButton(.7, .7, pane=self.interactivePane,
        #                      text="Main Menu", font=font, command=self.gui.HomePage)
        # self.gui.moduleDict["Computer Vision"].completed = True
        self.placeNextButton(.7, .7, pane=self.interactivePane,
                             text="ED Interaction", font=font, command=self.edge_detection_interactive)

    def edge_detection_interactive(self):
        self.gui.clearScreen()
        #INSTEAD OF SELF.MAKE PANES
        self.interactivePane = tk.Canvas(self.gui.win, width=500, height=250, bg='grey')
        sliderPane = tk.Canvas(self.gui.win, width=500, height=250, bg='grey')
        self.visualizingPane = tk.Canvas(self.gui.win, width=500, height=250, bg='white')
        second_visualizingPane = tk.Canvas(self.gui.win, width=500, height=250, bg='grey')
        self.interactivePane.grid(row=0, column=0)
        sliderPane.grid(row=1, column=0)
        self.visualizingPane.grid(row=0, column=1)
        second_visualizingPane.grid(row=1, column=1)

        self.visualizingPane.create_image(250, 100, image=self.img_for_ed_interactive, anchor=tk.CENTER)
        ed = EdgeDecectionandGaussianBlur().edge_detection()
        im = Image.fromarray(ed)
        im_temp = im
        im_temp = im_temp.resize((300, 300), Image.ANTIALIAS)
        self.imgtk = ImageTk.PhotoImage(image=im_temp)

        second_visualizingPane.create_image(250, 100, image=self.imgtk, anchor=tk.CENTER)

        font = ('Comic Sans MS', 11, 'bold italic')
        self.showText(275, 150, "THIS IS SO DUMB", self.interactivePane, font)

        self.minval_slider = tk.Scale(sliderPane, from_=0, to=200, orient=tk.HORIZONTAL)
        self.maxval_slider = tk.Scale(sliderPane, from_=0, to=200, orient=tk.HORIZONTAL)
        self.minval_slider.pack()
        self.maxval_slider.pack()

        recalc = tk.Button(sliderPane, text='Recalc Image', command=self.recalc_image)
        recalc.pack()
        # w = tk.Scale(self.interactivePane, from_=0, to=200, orient=HORIZONTAL)
        # w.pack()

        self.placeBackButton(0.1, .4, pane=self.interactivePane, command=self.edge_detection,
                             text="ED Activity", font=font)
        self.placeNextButton(.7, .4, pane=self.interactivePane,
                             text="Gaussian Filtering", font=font, command=self.gaussian)


    def gaussian(self):
        self.gui.clearScreen()
        # INSTEAD OF SELF.MAKE PANES
        self.interactivePane = tk.Canvas(self.gui.win, width=500, height=250, bg='grey')
        sliderPane = tk.Canvas(self.gui.win, width=500, height=250, bg='grey')
        self.visualizingPane = tk.Canvas(self.gui.win, width=500, height=250, bg='white')
        self.second_visualizingPane = tk.Canvas(self.gui.win, width=500, height=250, bg='grey')
        self.interactivePane.grid(row=0, column=0)
        sliderPane.grid(row=1, column=0)
        self.visualizingPane.grid(row=0, column=1)
        self.second_visualizingPane.grid(row=1, column=1)

        ed = EdgeDecectionandGaussianBlur().edge_detection()
        im = Image.fromarray(ed)
        imgtk = ImageTk.PhotoImage(image=im)

        self.visualizingPane.create_image(250, 100, image=self.img_for_ed_interactive, anchor=tk.NE)
        self.second_visualizingPane.create_image(50, 50, image=imgtk, anchor=tk.NE)

        font = ('Comic Sans MS', 11, 'bold italic')
        self.showText(275, 150, "THIS IS SO DUMB pt 2", self.interactivePane, font)

        kernalX_slider = tk.Scale(sliderPane, from_=0, to=200, orient=tk.HORIZONTAL)
        kernalY_slider = tk.Scale(sliderPane, from_=0, to=200, orient=tk.HORIZONTAL)
        sigmaX_slider= tk.Scale(sliderPane, from_=0, to=200, orient=tk.HORIZONTAL)
        kernalX_slider.pack()
        kernalY_slider.pack()
        sigmaX_slider.pack()

        self.placeBackButton(.1, .4, pane=self.interactivePane, command=self.edge_detection_interactive,
                             text="ED Activity", font=font)
        self.placeNextButton(.7, .4, pane=self.interactivePane,
                             text="Gaussian Filtering", font=font, command=self.CVQuiz)


    def recalc_image(self):
        minval = self.minval_slider.get()
        maxval = self.maxval_slider.get()

        ed = EdgeDecectionandGaussianBlur(minval, maxval).edge_detection()
        im = Image.fromarray(ed)
        im_temp = im
        im_temp = im_temp.resize((300, 300), Image.ANTIALIAS)
        self.imgtk = ImageTk.PhotoImage(image=im_temp)

        self.gui.win.winfo_children()[3].destroy()
        self.second_visualizingPane = tk.Canvas(self.gui.win, width=500, height=250, bg='grey')
        self.second_visualizingPane.grid(row=1, column=1)
        self.second_visualizingPane.create_image(250, 100, image=self.imgtk, anchor=tk.CENTER)

    def CVQuiz(self):
        quizPrompt = "Let's put the knowlege you learned to the test!\n" \
                     "Here are two questions to make sure you're understanding\n" \
                     "The material so far.\n"
        question1 = "1) What is Hysterisis Thresholding used for?\n"
        question2 = "2) How is the gradient used in non-maximum supression?\n"
        self.gui.clearScreen()
        self.makePanes()
        self.radioVarCVQ1.set(-1) # I think this makes it so that none are selected. Nice.
        self.radioVarCVQ2.set(-1) # I think this makes it so that none are selected. Nice.
        self.interactivePane.create_text(260, 50, text = quizPrompt, font = self.font)

        # QUESTION 1
        self.interactivePane.create_text(200, 90, text=question1, font=self.font)
        self.visualizingPane.create_image(250, 250, image=self.quizQuestionMark, anchor=tk.CENTER)
        A1 = tk.Radiobutton(self.interactivePane, text="A) To lighten the image",
                            padx=20, value = "A1", bg = "grey", variable = self.radioVarCVQ1)
        A1.place(relx = .1, rely = .2)
        B1 = tk.Radiobutton(self.interactivePane, text="B) To change the color intensity of the image",
                            padx=20, value = "B1", bg="grey",variable = self.radioVarCVQ1)
        B1.place(relx=.1, rely=.25)
        C1 = tk.Radiobutton(self.interactivePane, text="C) To remove noise from the image",
                            padx=20, value = "C1", bg="grey", variable = self.radioVarCVQ1)
        C1.place(relx=.1, rely=.3)
        D1 = tk.Radiobutton(self.interactivePane, text="D) To determine which edges are true edges",
                            padx=20, value = "D1", bg="grey", variable = self.radioVarCVQ1)
        D1.place(relx=.1, rely=.35)

        # QUESTION 2
        self.interactivePane.create_text(250, 235, text=question2, font=self.font)
        A2 = tk.Radiobutton(self.interactivePane, text="A) It is used to determine if a point should be put to zero or not",
                            padx=20, value="A2", bg="grey", variable=self.radioVarCVQ2)
        A2.place(relx=.1, rely=.525)
        B2 = tk.Radiobutton(self.interactivePane, text="B) It is used to smooth out the image",
                            padx=20, value="B2", bg="grey", variable=self.radioVarCVQ2)
        B2.place(relx=.1, rely=.575)
        C2 = tk.Radiobutton(self.interactivePane, text="C) It is used to determine where an pixel is in the image",
                            padx=20, value="C2", bg="grey", variable=self.radioVarCVQ2)
        C2.place(relx=.1, rely=.625)
        D2 = tk.Radiobutton(self.interactivePane, text="D) It is used to calculate minval",
                            padx=20, value="D2", bg="grey", variable=self.radioVarCVQ2)
        D2.place(relx=.1, rely=.675)
        correctAnswers = [[self.radioVarCVQ1, "D1"],[self.radioVarCVQ2, "A2"]]
        self.placeBackToMenuButton(self.visualizingPane)
        self.placeNextButton(.675, .75, pane=self.interactivePane,
                             text="Submit Quiz", font=self.font, command=lambda: self.checkTest(correctAnswers))
        self.placeBackButton(.075, .75, pane=self.interactivePane, command=self.gaussian,
                             text="", font=self.font)
        pass


    # Pass the list containing the correct answer objects (multiple choice)
    def checkTest(self, correctAnswers):
        for answer in correctAnswers:
            if (answer[0].get() == answer[1]):
                pass
            else:
                print("Quiz Failed.")
                self.quizFailed(self.CVQuiz)
                return
        print("Quiz Passed.")
        #self.quizPassed(self.introToKalmanFilter)
        pass

    def quizPassed(self, nextPage):
        self.gui.clearScreen()
        canvas = tk.Canvas(self.gui.win, width=1000, height=500, bg='grey')
        canvas.grid(row=0, column=0)
        canvas.create_image(500, 250, image=self.quizPassedImage, anchor=tk.CENTER)
        canvas.create_text(500, 50, text="Quiz Passed!", font=self.font)
        self.placeBackToMenuButton(canvas)
        self.placeNextButton(.7, .7, pane=canvas, command=nextPage, text="Next Topic!",
                             font=self.font)

    def quizFailed(self, previousPage):
        self.gui.clearScreen()
        canvas = tk.Canvas(self.gui.win, width=1000, height=500, bg='grey')
        canvas.grid(row=0, column=0)
        canvas.create_image(500, 250, image=self.quizFailedImage, anchor=tk.CENTER)
        canvas.create_text(500, 50, text="Quiz Failed!", font=self.font)
        self.placeBackToMenuButton(canvas)
        self.placeBackButton(.1, .7, pane=canvas, command=previousPage, text="To Quiz",
                             font=self.font)


    def runModule(self):
        self.gui.clearScreen()
        self.makePanes()
        self.introPage()


        #MAKE EDGE DETECTION CHANGE PARAMETER EXAMPLE OPENCV AND PYTHON REPROCESS IMAGE

