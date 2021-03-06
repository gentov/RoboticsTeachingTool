from Module import *
import tkinter as tk
from PIL import Image, ImageTk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from edge_detection import *
import cv2


class CVModule(Module):
    def __init__(self, gui=None, title=None):
        super(CVModule, self).__init__(gui=gui, title=title)
        self.cv_overview = tk.PhotoImage(file="images/cv_home_example.png")
        self.cv_connections = tk.PhotoImage(file="images/cv_overview_resized.png")
        self.edge_detect = tk.PhotoImage(file="images/edge_pepper_cropped5.png")
        self.img_for_ed_interactive = tk.PhotoImage(file="images/single_rose_medium_square.png")
        self.img_for_pg_intro = tk.PhotoImage(file="images/perspective4.png")
        self.lr_example = tk.PhotoImage(file="images/lr_example4.png")
        self.fmse_eqns = tk.PhotoImage(file="images/fmse_eqns4.png")
        self.sobel_eqns = tk.PhotoImage(file = "images/sobel_eqns2.png")
        self.non_max = tk.PhotoImage(file = "images/nonmaxsupress2.png")
        self.hyst_graph = tk.PhotoImage(file = "images/hysterisis_graph2.png")
        self.butterfly = tk.PhotoImage(file = "images/butterfly_resized.png")
        self.robot_learning = tk.PhotoImage(file = "images/machineLearning_robot.png")
        self.gaussian_image = tk.PhotoImage(file="images/gaussian_filtering_img2.png")
        # tk.Frame.__init__(self)
        # self.tk.Frame.master.bind('<Configure>', self.resize_image)

        self.quizQuestionMark = tk.PhotoImage(file="images/quizQuestionMark.png")
        self.quizPassedImage = tk.PhotoImage(file="images/passedQuiz.png")
        self.quizFailedImage = tk.PhotoImage(file="images/failedQuiz.png")
        self.radioVarCVQ1 = tk.StringVar()
        self.radioVarCVQ2 = tk.StringVar()

        self.font = ('Comic Sans MS', 11, 'bold italic')
        self.label_font = ('Comic Sans MS', 10, 'bold italic')

    def introPage(self):
        self.gui.clearScreen()
        self.makePanes()
        with open('text_blurbs/cv_intro.txt', 'r') as file:
            data = file.read().replace('\n', '')
            paragraph = data
        font = ('Comic Sans MS', 11, 'bold italic')
        self.visualizingPane.bg = "grey"
        self.visualizingPane.create_image(250, 250, image=self.cv_overview, anchor=tk.CENTER)
        self.showText(250, 150, paragraph, self.interactivePane, font)
        self.placeNextButton(.7, .7, pane=self.interactivePane,
                             text="Let's go!", font=font, command=self.connection)
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
        with open('text_blurbs/connections.txt', 'r') as file:
            data = file.read().replace('\n', '')
            paragraph = data
        font = ('Comic Sans MS', 11, 'bold italic')
        self.showText(250, 150, paragraph, self.interactivePane, font)
        w = self.visualizingPane.winfo_width()
        h = self.visualizingPane.winfo_height()

        # im_temp = Image.open("Computer-vision-apply-for-medical-image-processing.png")
        # im_temp = im_temp.resize((400, 300), Image.ANTIALIAS)
        # im_temp.save("cv_overview_resized.png", "png")

        # im_temp = Image.open("gaussian_filtering_img.png")
        # im_temp = im_temp.resize((500, 500), Image.ANTIALIAS)
        # im_temp.save("gaussian_filtering_img2.png", "png")

        # int(300 * float(w / 2)),int(300 * float(h / 2))
        self.visualizingPane.create_image(250, 250, image=self.cv_connections, anchor=tk.CENTER)

        self.placeNextButton(.7, .7, pane=self.interactivePane,
                             text="Edge \n Detection", font=self.label_font, command=self.edge_detection)
        self.placeBackButton(.1, .7, pane=self.interactivePane, command=self.introPage,
                             text="Overview", font=self.label_font)

    def edge_detection(self):
        self.gui.clearScreen()
        self.makePanes()
        with open('text_blurbs/edge_detection.txt', 'r') as file:
            data = file.read().replace('\n', '')
            paragraph = data
        with open('text_blurbs/cv_gaussian_filter.txt', 'r') as file:
            data = file.read().replace('\n', '')
            paragraph2 = data
        full_paragraph = paragraph + "\n" + paragraph2
        font = ('Comic Sans MS', 11, 'bold italic')
        self.showText(250, 150, full_paragraph, self.interactivePane, font)
        self.visualizingPane.create_image(250, 250, image=self.edge_detect, anchor=tk.CENTER)
        # self.placeNextButton(.7, .7, pane=self.interactivePane,
        #                      text="Let's go!", font=font, command=self.edge_detection)
        self.placeBackButton(.1, .7, pane=self.interactivePane, command=self.connection,
                             text="CV Topics", font=self.label_font)
        # self.placeNextButton(.7, .7, pane=self.interactivePane,
        #                      text="Main Menu", font=font, command=self.gui.HomePage)
        # self.gui.moduleDict["Computer Vision"].completed = True
        self.placeNextButton(.7, .7, pane=self.interactivePane,
                             text="Gaussian \nFilter", font=self.label_font, command=self.gaussian_intro)

    def gaussian_intro(self):
        self.gui.clearScreen()
        self.makePanes()
        with open('text_blurbs/cv_gaussian_filter2.txt', 'r') as file:
            d = file.read().replace('\n', '')
            data = d.replace("SPACEPLEASE", '\n')
            paragraph2 = data
        font = ('Comic Sans MS', 11, 'bold italic')
        self.showText(250, 175, paragraph2, self.interactivePane, font)
        self.visualizingPane.create_image(250, 250, image=self.gaussian_image, anchor=tk.CENTER)
        #self.showText(250, 250, paragraph2, self.visualizingPane, font)
        self.placeBackButton(.1, .7, pane=self.interactivePane, command=self.edge_detection,
                             text="Edge \nDetection", font=self.label_font)
        self.placeNextButton(.7, .7, pane=self.interactivePane,
                             text="Sobel Filter", font=self.label_font, command=self.sobel_intro)

    def sobel_intro(self):
        self.gui.clearScreen()
        self.makePanes()
        with open('text_blurbs/cv_sobel.txt', 'r') as file:
            data = file.read().replace('\n', '')
            paragraph = data
        font = ('Comic Sans MS', 11, 'bold italic')
        self.showText(250, 150, paragraph, self.interactivePane, font)
        w = self.visualizingPane.winfo_width()
        h = self.visualizingPane.winfo_height()

        # int(300 * float(w / 2)),int(300 * float(h / 2))
        self.visualizingPane.create_image(250, 250, image=self.sobel_eqns, anchor=tk.CENTER)

        self.placeBackButton(.1, .7, pane=self.interactivePane, command=self.gaussian_intro,
                             text="Gaussian \n Filter", font=self.label_font)
        self.placeNextButton(.7, .7, pane=self.interactivePane,
                             text="Non-Maximum \nSupression", font=self.label_font, command=self.non_maximum_supression_intro)

    def non_maximum_supression_intro(self):
        self.gui.clearScreen()
        self.makePanes()
        with open('text_blurbs/nonmaximum_supression.txt', 'r') as file:
            data = file.read().replace('\n', '')
            paragraph = data
        font = ('Comic Sans MS', 11, 'bold italic')
        self.showText(250, 150, paragraph, self.interactivePane, font)
        w = self.visualizingPane.winfo_width()
        h = self.visualizingPane.winfo_height()

        # int(300 * float(w / 2)),int(300 * float(h / 2))
        self.visualizingPane.create_image(250, 250, image=self.non_max, anchor=tk.CENTER)

        self.placeBackButton(.1, .7, pane=self.interactivePane, command=self.sobel_intro,
                             text="Sobel Filter", font=self.label_font)
        self.placeNextButton(.7, .7, pane=self.interactivePane,
                             text="Hysterisis \nThresholding", font=self.label_font, command=self.hyst_thresh)

    def hyst_thresh(self):
        self.gui.clearScreen()
        self.makePanes()
        with open('text_blurbs/hysterisis_thresh.txt', 'r') as file:
            data = file.read().replace('\n', '')
            paragraph = data
        font = ('Comic Sans MS', 11, 'bold italic')
        self.showText(250, 150, paragraph, self.interactivePane, font)
        w = self.visualizingPane.winfo_width()
        h = self.visualizingPane.winfo_height()

        # int(300 * float(w / 2)),int(300 * float(h / 2))
        self.visualizingPane.create_image(250, 250, image=self.hyst_graph, anchor=tk.CENTER)

        self.placeBackButton(.1, .7, pane=self.interactivePane, command=self.non_maximum_supression_intro,
                             text="Non-Maximum \nSupression", font=self.label_font)
        self.placeNextButton(.7, .7, pane=self.interactivePane,
                             text="Gaussian \nInteractive", font=self.label_font, command=self.gaussian)

    def gaussian(self):
        self.gui.clearScreen()
        # INSTEAD OF SELF.MAKE PANES
        self.interactivePane = tk.Canvas(self.gui.win, width=500, height=250, bg='grey')
        self.sliderPane = tk.Canvas(self.gui.win, width=500, height=250, bg='grey')
        self.visualizingPane = tk.Canvas(self.gui.win, width=500, height=250, bg='white')
        self.second_visualizingPane = tk.Canvas(self.gui.win, width=500, height=250, bg='grey')
        self.interactivePane.grid(row=0, column=0)
        self.sliderPane.grid(row=1, column=0)
        self.visualizingPane.grid(row=0, column=1)
        self.second_visualizingPane.grid(row=1, column=1)

        self.kernalX_slider = tk.Scale(self.sliderPane, from_=0, to=30, label="Kernal X", orient=tk.HORIZONTAL)
        self.kernalY_slider = tk.Scale(self.sliderPane, from_=0, to=30, label="Kernal Y", orient=tk.HORIZONTAL)
        self.sigmaX_slider = tk.Scale(self.sliderPane, from_=0, to=30, label="Sigma X", orient=tk.HORIZONTAL,
                                      resolution=0.1)
        self.kernalX_slider.pack()
        self.kernalY_slider.pack()
        self.sigmaX_slider.pack()

        self.visualizingPane.create_image(250, 100, image=self.img_for_ed_interactive, anchor=tk.CENTER)
        ed = EdgeDecectionandGaussianBlur().gaussian_blur()
        im = Image.fromarray(ed)
        im_temp = im
        im_temp = im_temp.resize((300, 300), Image.ANTIALIAS)
        self.imgtk = ImageTk.PhotoImage(image=im_temp)

        self.second_visualizingPane.create_image(250, 100, image=self.imgtk, anchor=tk.CENTER)

        with open('text_blurbs/gaussian_instructions.txt', 'r') as file:
            data = file.read().replace('\n', '')
            paragraph = data

        font = ('Comic Sans MS', 11, 'bold italic')
        self.showText(250, 75, paragraph, self.interactivePane, font)

        recalc = tk.Button(self.sliderPane, text='Recalc Image', command=self.recalc_image_gaussian)
        recalc.pack()

        self.placeBackButton(0.1, .5, pane=self.interactivePane, command=self.hyst_thresh,
                             text="Hysterisis \nThresholding", font=self.label_font)
        self.placeNextButton(.6, .5, pane=self.interactivePane,
                             text="Edge Detect \nInteractive", font=self.label_font, command=self.edge_detection_interactive)


    def edge_detection_interactive(self):
        self.gui.clearScreen()
        # INSTEAD OF SELF.MAKE PANES
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

        with open('text_blurbs/ed_instructions.txt', 'r') as file:
            data = file.read().replace('\n', '')
            paragraph = data

        font = ('Comic Sans MS', 11, 'bold italic')
        self.showText(250, 75, paragraph, self.interactivePane, font)

        self.minval_slider = tk.Scale(sliderPane, from_=0, to=200, label="Min Val", orient=tk.HORIZONTAL)
        self.maxval_slider = tk.Scale(sliderPane, from_=0, to=200, label="Max Val", orient=tk.HORIZONTAL)
        self.minval_slider.pack()
        self.maxval_slider.pack()

        recalc = tk.Button(sliderPane, text='Recalc Image', command=self.recalc_image_ed)
        recalc.pack()
        # w = tk.Scale(self.interactivePane, from_=0, to=200, orient=HORIZONTAL)
        # w.pack()

        self.placeBackButton(0.1, .5, pane=self.interactivePane, command=self.gaussian,
                             text="Gaussian \nInteractive", font=self.label_font)
        self.placeNextButton(.6, .5, pane=self.interactivePane,
                             text="Quiz", font=self.label_font, command=self.CVQuiz)


    def recalc_image_ed(self):
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

    def recalc_image_gaussian(self):
        kernalX = self.kernalX_slider.get()
        kernalY = self.kernalY_slider.get()
        sigmaX = self.sigmaX_slider.get()

        if kernalX % 2 != 1 or kernalY % 2 != 1:
            error_page = tk.Tk()
            T = tk.Text(error_page, height=3, width=30)
            T.pack()
            T.insert(tk.END, "Kernals need to be odd numbers\n\n close this message\n")
        else:
            ed = EdgeDecectionandGaussianBlur(kernalX=kernalX, kernalY=kernalY, sigmaX=sigmaX).gaussian_blur()
            im = Image.fromarray(ed)
            im_temp = im
            im_temp = im_temp.resize((300, 300), Image.ANTIALIAS)
            self.imgtk = ImageTk.PhotoImage(image=im_temp)

            self.gui.win.winfo_children()[3].destroy()
            self.second_visualizingPane = tk.Canvas(self.gui.win, width=500, height=250, bg='grey')
            self.second_visualizingPane.grid(row=1, column=1)
            self.second_visualizingPane.create_image(250, 100, image=self.imgtk, anchor=tk.CENTER)

    def projective_geometry(self):
        self.gui.clearScreen()
        self.makePanes()
        with open('text_blurbs/pe_intro.txt', 'r') as file:
            data = file.read().replace('\n', '')
            paragraph = data
        with open('text_blurbs/analyticgeometric.txt', 'r') as file:
            data = file.read().replace('\n', '')
            paragraph2 = data
        font = ('Comic Sans MS', 11, 'bold italic')
        self.showText(250, 150, paragraph, self.interactivePane, font)
        self.showText(250, 250, paragraph2, self.visualizingPane, font)
        self.placeBackButton(.1, .7, pane=self.interactivePane, command=self.CVQuiz,
                             text="Quiz", font=self.label_font)
        self.placeNextButton(.7, .7, pane=self.interactivePane,
                             text="Uncalibrated \nCamera", font=self.label_font, command=self.uncalibrated_camera)

    def uncalibrated_camera(self):
        self.gui.clearScreen()
        self.makePanes()
        with open('text_blurbs/cv_uncalibrated_camera.txt', 'r') as file:
            data = file.read().replace('\n', '')
            paragraph = data
        with open('text_blurbs/cv_uncalibrated_camera2.txt', 'r') as file:
            data = file.read().replace('\n', '')
            paragraph2 = data
        font = ('Comic Sans MS', 11, 'bold italic')
        self.showText(250, 150, paragraph, self.interactivePane, font)
        self.showText(250, 250, paragraph2, self.visualizingPane, font)
        self.placeBackButton(.1, .7, pane=self.interactivePane, command=self.projective_geometry,
                             text="Pose \nEstimation", font=self.label_font)
        self.placeNextButton(.7, .7, pane=self.interactivePane,
                             text="Calibrated \nCamera", font=self.label_font, command=self.calibrated_camera)

    def calibrated_camera(self):
        self.gui.clearScreen()
        self.makePanes()
        with open('text_blurbs/cv_calibrated_camera.txt', 'r') as file:
            data = file.read().replace('\n', '')
            paragraph = data
        # with open('cv_calibrated_camera2.txt', 'r') as file:
        #     data = file.read().replace('\n', '')
        #     paragraph2 = data
        paragraph2 = "The algorithm for determining pose estimation is based on \n" \
        "the iterative closest point algorithm. The main idea is to  \n" \
        "determine the correspondences between 2D image features \n" \
        "and points on the 3D model curve.\n"\
        "(a) Reconstruct projection rays from the image points \n" \
        "(b) Estimate the nearest point of each projection ray to a point on the 3D contour \n" \
        "(c) Estimate the pose of the contour with the use of this correspondence set \n" \
        "(d) goto (b)\n" \
        "The above algorithm does not account for images containing\n" \
        "an object that is partially occluded.  Next is an algorithm \n" \
        "that 'assumes that all contours are rigidly coupled, meaning \n" \
        "the pose of one contour defines the pose of another contour."
        font = ('Comic Sans MS', 11, 'bold italic')
        self.showText(250, 150, paragraph, self.interactivePane, font)
        self.showText(250, 250, paragraph2, self.visualizingPane, font)
        self.placeBackButton(.1, .7, pane=self.interactivePane, command=self.uncalibrated_camera,
                             text="Uncalibrated \nCamera", font=self.label_font)
        self.placeNextButton(.7, .7, pane=self.interactivePane,
                             text="Calibrated \nCamera cont.", font=self.label_font, command=self.calibrated_camera_cont)

    def calibrated_camera_cont(self):
        self.gui.clearScreen()
        self.makePanes()
        # with open('cv_calibrated_camera3.txt', 'r') as file:
        #     data = file.read().replace('\n', '')
        #     paragraph = data
        paragraph = "If the pose of one contour defines the pose of another \n" \
        "contour then the following algorithm can be used.\n" \
        "(a) Reconstruct projection rays from the image points \n" \
        "(b) For each projection ray R: \n" \
        "(c) For each 3D contour: \n" \
        "      (c1) Estimate the nearest point P1 \n"\
        "           of ray R to a point on the contour \n" \
        "      (c2) if (n == 1) choose P1 as actual P for \n" \
        "           the point-line correspondence \n" \
        "      (c3) else compare P1 with P: \n" \
        "              if dist(P1, R) is smaller than dist(P, R) then \n" \
        "              choose P1 as new P \n" \
        "(d) Use (P, R) as correspondence set. \n" \
        "(e) Estimate pose with this correspondence set \n" \
        "(f) Transform contours, goto (b)"
        with open('text_blurbs/cv_calibrated_camera4.txt', 'r') as file:
            data = file.read().replace('\n', '')
            paragraph2 = data
        font = ('Comic Sans MS', 11, 'bold italic')
        self.showText(250, 175, paragraph, self.interactivePane, font)
        self.showText(250, 250, paragraph2, self.visualizingPane, font)
        self.placeBackButton(.1, .7, pane=self.interactivePane, command=self.calibrated_camera,
                             text="Calibrated \nCamera", font=self.label_font)
        self.placeNextButton(.7, .7, pane=self.interactivePane,
                             text="Quiz", font=self.label_font, command=self.PoseQuiz)

    def ml_intro(self):
        self.gui.clearScreen()
        self.makePanes()
        with open('text_blurbs/MLintro.txt', 'r') as file:
            data = file.read().replace('\n', '')
            paragraph = data
        # with open('cv_calibrated_camera4.txt', 'r') as file:
        #     data = file.read().replace('\n', '')
        #     paragraph2 = data
        font = ('Comic Sans MS', 11, 'bold italic')
        self.visualizingPane.create_image(250, 250, image=self.robot_learning, anchor=tk.CENTER)
        self.showText(250, 175, paragraph, self.interactivePane, font)
        # self.showText(275, 150, paragraph2, self.visualizingPane, font)
        self.placeBackButton(.1, .7, pane=self.interactivePane, command=self.PoseQuiz,
                             text="Quiz", font=self.label_font)
        self.placeNextButton(.7, .7, pane=self.interactivePane,
                             text="Data \nImportance", font=self.label_font, command=self.ml_data_explain)

    def ml_data_explain(self):
        self.gui.clearScreen()
        self.makePanes()
        with open('text_blurbs/MLdata_explain.txt', 'r') as file:
            data = file.read().replace('\n', '')
            paragraph = data
        self.visualizingPane.create_image(250, 250, image=self.lr_example, anchor=tk.CENTER)
        # with open('cv_calibrated_camera4.txt', 'r') as file:
        #     data = file.read().replace('\n', '')
        #     paragraph2 = data
        font = ('Comic Sans MS', 11, 'bold italic')
        self.showText(250, 178, paragraph, self.interactivePane, font)
        # self.showText(275, 150, paragraph2, self.visualizingPane, font)
        self.yhat_entry = tk.Entry(self.interactivePane)
        self.yhat_entry.place(relx=.5, rely=.9, anchor=tk.CENTER)
        yhatLabel = tk.Label(self.interactivePane, text="y_hat:", bg='grey')
        yhatLabel.place(relx=.5, rely=.85, anchor=tk.CENTER)
        tryNewYhat = tk.Button(self.interactivePane, command = self.check_yhat,
                                  text="Check")
        tryNewYhat.place(relx=.5, rely=.95, anchor=tk.CENTER)

        self.placeBackButton(.1, .7, pane=self.interactivePane, command=self.ml_intro,
                             text="ML Overview", font=self.label_font)
        self.placeNextButton(.7, .7, pane=self.interactivePane,
                             text="Calculating \nWeights", font=self.label_font, command=self.ml_calculating_weights)


    def check_yhat(self):
        is_int = False
        try:
            int(self.yhat_entry.get())
            is_int = True
        except ValueError:
            is_int = False

        if is_int:
            if int(self.yhat_entry.get()) == 119:
                success_page = tk.Tk()
                T = tk.Text(success_page, height=3, width=30)
                T.pack()
                T.insert(tk.END, "Great Job! \n\nClick X and continue on\n")

            else:
                error_page = tk.Tk()
                T = tk.Text(error_page, height=5, width=30)
                T.pack()
                T.insert(tk.END, "Try again \nHINT: vectors should be \nvertical \n\nClick X and try again\n")

        else:
            error_page = tk.Tk()
            T = tk.Text(error_page, height=5, width=30)
            T.pack()
            T.insert(tk.END, "Try again \nHINT: vectors should be \nvertical \n\nClick X and try again\n")


    def ml_calculating_weights(self):
        self.gui.clearScreen()
        self.makePanes()
        with open('text_blurbs/ML_fmse.txt', 'r') as file:
            data = file.read().replace('\n', '')
            paragraph = data
        self.visualizingPane.create_image(250, 250, image=self.fmse_eqns, anchor=tk.CENTER)
        # with open('cv_calibrated_camera4.txt', 'r') as file:
        #     data = file.read().replace('\n', '')
        #     paragraph2 = data
        font = ('Comic Sans MS', 11, 'bold italic')
        self.showText(250, 178, paragraph, self.interactivePane, font)
        # self.showText(275, 150, paragraph2, self.visualizingPane, font)
        self.placeBackButton(.1, .7, pane=self.interactivePane, command=self.ml_data_explain,
                             text="Data \nImportance", font=self.label_font)
        self.placeNextButton(.7, .7, pane=self.interactivePane,
                             text="Additional \nData", font=self.label_font, command=self.ml_data_aug)

    def ml_data_aug(self):
        self.gui.clearScreen()
        self.makePanes()
        with open('text_blurbs/ml_data_augmentation.txt', 'r') as file:
            data = file.read().replace('\n', '')
            paragraph = data

        self.visualizingPane.create_image(250, 250, image=self.butterfly, anchor=tk.CENTER)
        #self.visualizingPane.create_image(250, 250, image=tk.PhotoImage(file="fmse_eqns.png"), anchor=tk.CENTER)
        # with open('cv_calibrated_camera4.txt', 'r') as file:
        #     data = file.read().replace('\n', '')
        #     paragraph2 = data
        font = ('Comic Sans MS', 11, 'bold italic')
        self.showText(250, 175, paragraph, self.interactivePane, font)

        self.data_a= tk.Entry(self.interactivePane)
        self.data_a.place(relx=.5, rely=.9, anchor=tk.CENTER)
        data_a_label = tk.Label(self.interactivePane, text="Python statement:", bg='grey')
        data_a_label.place(relx=.5, rely=.85, anchor=tk.CENTER)
        data_a_button = tk.Button(self.interactivePane, relief=tk.RAISED, command=self.flip_image,
                                  text="Check")
        data_a_button.place(relx=.5, rely=.95, anchor=tk.CENTER)

        # self.showText(275, 150, paragraph2, self.visualizingPane, font)
        self.placeBackButton(.1, .7, pane=self.interactivePane, command=self.ml_calculating_weights,
                             text="Calculating \nWeights", font=self.label_font)
        self.placeNextButton(.7, .7, pane=self.interactivePane,
                             text="Quiz", font=self.label_font, command=self.MLQuiz)

    def flip_image(self):
        statement = self.data_a.get()
        print(statement)

        image = cv2.imread('images/butterfly.jpg', 1)
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        image1 = cv2.imread('images/roses.jpg', 1)
        image2 = cv2.imread('images/single_rose.jpg', 1)

        all_images = [image, image1, image2]

        if (statement == "all_images[0][:, ::-1]"):
            single_image = all_images[0][:, ::-1]
            im = Image.fromarray(single_image)
            im_temp = im
            im_temp = im_temp.resize((500, 500), Image.ANTIALIAS)
            self.imgtk = ImageTk.PhotoImage(image=im_temp)
            self.visualizingPane.create_image(250, 250, image=self.imgtk, anchor=tk.CENTER)

            success_page = tk.Tk()
            T = tk.Text(success_page, height=3, width=30)
            T.pack()
            T.insert(tk.END, "Great Job! \n\nClick X and continue on\n")

        #     return single_image
        # else:
        #     return None


    def CVQuiz(self):
        quizPrompt = "Let's put the knowledge you learned to the test!\n" \
                     "Here are two questions to make sure you're understanding\n" \
                     "The material so far.\n"
        question1 = "1) What is Hysterisis Thresholding used for?\n"
        question2 = "2) How is the gradient used in non-maximum supression?\n"
        self.gui.clearScreen()
        self.makePanes()
        self.radioVarCVQ1.set(-1)  # I think this makes it so that none are selected. Nice.
        self.radioVarCVQ2.set(-1)  # I think this makes it so that none are selected. Nice.
        self.interactivePane.create_text(260, 50, text=quizPrompt, font=self.font)

        # QUESTION 1
        self.interactivePane.create_text(200, 90, text=question1, font=self.font)
        self.visualizingPane.create_image(250, 250, image=self.quizQuestionMark, anchor=tk.CENTER)
        A1 = tk.Radiobutton(self.interactivePane, text="A) To lighten the image",
                            padx=20, value="A1", bg="grey", variable=self.radioVarCVQ1)
        A1.place(relx=.1, rely=.2)
        B1 = tk.Radiobutton(self.interactivePane, text="B) To change the color intensity of the image",
                            padx=20, value="B1", bg="grey", variable=self.radioVarCVQ1)
        B1.place(relx=.1, rely=.25)
        C1 = tk.Radiobutton(self.interactivePane, text="C) To remove noise from the image",
                            padx=20, value="C1", bg="grey", variable=self.radioVarCVQ1)
        C1.place(relx=.1, rely=.3)
        D1 = tk.Radiobutton(self.interactivePane, text="D) To determine which edges are true edges",
                            padx=20, value="D1", bg="grey", variable=self.radioVarCVQ1)
        D1.place(relx=.1, rely=.35)

        # QUESTION 2
        self.interactivePane.create_text(250, 235, text=question2, font=self.font)
        A2 = tk.Radiobutton(self.interactivePane,
                            text="A) It is used to determine if a point should be put to zero or not",
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
        correctAnswers = [[self.radioVarCVQ1, "D1"], [self.radioVarCVQ2, "A2"]]
        self.placeBackToMenuButton(self.visualizingPane)
        self.placeNextButton(.675, .75, pane=self.interactivePane,
                             text="Submit Quiz", font=self.label_font, command=lambda: self.checkFIRSTTest(correctAnswers))
        self.placeBackButton(.075, .75, pane=self.interactivePane, command=self.edge_detection_interactive,
                             text="ED Interactive", font=self.label_font)
        pass

    # Pass the list containing the correct answer objects (multiple choice)
    def checkFIRSTTest(self, correctAnswers):
        for answer in correctAnswers:
            if (answer[0].get() == answer[1]):
                pass
            else:
                print("Quiz Failed.")
                self.quizFailed(self.CVQuiz)
                return
        print("Quiz Passed.")
        self.quizPassed(self.projective_geometry)
        pass

    def PoseQuiz(self):
        # quizPrompt = "Let's put the knowledge you learned to the test!\n"
        #              # "Here are two questions to make sure you're understanding\n" \
        #              # "The material so far.\n"
        question1 = "1) When a camera is calibrated with respect to the world\n" \
                    "coordinate system, image points are extracted from the 2D\n" \
                    "image that correspond to what?"
        question2 = "2) How can you estimate pose through comparison?\n"
        self.gui.clearScreen()
        self.makePanes()
        self.radioVarCVQ1.set(-1)  # I think this makes it so that none are selected. Nice.
        self.radioVarCVQ2.set(-1)  # I think this makes it so that none are selected. Nice.
        # self.interactivePane.create_text(260, 50, text=quizPrompt, font=self.font)

        # QUESTION 1
        self.interactivePane.create_text(260, 50, text=question1, font=self.font)
        self.visualizingPane.create_image(250, 250, image=self.quizQuestionMark, anchor=tk.CENTER)
        A1 = tk.Radiobutton(self.interactivePane, text="A) The center",
                            padx=20, value="A1", bg="grey", variable=self.radioVarCVQ1)
        A1.place(relx=.1, rely=.2)
        B1 = tk.Radiobutton(self.interactivePane, text="B) The corners",
                            padx=20, value="B1", bg="grey", variable=self.radioVarCVQ1)
        B1.place(relx=.1, rely=.25)
        C1 = tk.Radiobutton(self.interactivePane, text="C) Black points",
                            padx=20, value="C1", bg="grey", variable=self.radioVarCVQ1)
        C1.place(relx=.1, rely=.3)
        D1 = tk.Radiobutton(self.interactivePane, text="D) The horizon",
                            padx=20, value="D1", bg="grey", variable=self.radioVarCVQ1)
        D1.place(relx=.1, rely=.35)

        # QUESTION 2
        self.interactivePane.create_text(240, 235, text=question2, font=self.font)
        A2 = tk.Radiobutton(self.interactivePane,
                            text="A) Compare camera output to a single image",
                            padx=20, value="A2", bg="grey", variable=self.radioVarCVQ2)
        A2.place(relx=.1, rely=.525)
        B2 = tk.Radiobutton(self.interactivePane, text="B) Use gradient descent",
                            padx=20, value="B2", bg="grey", variable=self.radioVarCVQ2)
        B2.place(relx=.1, rely=.575)
        C2 = tk.Radiobutton(self.interactivePane, text="C) Compare the area of the camera's object to the object's known area",
                            padx=20, value="C2", bg="grey", variable=self.radioVarCVQ2)
        C2.place(relx=.1, rely=.625)
        D2 = tk.Radiobutton(self.interactivePane, text="D) Compare camera's image obect to a database of imagegs of the \n" \
                                                        "object at various poses",
                            padx=20, value="D2", bg="grey", variable=self.radioVarCVQ2)
        D2.place(relx=.1, rely=.675)
        correctAnswers = [[self.radioVarCVQ1, "B1"], [self.radioVarCVQ2, "D2"]]
        self.placeBackToMenuButton(self.visualizingPane)
        self.placeNextButton(.675, .75, pane=self.interactivePane,
                             text="Submit Quiz", font=self.label_font, command=lambda: self.checkSECONDTest(correctAnswers))
        self.placeBackButton(.075, .75, pane=self.interactivePane, command=self.calibrated_camera_cont,
                             text="Calibrated \nCamera Cont.", font=self.label_font)
        pass

    def checkSECONDTest(self, correctAnswers):
        for answer in correctAnswers:
            if (answer[0].get() == answer[1]):
                pass
            else:
                print("Quiz Failed.")
                self.quizFailed(self.PoseQuiz)
                return
        print("Quiz Passed.")
        self.quizPassed(self.ml_intro)
        pass


    def MLQuiz(self):
        # quizPrompt = "Let's put the knowledge you learned to the test!\n"\
        #              # "Here are two questions to make sure you're understanding\n" \
        #              # "The material so far.\n"
        question1 = "1) What is training and testing data used for?\n"
        question2 = "2) How is the gradient used for f_mse?\n"
        self.gui.clearScreen()
        self.makePanes()
        self.radioVarCVQ1.set(-1)  # I think this makes it so that none are selected. Nice.
        self.radioVarCVQ2.set(-1)  # I think this makes it so that none are selected. Nice.
        # self.interactivePane.create_text(260, 50, text=quizPrompt, font=self.font)

        # QUESTION 1
        self.interactivePane.create_text(240, 75, text=question1, font=self.font)
        self.visualizingPane.create_image(250, 250, image=self.quizQuestionMark, anchor=tk.CENTER)
        A1 = tk.Radiobutton(self.interactivePane, text="A) Making more images",
                            padx=20, value="A1", bg="grey", variable=self.radioVarCVQ1)
        A1.place(relx=.1, rely=.2)
        B1 = tk.Radiobutton(self.interactivePane, text="B) Finding squirrels",
                            padx=20, value="B1", bg="grey", variable=self.radioVarCVQ1)
        B1.place(relx=.1, rely=.25)
        C1 = tk.Radiobutton(self.interactivePane, text="C) Making the model faster",
                            padx=20, value="C1", bg="grey", variable=self.radioVarCVQ1)
        C1.place(relx=.1, rely=.3)
        D1 = tk.Radiobutton(self.interactivePane, text="D) Creating weights and testing their accuracy",
                            padx=20, value="D1", bg="grey", variable=self.radioVarCVQ1)
        D1.place(relx=.1, rely=.35)

        # QUESTION 2
        self.interactivePane.create_text(210, 240, text=question2, font=self.font)
        A2 = tk.Radiobutton(self.interactivePane,
                            text="A) It gradually lightens the training images",
                            padx=20, value="A2", bg="grey", variable=self.radioVarCVQ2)
        A2.place(relx=.1, rely=.525)
        B2 = tk.Radiobutton(self.interactivePane, text="B) It finds the edges in the images",
                            padx=20, value="B2", bg="grey", variable=self.radioVarCVQ2)
        B2.place(relx=.1, rely=.575)
        C2 = tk.Radiobutton(self.interactivePane, text="C) It gets us to the global mimimum",
                            padx=20, value="C2", bg="grey", variable=self.radioVarCVQ2)
        C2.place(relx=.1, rely=.625)
        D2 = tk.Radiobutton(self.interactivePane, text="D) It decreases the weights",
                            padx=20, value="D2", bg="grey", variable=self.radioVarCVQ2)
        D2.place(relx=.1, rely=.675)
        correctAnswers = [[self.radioVarCVQ1, "D1"], [self.radioVarCVQ2, "C2"]]
        self.placeBackToMenuButton(self.visualizingPane)
        self.placeNextButton(.675, .75, pane=self.interactivePane,
                             text="Submit Quiz", font=self.label_font, command=lambda: self.checkTHIRDTest(correctAnswers))
        self.placeBackButton(.075, .75, pane=self.interactivePane, command=self.ml_data_aug,
                             text="Additional \nData", font=self.label_font)
        pass

    def checkTHIRDTest(self, correctAnswers):
        for answer in correctAnswers:
            if (answer[0].get() == answer[1]):
                pass
            else:
                print("Quiz Failed.")
                self.quizFailed(self.MLQuiz)
                return
        print("Quiz Passed.")
        self.quizPassed_module_end(self.gui.HomePage)
        pass

    def quizPassed(self, nextPage):
        self.gui.clearScreen()
        canvas = tk.Canvas(self.gui.win, width=1000, height=500, bg='grey')
        canvas.grid(row=0, column=0)
        canvas.create_image(500, 250, image=self.quizPassedImage, anchor=tk.CENTER)
        canvas.create_text(500, 50, text="Quiz Passed!", font=self.font)
        self.placeBackToMenuButton(canvas)
        self.placeNextButton(.7, .7, pane=canvas, command=nextPage, text="Next Topic!",
                             font=self.label_font)

    def quizPassed_module_end(self, nextPage):
        self.gui.clearScreen()
        canvas = tk.Canvas(self.gui.win, width=1000, height=500, bg='grey')
        canvas.grid(row=0, column=0)
        canvas.create_image(500, 250, image=self.quizPassedImage, anchor=tk.CENTER)
        canvas.create_text(500, 50, text="Final Quiz Passed!\n\nYOU'RE DONE WITH THIS MODULE!", font=self.font)
        self.placeBackToMenuButton(canvas)
        self.placeNextButton(.7, .7, pane=canvas, command=nextPage, text="Home page",
                             font=self.label_font)
        self.gui.moduleDict["Computer Vision"].completed = True

    def quizFailed(self, previousPage):
        self.gui.clearScreen()
        canvas = tk.Canvas(self.gui.win, width=1000, height=500, bg='grey')
        canvas.grid(row=0, column=0)
        canvas.create_image(500, 250, image=self.quizFailedImage, anchor=tk.CENTER)
        canvas.create_text(500, 50, text="Quiz Failed!", font=self.font)
        self.placeBackToMenuButton(canvas)
        self.placeBackButton(.1, .7, pane=canvas, command=previousPage, text="To Quiz",
                             font=self.label_font)

    def runModule(self):
        self.gui.clearScreen()
        self.makePanes()
        self.introPage()



