# Owen Smith
# 6/16/2020

from Module import Module as Mod
from PIL import ImageTk, Image
import tkinter as tk


def place_rainbow_text(text, pane, x, y, font_size):
    title_font = ('Courier', font_size, 'bold italic')
    rainbow_fill = ['red', 'dark orange', 'gold', 'green3', 'blue', 'dark violet']
    char_count = 0
    space_count = 0
    start = x
    for i in range(0, len(text)):

        char = text[i]
        if char == ' ':
            space_count += 1
        color_idx = (i - space_count) % len(rainbow_fill)
        color = rainbow_fill[color_idx]
        if char_count > 13 and char == ' ':
            y += 35
            char_count = 0
        x = start + (font_size * .8 * char_count)
        pane.create_text(x, y, anchor="nw", font=title_font, text=char, fill=color)
        char_count += 1


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
        self.button_font = ('Comic Sans MS', 6)
        self.current_page = 0
        self.page_titles = ['Robot Kinematics',
                            'Frame Transformations',
                            'Rotations',
                            'Transformation Matrices',
                            'DH Parameters',
                            'DH (Continued)',
                            'Forward Kinematics Example 1',
                            'Forward Kinematics Example 2',
                            'Law of Cosines',
                            'Arctangent and Atan2',
                            'Inverse Kinematics Example 1',
                            'Inverse Kinematics Example 2',
                            'Velocity Kinematics',
                            'Singularities',
                            'Congratulations!']
        self.page_loads = {'Robot Kinematics': self.intro_page,
                           'Frame Transformations': self.frame_trans_page,
                           'Rotations': self.rot_page,
                           'Transformation Matrices': self.trans_mat_page,
                           'DH Parameters': self.dh_page,
                           'DH (Continued)': self.dh_page2,
                           'Forward Kinematics Example 1': self.fk1_page,
                           'Forward Kinematics Example 2': self.fk2_page,
                           'Law of Cosines': self.cos_page,
                           'Arctangent and Atan2': self.atan_page,
                           'Inverse Kinematics Example 1': self.ik1_page,
                           'Inverse Kinematics Example 2': self.ik2_page,
                           'Velocity Kinematics': self.velkin_page,
                           'Singularities': self.sing_page,
                           'Congratulations!': self.congrats_page}

        image = Image.open("BluePurpleGreenStyle2.jpg")
        fit_canvas_im = image.resize((500, 500), Image.ANTIALIAS)
        self.blue_purple_bg = ImageTk.PhotoImage(fit_canvas_im)
        self.basic_frames = ImageTk.PhotoImage(Image.open("BasicFrames.jpg"))
        self.basic_rotations = ImageTk.PhotoImage(Image.open("rotations.png"))
        self.trans_matrix = ImageTk.PhotoImage(Image.open("TransMatFrames.png"))
        image2 = Image.open("robot1_dh_z.png")
        image3 = Image.open("robot1_dh_x.png")
        image4 = Image.open("robot1_full_dh.png")
        resize2 = image2.resize((200, 200), Image.ANTIALIAS)
        resize3 = image3.resize((200, 200), Image.ANTIALIAS)
        resize4 = image4.resize((175, 175), Image.ANTIALIAS)
        self.rob1_z = ImageTk.PhotoImage(resize2)
        self.rob1_x = ImageTk.PhotoImage(resize3)
        self.rob1_full = ImageTk.PhotoImage(resize4)
        self.dh_show = ImageTk.PhotoImage(Image.open("exampleDH.png"))
        self.param_mat = ImageTk.PhotoImage(Image.open("DH_parameterized.png"))
        self.planar2D = ImageTk.PhotoImage(Image.open("2DPlanar.png"))
        self.RRR3D = ImageTk.PhotoImage(Image.open("3DRRR.png"))
        self.cos = ImageTk.PhotoImage(Image.open("lawOfcosines.png").resize((440, 400), Image.ANTIALIAS))
        self.sincos = ImageTk.PhotoImage(Image.open("sincos.png").resize((470, 120), Image.ANTIALIAS))
        self.atan2_im = ImageTk.PhotoImage(Image.open("atan2.png").resize((480, 125), Image.ANTIALIAS))
        self.D = ImageTk.PhotoImage(Image.open("D.png").resize((400, 250), Image.ANTIALIAS))
        self.ikin_ex1 = ImageTk.PhotoImage(Image.open("2DPlanarIKin.png").resize((400, 250), Image.ANTIALIAS))
        self.ikin_ex2 = ImageTk.PhotoImage(Image.open("3DIKin.png").resize((400, 400), Image.ANTIALIAS))

        self.interactive_text_x = 255
        self.interactive_text_y = 100

        self.debug = True

        self.backButton = None
        self.nextButton = None

    def makePanes(self):
        self.interactivePane = tk.Canvas(self.gui.win, width=500, height=500, bg='gainsboro')
        self.visualizingPane = tk.Canvas(self.gui.win, width=500, height=500, bg='gainsboro')
        self.interactivePane.grid(row=0, column=0)
        self.visualizingPane.grid(row=0, column=1)

    def runModule(self):
        self.gui.clearScreen()
        self.makePanes()
        # This is to get around having the +1 in load next page
        self.current_page = -1
        self.load_next_page()

    def intro_page(self):
        self.interactivePane.create_text(self.interactive_text_x, self.interactive_text_y,
                                         text="This module covers the breadth of topics necessary to\n "
                                              "form an introductory understanding of forward and\n"
                                              "inverse position kinematics for serial (i.e. armed) robots.\n"
                                              "It begins with a discussion of basic frame transformations\n"
                                              "and transitions to a discussion of transformation matrices.\n"
                                              "These form the basis needed to dive into forward kinematics\n"
                                              "and to introduce Denavit-Hartenburg (DH) parameters. Then\n"
                                              "geometric inverse kinematics are covered using the law of\n"
                                              "cosines and the atan2 function. Lastly, the Jacobian, velocity"
                                              "\nkinematics and singularities are covered.",
                                         font=self.font,
                                         anchor='n')

    def frame_trans_page(self):
        if not self.debug:
            self.nextButton["state"] = 'disabled'
        self.interactivePane.create_text(self.interactive_text_x, self.interactive_text_y,
                                         text="Frame transformations are the building blocks for robot\n"
                                              "kinematics and are closely associated with transformation.\n"
                                              "A reference frame is a coordinate system positioned in space"
                                              "\nat a defined position and orientation from which standardized"
                                              "\nmeasurements can be made. Therefore, a conversion\n"
                                              "between frames must be defined by a deviation in these\n"
                                              "measures. Position displacement is an easy concept as it is\n"
                                              "essentially the same as defining a point in a coordinate frame,"
                                              "\nbut rotations, which will be covered in the next section, can\n"
                                              "get tricky."
                                              "\n     Test your understanding of position displacement below!\n"
                                              "         (The answer will use only integer values)",
                                         font=self.font,
                                         anchor='n')
        ans_x, ans_y = '3', '2'
        x_check = y_check = False
        x = tk.StringVar()
        y = tk.StringVar()

        X_entry = tk.Entry(self.interactivePane, textvariable=x, font=('Comic Sans MS', 18, 'bold italic'), width=5)
        Y_entry = tk.Entry(self.interactivePane, textvariable=y, font=('Comic Sans MS', 18, 'bold italic'), width=5)

        X_entry.place(anchor=tk.S, relx=.5, rely=.85)
        Y_entry.place(anchor=tk.S, relx=.5, rely=.92)
        x.set('X')
        y.set('Y')
        x.trace('w',
                lambda a, b, c: self.check_frame_trans([x, y], [x_check, y_check], [ans_x, ans_y],
                                                       [X_entry, Y_entry]))
        y.trace('w',
                lambda a, b, c: self.check_frame_trans([x, y], [x_check, y_check], [ans_x, ans_y],
                                                       [X_entry, Y_entry]))
        self.visualizingPane.update()
        w = self.visualizingPane.winfo_width()
        h = self.visualizingPane.winfo_height()
        self.visualizingPane.create_image(w / 2, h / 2, image=self.basic_frames, anchor=tk.CENTER)

    def check_frame_trans(self, vals, checks, ans, entries):
        if vals[0].get() == ans[0]:
            checks[0] = True
            entries[0]['bg'] = 'chartreuse2'
        elif vals[0].get() != 'X':
            entries[0]['bg'] = 'firebrick1'
        if vals[1].get() == ans[1]:
            checks[1] = True
            entries[1]['bg'] = 'chartreuse2'
        elif vals[1].get() != 'Y':
            entries[1]['bg'] = 'firebrick1'

        if checks[0] and checks[1]:
            self.nextButton.config(state='normal')

    def rot_page(self):
        self.interactivePane.create_text(self.interactive_text_x, self.interactive_text_y - 45,
                                         text="Rotations with respect to a reference frame are best described"
                                              "\nby a rotation matrix. A rotation matrix represents the angle\n"
                                              "of the new frame’s axes with respect to the previous frame’s\n"
                                              "axes. Rotation matrices are square and their dimensions are\n"
                                              "dependent on the dimensions of the application (most often\n"
                                              "3x3 for 3D spaces). Their columns describe the projection of\n"
                                              "the new axes along the old set of axes.\n"
                                              "                     R = \n"
                                              "                     [ X_x, Y_x, Z_x]\n"
                                              "                     [ X_y, Y_y, Z_y]\n"
                                              "                     [ X_z, Y_z, Z_z]\n"
                                              "The first column describes how much of X can be projected\n"
                                              "onto each of the old X, Y, and Z. This concept applies in the\n"
                                              "same way to the other columns for the new Y and Z. Rotation",
                                         font=self.font,
                                         anchor='n')
        self.visualizingPane.create_text(self.interactive_text_x, 15,
                                         text="\nmatrices have some unique properties that make them a part"
                                              "\nof the Special Orthogonal group. This group of matrices have"
                                              "\nmutually orthogonal column vectors of unit length. Because\n"
                                              "of this designation, the inverse of a rotation matrix is equal to"
                                              "\nits transpose and also inverts the relationship defined by the"
                                              "\nrotation matrix. This means that a rotation matrix describing"
                                              "\nthe transformation from frame A to frame B can easily be\n"
                                              "changed to describe the transformation from frame B to frame"
                                              "\nA by just taking its transpose.\n"
                                              "                         R_AB.T= R_BA\n"
                                              "Rotation matrices can be used with point vectors to shift the\n"
                                              "point’s reference frame to a new rotated frame. Additionally,\n"
                                              "rotation matrices can be multiplied together to create new \n"
                                              "matrices that describe both rotations in one matrix.\n"
                                              "              p0 = R_10*p1    p2 = R_01*R_12*p0\n\n"
                                              "These are the generic single axis rotation matrices:",
                                         font=self.font,
                                         anchor='n')
        self.visualizingPane.update()
        w = self.visualizingPane.winfo_width()
        h = self.visualizingPane.winfo_height()
        self.visualizingPane.create_image(w / 2, .9 * h, image=self.basic_rotations, anchor=tk.CENTER)

    def trans_mat_page(self):
        if not self.debug:
            self.nextButton["state"] = 'disabled'
        self.interactivePane.create_text(self.interactive_text_x, self.interactive_text_y,
                                         text="This powerful tool allows positions and orientations to be\n"
                                              "converted simultaneously between reference frames.\n"
                                              "Transformation matrices are 4x4 square matrices made up of\n"
                                              "a 3x1 position vector, a 3x3 rotation matrix, and a bottom row\n"
                                              "of [0, 0, 0, 1]. Yes, always that.\n"
                                              "                         T = [R p]\n"
                                              "                             [0 1]\n"
                                              "A transformation matrix from frame A to frame B is written as\n"
                                              "T_BA. The inverse of a transformation matrix defines the\n"
                                              "opposite relationship, similar to rotation matrices (i.e. T_BA =\n"
                                              "inv(T_AB). Additionally the inverse of a transformation matrix\n"
                                              "can be found in pieces in place of the usual approach.\n"
                                              "                     inv(T) = [R.T -R.T*p]\n"
                                              "                              [0	 1]\n",
                                         font=self.font,
                                         anchor='n')
        self.visualizingPane.create_text(self.interactive_text_x, 20,
                                         text="Test your understanding so far by building the transformation\n"
                                              "matrix for frame A to frame B. Remember that each row and\n"
                                              "column of the rotation matrix should add up to 1!\n",
                                         font=self.font,
                                         anchor='n')

        check_T = [[False, False, False, False],
                   [False, False, False, False],
                   [False, False, False, False]]
        rxx = tk.StringVar()
        rxy = tk.StringVar()
        rxz = tk.StringVar()
        ryx = tk.StringVar()
        ryy = tk.StringVar()
        ryz = tk.StringVar()
        rzx = tk.StringVar()
        rzy = tk.StringVar()
        rzz = tk.StringVar()
        px = tk.StringVar()
        py = tk.StringVar()
        pz = tk.StringVar()

        RXX_entry = tk.Entry(self.visualizingPane, textvariable=rxx, font=('Comic Sans MS', 11, 'bold italic'), width=5)
        RXY_entry = tk.Entry(self.visualizingPane, textvariable=rxy, font=('Comic Sans MS', 11, 'bold italic'), width=5)
        RXZ_entry = tk.Entry(self.visualizingPane, textvariable=rxz, font=('Comic Sans MS', 11, 'bold italic'), width=5)

        RYX_entry = tk.Entry(self.visualizingPane, textvariable=ryx, font=('Comic Sans MS', 11, 'bold italic'), width=5)
        RYY_entry = tk.Entry(self.visualizingPane, textvariable=ryy, font=('Comic Sans MS', 11, 'bold italic'), width=5)
        RYZ_entry = tk.Entry(self.visualizingPane, textvariable=ryz, font=('Comic Sans MS', 11, 'bold italic'), width=5)

        RZX_entry = tk.Entry(self.visualizingPane, textvariable=rzx, font=('Comic Sans MS', 11, 'bold italic'), width=5)
        RZY_entry = tk.Entry(self.visualizingPane, textvariable=rzy, font=('Comic Sans MS', 11, 'bold italic'), width=5)
        RZZ_entry = tk.Entry(self.visualizingPane, textvariable=rzz, font=('Comic Sans MS', 11, 'bold italic'), width=5)

        PX_entry = tk.Entry(self.visualizingPane, textvariable=px, font=('Comic Sans MS', 11, 'bold italic'), width=5)
        PY_entry = tk.Entry(self.visualizingPane, textvariable=py, font=('Comic Sans MS', 11, 'bold italic'), width=5)
        PZ_entry = tk.Entry(self.visualizingPane, textvariable=pz, font=('Comic Sans MS', 11, 'bold italic'), width=5)

        col1_rel, col2_rel, col3_rel, col4_rel = .35, .45, .55, .65
        row1_rel, row2_rel, row3_rel = .23, .28, .33
        RXX_entry.place(anchor=tk.S, relx=col1_rel, rely=row1_rel)
        RXY_entry.place(anchor=tk.S, relx=col1_rel, rely=row2_rel)
        RXZ_entry.place(anchor=tk.S, relx=col1_rel, rely=row3_rel)

        RYX_entry.place(anchor=tk.S, relx=col2_rel, rely=row1_rel)
        RYY_entry.place(anchor=tk.S, relx=col2_rel, rely=row2_rel)
        RYZ_entry.place(anchor=tk.S, relx=col2_rel, rely=row3_rel)

        RZX_entry.place(anchor=tk.S, relx=col3_rel, rely=row1_rel)
        RZY_entry.place(anchor=tk.S, relx=col3_rel, rely=row2_rel)
        RZZ_entry.place(anchor=tk.S, relx=col3_rel, rely=row3_rel)

        PX_entry.place(anchor=tk.S, relx=col4_rel, rely=row1_rel)
        PY_entry.place(anchor=tk.S, relx=col4_rel, rely=row2_rel)
        PZ_entry.place(anchor=tk.S, relx=col4_rel, rely=row3_rel)

        rxx.set('RXx')
        rxy.set('RXy')
        rxz.set('RXz')
        ryx.set('RYx')
        ryy.set('RYy')
        ryz.set('RYz')
        rzx.set('RZx')
        rzy.set('RZy')
        rzz.set('RZz')
        px.set('Px')
        py.set('Py')
        pz.set('Pz')

        entries_T = [[RXX_entry, RYX_entry, RZX_entry, PX_entry],
                     [RXY_entry, RYY_entry, RZY_entry, PY_entry],
                     [RXZ_entry, RYZ_entry, RZZ_entry, PZ_entry]]
        rxx.trace('w',
                  lambda a, b, c: self.check_trans_mat(check_T, entries_T))
        rxy.trace('w',
                  lambda a, b, c: self.check_trans_mat(check_T, entries_T))
        rxz.trace('w',
                  lambda a, b, c: self.check_trans_mat(check_T, entries_T))
        ryx.trace('w',
                  lambda a, b, c: self.check_trans_mat(check_T, entries_T))
        ryy.trace('w',
                  lambda a, b, c: self.check_trans_mat(check_T, entries_T))
        ryz.trace('w',
                  lambda a, b, c: self.check_trans_mat(check_T, entries_T))
        rzx.trace('w',
                  lambda a, b, c: self.check_trans_mat(check_T, entries_T))
        rzy.trace('w',
                  lambda a, b, c: self.check_trans_mat(check_T, entries_T))
        rzz.trace('w',
                  lambda a, b, c: self.check_trans_mat(check_T, entries_T))
        px.trace('w',
                 lambda a, b, c: self.check_trans_mat(check_T, entries_T))
        py.trace('w',
                 lambda a, b, c: self.check_trans_mat(check_T, entries_T))
        pz.trace('w',
                 lambda a, b, c: self.check_trans_mat(check_T, entries_T))

        self.visualizingPane.update()
        w = self.visualizingPane.winfo_width()
        h = self.visualizingPane.winfo_height()
        self.visualizingPane.create_image(w / 2, .65 * h, image=self.trans_matrix, anchor=tk.CENTER)

    def check_trans_mat(self, check_T, entries_T):
        ans_T = [('0', '-1', '0', '5'),
                 ('1', '0', '0', '2'),
                 ('0', '0', '1', '0')]

        for i in range(0, 3):
            for j in range(0, 4):
                if entries_T[i][j].get() == ans_T[i][j]:
                    check_T[i][j] = True
                    entries_T[i][j]['bg'] = 'chartreuse2'
                else:
                    check_T[i][j] = False
                    entries_T[i][j]['bg'] = 'firebrick1'
        if check_T:
            self.nextButton.config(state='normal')

    def dh_page(self):
        self.interactivePane.create_text(self.interactive_text_x, self.interactive_text_y - 45,
                                         text="Denavit-Hartenberg parameters are a standardized approach\n"
                                              "to establishing reference frame positions and orientations to\n"
                                              "describe a n-DOF (degree of freedom) armed robot. With\n"
                                              "standardized reference frames, separate people can develop\n"
                                              "the same equations for forward kinematics. Forward\n"
                                              "kinematics is determining the position of the\n"
                                              "end-effector, or tip, of the robot when given the joint variables\n"
                                              "of the robot. There are two types of joints in armed robots:\n"
                                              "rotational and prismatic. Rotational joints are described by a\n"
                                              "theta (angular position) and prismatic joints are described by\n"
                                              "a displacement, d, (linear position). Determination of DH\n"
                                              "parameters follows three steps: z-axis assignment, x-axis\n"
                                              "assignment, DH table construction.\n"
                                         ,
                                         font=self.font,
                                         anchor='n')
        self.visualizingPane.create_text(self.interactive_text_x, 20,
                                         text="Z-axis assignment is placing the z axes for each\n"
                                              "reference frame. For a rotational joint, the z axis for the\n"
                                              "representative reference frame will be coincident with the axis"
                                              "\nof rotation. For a prismatic joint, the z axis will be coincident"
                                              "\nwith the axis of translation. The end-effector frame should"
                                              "\nhave the z axis pointing out along the end-effector.\n"
                                              "   X axis assignment is placing the x axes for each\n"
                                              "reference frame. The x axis of the first frame is a free choice,\n"
                                              "and so can be placed in any orthogonal direction to the first z\n"
                                              "axis. For all following reference frames, the x axis must lie in\n"
                                              "the shortest orthogonal direction between the current and\n"
                                              "previous z axes."
                                         ,
                                         font=self.font,
                                         anchor='n')
        self.visualizingPane.update()
        w = self.visualizingPane.winfo_width()
        h = self.visualizingPane.winfo_height()
        self.visualizingPane.create_image(w / 4, .78 * h, image=self.rob1_z, anchor=tk.CENTER)
        self.visualizingPane.create_image(3 * w / 4, .78 * h, image=self.rob1_x, anchor=tk.CENTER)

    def dh_page2(self):
        self.interactivePane.create_text(self.interactive_text_x, self.interactive_text_y - 45,
                                         text="DH table construction consists of defining four values\n"
                                              "for every link of the robot. These four values are theta, d, a,\n"
                                              "and alpha. The values describe the transformations necessary\n"
                                              "to move from frame i to frame i+1. Theta describes any rotation\n"
                                              "around the z axis in radians; d describes any translation along\n"
                                              "the z axis; a describes any translation along the x axis; and\n"
                                              "alpha describes any rotation around the x axis in radians. They\n"
                                              "must all occur in the given order (theta, d, a, and then alpha).\n"
                                              "This means that every transformation will be defined by a\n"
                                              "Rot(z), Trans(d), Trans(a), and Rot(x). These correspond to\n"
                                              "the simple, one function transformation matrices noted earlier.\n"
                                              "However, instead of doing the matrix multiplication every time\n"
                                              "there is also a precomputed matrix into which\n"
                                              "one can simply plug the DH parameters.\n"
                                         ,
                                         font=self.font,
                                         anchor='n')
        self.visualizingPane.update()
        w = self.visualizingPane.winfo_width()
        h = self.visualizingPane.winfo_height()
        self.visualizingPane.create_image(w / 2, .14 * h, image=self.param_mat, anchor=tk.CENTER)

        self.visualizingPane.create_text(self.interactive_text_x, 135,
                                         text="This matrix will describe the transformation from frame i-1 to i\n"
                                              "and will be parameterized by the appropriate joint variable,\n"
                                              "theta or d, for the given joint at i-1. Then, to describe the\n"
                                              "transformation from the base frame to the end-effector just\n"
                                              "multiply each transformation matrix in numerical order\n"
                                              "(e.g. T03 = T01*T12*T23). An example DH table and the 2 link\n"
                                              "RP (rotational, prismatic) robot it describes can be\n"
                                              "seen below. See if you can come to the same conclusion!",
                                         font=self.font,
                                         anchor='n')
        self.visualizingPane.create_image(2 * w / 9, .8 * h, image=self.rob1_full, anchor=tk.CENTER)
        self.visualizingPane.create_image(3 * w / 5, .86 * h, image=self.dh_show, anchor=tk.CENTER)

    def fk1_page(self):
        self.interactivePane.create_text(self.interactive_text_x, self.interactive_text_y,
                                         text="Fill in the DH table for this 2DOF RR Planar robot. Then write\n"
                                              "out the transformation matrix corresponding to the first row of\n"
                                              "the table if l1=l2=5, t1=t2=0. Write decimals out to 3 places.",
                                         font=self.font,
                                         anchor='n')

        self.visualizingPane.update()
        w = self.visualizingPane.winfo_width()
        h = self.visualizingPane.winfo_height()
        self.visualizingPane.create_image(w / 2, h / 2, image=self.planar2D, anchor=tk.CENTER)

        self.interactivePane.create_text(self.interactive_text_x, self.interactive_text_y + 80,
                                         text="θ      d      a     α",
                                         font=self.font,
                                         anchor='n')
        dh11 = tk.StringVar()
        dh12 = tk.StringVar()
        dh13 = tk.StringVar()
        dh14 = tk.StringVar()
        dh21 = tk.StringVar()
        dh22 = tk.StringVar()
        dh23 = tk.StringVar()
        dh24 = tk.StringVar()

        entry11 = tk.Entry(self.interactivePane, textvariable=dh11, font=('Comic Sans MS', 11, 'bold italic'), width=5)
        entry12 = tk.Entry(self.interactivePane, textvariable=dh12, font=('Comic Sans MS', 11, 'bold italic'), width=5)
        entry13 = tk.Entry(self.interactivePane, textvariable=dh13, font=('Comic Sans MS', 11, 'bold italic'), width=5)
        entry14 = tk.Entry(self.interactivePane, textvariable=dh14, font=('Comic Sans MS', 11, 'bold italic'), width=5)
        entry21 = tk.Entry(self.interactivePane, textvariable=dh21, font=('Comic Sans MS', 11, 'bold italic'), width=5)
        entry22 = tk.Entry(self.interactivePane, textvariable=dh22, font=('Comic Sans MS', 11, 'bold italic'), width=5)
        entry23 = tk.Entry(self.interactivePane, textvariable=dh23, font=('Comic Sans MS', 11, 'bold italic'), width=5)
        entry24 = tk.Entry(self.interactivePane, textvariable=dh24, font=('Comic Sans MS', 11, 'bold italic'), width=5)

        entries_dh = [[entry11, entry12, entry13, entry14],
                      [entry21, entry22, entry23, entry24]]
        check_T = [[False, False, False, False],
                   [False, False, False, False]]

        dh11.trace('w',
                   lambda a, b, c: self.check_dh_1(check_T, entries_dh))
        dh12.trace('w',
                   lambda a, b, c: self.check_dh_1(check_T, entries_dh))
        dh13.trace('w',
                   lambda a, b, c: self.check_dh_1(check_T, entries_dh))
        dh14.trace('w',
                   lambda a, b, c: self.check_dh_1(check_T, entries_dh))
        dh21.trace('w',
                   lambda a, b, c: self.check_dh_1(check_T, entries_dh))
        dh22.trace('w',
                   lambda a, b, c: self.check_dh_1(check_T, entries_dh))
        dh23.trace('w',
                   lambda a, b, c: self.check_dh_1(check_T, entries_dh))
        dh24.trace('w',
                   lambda a, b, c: self.check_dh_1(check_T, entries_dh))

        col1_rel, col2_rel, col3_rel, col4_rel = .35, .45, .55, .65
        row1_rel, row2_rel = .45, .50
        entry11.place(anchor=tk.S, relx=col1_rel, rely=row1_rel)
        entry12.place(anchor=tk.S, relx=col2_rel, rely=row1_rel)
        entry13.place(anchor=tk.S, relx=col3_rel, rely=row1_rel)
        entry14.place(anchor=tk.S, relx=col4_rel, rely=row1_rel)
        entry21.place(anchor=tk.S, relx=col1_rel, rely=row2_rel)
        entry22.place(anchor=tk.S, relx=col2_rel, rely=row2_rel)
        entry23.place(anchor=tk.S, relx=col3_rel, rely=row2_rel)
        entry24.place(anchor=tk.S, relx=col4_rel, rely=row2_rel)

        check_TT = [[False, False, False, False],
                    [False, False, False, False],
                    [False, False, False, False]]

        rxx = tk.StringVar()
        rxy = tk.StringVar()
        rxz = tk.StringVar()
        ryx = tk.StringVar()
        ryy = tk.StringVar()
        ryz = tk.StringVar()
        rzx = tk.StringVar()
        rzy = tk.StringVar()
        rzz = tk.StringVar()
        px = tk.StringVar()
        py = tk.StringVar()
        pz = tk.StringVar()

        RXX_entry = tk.Entry(self.interactivePane, textvariable=rxx, font=('Comic Sans MS', 11, 'bold italic'), width=5)
        RXY_entry = tk.Entry(self.interactivePane, textvariable=rxy, font=('Comic Sans MS', 11, 'bold italic'), width=5)
        RXZ_entry = tk.Entry(self.interactivePane, textvariable=rxz, font=('Comic Sans MS', 11, 'bold italic'), width=5)

        RYX_entry = tk.Entry(self.interactivePane, textvariable=ryx, font=('Comic Sans MS', 11, 'bold italic'), width=5)
        RYY_entry = tk.Entry(self.interactivePane, textvariable=ryy, font=('Comic Sans MS', 11, 'bold italic'), width=5)
        RYZ_entry = tk.Entry(self.interactivePane, textvariable=ryz, font=('Comic Sans MS', 11, 'bold italic'), width=5)

        RZX_entry = tk.Entry(self.interactivePane, textvariable=rzx, font=('Comic Sans MS', 11, 'bold italic'), width=5)
        RZY_entry = tk.Entry(self.interactivePane, textvariable=rzy, font=('Comic Sans MS', 11, 'bold italic'), width=5)
        RZZ_entry = tk.Entry(self.interactivePane, textvariable=rzz, font=('Comic Sans MS', 11, 'bold italic'), width=5)

        PX_entry = tk.Entry(self.interactivePane, textvariable=px, font=('Comic Sans MS', 11, 'bold italic'), width=5)
        PY_entry = tk.Entry(self.interactivePane, textvariable=py, font=('Comic Sans MS', 11, 'bold italic'), width=5)
        PZ_entry = tk.Entry(self.interactivePane, textvariable=pz, font=('Comic Sans MS', 11, 'bold italic'), width=5)

        col1_rel, col2_rel, col3_rel, col4_rel = .35, .45, .55, .65
        row1_rel, row2_rel, row3_rel = .63, .68, .73
        RXX_entry.place(anchor=tk.S, relx=col1_rel, rely=row1_rel)
        RXY_entry.place(anchor=tk.S, relx=col1_rel, rely=row2_rel)
        RXZ_entry.place(anchor=tk.S, relx=col1_rel, rely=row3_rel)

        RYX_entry.place(anchor=tk.S, relx=col2_rel, rely=row1_rel)
        RYY_entry.place(anchor=tk.S, relx=col2_rel, rely=row2_rel)
        RYZ_entry.place(anchor=tk.S, relx=col2_rel, rely=row3_rel)

        RZX_entry.place(anchor=tk.S, relx=col3_rel, rely=row1_rel)
        RZY_entry.place(anchor=tk.S, relx=col3_rel, rely=row2_rel)
        RZZ_entry.place(anchor=tk.S, relx=col3_rel, rely=row3_rel)

        PX_entry.place(anchor=tk.S, relx=col4_rel, rely=row1_rel)
        PY_entry.place(anchor=tk.S, relx=col4_rel, rely=row2_rel)
        PZ_entry.place(anchor=tk.S, relx=col4_rel, rely=row3_rel)

        rxx.set('RXx')
        rxy.set('RXy')
        rxz.set('RXz')
        ryx.set('RYx')
        ryy.set('RYy')
        ryz.set('RYz')
        rzx.set('RZx')
        rzy.set('RZy')
        rzz.set('RZz')
        px.set('Px')
        py.set('Py')
        pz.set('Pz')

        entries_T = [[RXX_entry, RYX_entry, RZX_entry, PX_entry],
                     [RXY_entry, RYY_entry, RZY_entry, PY_entry],
                     [RXZ_entry, RYZ_entry, RZZ_entry, PZ_entry]]
        rxx.trace('w',
                  lambda a, b, c: self.check_fk_ex1(check_TT, entries_T))
        rxy.trace('w',
                  lambda a, b, c: self.check_fk_ex1(check_TT, entries_T))
        rxz.trace('w',
                  lambda a, b, c: self.check_fk_ex1(check_TT, entries_T))
        ryx.trace('w',
                  lambda a, b, c: self.check_fk_ex1(check_TT, entries_T))
        ryy.trace('w',
                  lambda a, b, c: self.check_fk_ex1(check_TT, entries_T))
        ryz.trace('w',
                  lambda a, b, c: self.check_fk_ex1(check_TT, entries_T))
        rzx.trace('w',
                  lambda a, b, c: self.check_fk_ex1(check_TT, entries_T))
        rzy.trace('w',
                  lambda a, b, c: self.check_fk_ex1(check_TT, entries_T))
        rzz.trace('w',
                  lambda a, b, c: self.check_fk_ex1(check_TT, entries_T))
        px.trace('w',
                 lambda a, b, c: self.check_fk_ex1(check_TT, entries_T))
        py.trace('w',
                 lambda a, b, c: self.check_fk_ex1(check_TT, entries_T))
        pz.trace('w',
                 lambda a, b, c: self.check_fk_ex1(check_TT, entries_T))

    def check_dh_1(self, check_T, entries_T):
        ans_T = [('t1', '0', 'l1', '0'),
                 ('t2', '0', 'l2', '0')]

        for i in range(0, 2):
            for j in range(0, 3):
                if entries_T[i][j].get() == ans_T[i][j]:
                    check_T[i][j] = True
                    entries_T[i][j]['bg'] = 'chartreuse2'
                else:
                    check_T[i][j] = False
                    entries_T[i][j]['bg'] = 'firebrick1'
        if check_T:
            self.nextButton.config(state='normal')

    def check_fk_ex1(self, check_T, entries_T):
        ans_T = [('1', '0', '0', '5'),
                 ('0', '1', '0', '0'),
                 ('0', '0', '1', '0')]

        for i in range(0, 3):
            for j in range(0, 4):
                if entries_T[i][j].get() == ans_T[i][j]:
                    check_T[i][j] = True
                    entries_T[i][j]['bg'] = 'chartreuse2'
                else:
                    check_T[i][j] = False
                    entries_T[i][j]['bg'] = 'firebrick1'
        if check_T:
            self.nextButton.config(state='normal')

    def fk2_page(self):
        self.interactivePane.create_text(self.interactive_text_x, self.interactive_text_y,
                                         text="Fill in the DH table for this 3DOF RRR robot. Then write\n"
                                              "out the transformation matrix corresponding to the third row of\n"
                                              "the table if l1=l2=5, t1=t2=t3=π/2. Write joint variables as\n"
                                              "'tn' (i.e. t1, t2) and π as pi.",
                                         font=self.font,
                                         anchor='n')

        self.visualizingPane.update()
        w = self.visualizingPane.winfo_width()
        h = self.visualizingPane.winfo_height()
        self.visualizingPane.create_image(w / 2, h / 2, image=self.RRR3D, anchor=tk.CENTER)

        self.interactivePane.create_text(self.interactive_text_x, self.interactive_text_y + 85,
                                         text="θ      d      a     α",
                                         font=self.font,
                                         anchor='n')
        dh11 = tk.StringVar()
        dh12 = tk.StringVar()
        dh13 = tk.StringVar()
        dh14 = tk.StringVar()
        dh21 = tk.StringVar()
        dh22 = tk.StringVar()
        dh23 = tk.StringVar()
        dh24 = tk.StringVar()
        dh31 = tk.StringVar()
        dh32 = tk.StringVar()
        dh33 = tk.StringVar()
        dh34 = tk.StringVar()

        entry11 = tk.Entry(self.interactivePane, textvariable=dh11, font=('Comic Sans MS', 11, 'bold italic'), width=5)
        entry12 = tk.Entry(self.interactivePane, textvariable=dh12, font=('Comic Sans MS', 11, 'bold italic'), width=5)
        entry13 = tk.Entry(self.interactivePane, textvariable=dh13, font=('Comic Sans MS', 11, 'bold italic'), width=5)
        entry14 = tk.Entry(self.interactivePane, textvariable=dh14, font=('Comic Sans MS', 11, 'bold italic'), width=5)
        entry21 = tk.Entry(self.interactivePane, textvariable=dh21, font=('Comic Sans MS', 11, 'bold italic'), width=5)
        entry22 = tk.Entry(self.interactivePane, textvariable=dh22, font=('Comic Sans MS', 11, 'bold italic'), width=5)
        entry23 = tk.Entry(self.interactivePane, textvariable=dh23, font=('Comic Sans MS', 11, 'bold italic'), width=5)
        entry24 = tk.Entry(self.interactivePane, textvariable=dh24, font=('Comic Sans MS', 11, 'bold italic'), width=5)
        entry31 = tk.Entry(self.interactivePane, textvariable=dh31, font=('Comic Sans MS', 11, 'bold italic'), width=5)
        entry32 = tk.Entry(self.interactivePane, textvariable=dh32, font=('Comic Sans MS', 11, 'bold italic'), width=5)
        entry33 = tk.Entry(self.interactivePane, textvariable=dh33, font=('Comic Sans MS', 11, 'bold italic'), width=5)
        entry34 = tk.Entry(self.interactivePane, textvariable=dh34, font=('Comic Sans MS', 11, 'bold italic'), width=5)

        entries_dh = [[entry11, entry12, entry13, entry14],
                      [entry21, entry22, entry23, entry24]]
        check_T = [[False, False, False, False],
                   [False, False, False, False],
                   [False, False, False, False]]

        dh11.trace('w',
                   lambda a, b, c: self.check_dh_2(check_T, entries_dh))
        dh12.trace('w',
                   lambda a, b, c: self.check_dh_2(check_T, entries_dh))
        dh13.trace('w',
                   lambda a, b, c: self.check_dh_2(check_T, entries_dh))
        dh14.trace('w',
                   lambda a, b, c: self.check_dh_2(check_T, entries_dh))
        dh21.trace('w',
                   lambda a, b, c: self.check_dh_2(check_T, entries_dh))
        dh22.trace('w',
                   lambda a, b, c: self.check_dh_2(check_T, entries_dh))
        dh23.trace('w',
                   lambda a, b, c: self.check_dh_2(check_T, entries_dh))
        dh24.trace('w',
                   lambda a, b, c: self.check_dh_2(check_T, entries_dh))
        dh31.trace('w',
                   lambda a, b, c: self.check_dh_2(check_T, entries_dh))
        dh32.trace('w',
                   lambda a, b, c: self.check_dh_2(check_T, entries_dh))
        dh33.trace('w',
                   lambda a, b, c: self.check_dh_2(check_T, entries_dh))
        dh34.trace('w',
                   lambda a, b, c: self.check_dh_2(check_T, entries_dh))

        col1_rel, col2_rel, col3_rel, col4_rel = .35, .45, .55, .65
        row1_rel, row2_rel, row3_rel = .48, .53, .58
        entry11.place(anchor=tk.S, relx=col1_rel, rely=row1_rel)
        entry12.place(anchor=tk.S, relx=col2_rel, rely=row1_rel)
        entry13.place(anchor=tk.S, relx=col3_rel, rely=row1_rel)
        entry14.place(anchor=tk.S, relx=col4_rel, rely=row1_rel)
        entry21.place(anchor=tk.S, relx=col1_rel, rely=row2_rel)
        entry22.place(anchor=tk.S, relx=col2_rel, rely=row2_rel)
        entry23.place(anchor=tk.S, relx=col3_rel, rely=row2_rel)
        entry24.place(anchor=tk.S, relx=col4_rel, rely=row2_rel)
        entry31.place(anchor=tk.S, relx=col1_rel, rely=row3_rel)
        entry32.place(anchor=tk.S, relx=col2_rel, rely=row3_rel)
        entry33.place(anchor=tk.S, relx=col3_rel, rely=row3_rel)
        entry34.place(anchor=tk.S, relx=col4_rel, rely=row3_rel)

        check_TT = [[False, False, False, False],
                    [False, False, False, False],
                    [False, False, False, False]]

        rxx = tk.StringVar()
        rxy = tk.StringVar()
        rxz = tk.StringVar()
        ryx = tk.StringVar()
        ryy = tk.StringVar()
        ryz = tk.StringVar()
        rzx = tk.StringVar()
        rzy = tk.StringVar()
        rzz = tk.StringVar()
        px = tk.StringVar()
        py = tk.StringVar()
        pz = tk.StringVar()

        RXX_entry = tk.Entry(self.interactivePane, textvariable=rxx, font=('Comic Sans MS', 11, 'bold italic'), width=5)
        RXY_entry = tk.Entry(self.interactivePane, textvariable=rxy, font=('Comic Sans MS', 11, 'bold italic'), width=5)
        RXZ_entry = tk.Entry(self.interactivePane, textvariable=rxz, font=('Comic Sans MS', 11, 'bold italic'), width=5)

        RYX_entry = tk.Entry(self.interactivePane, textvariable=ryx, font=('Comic Sans MS', 11, 'bold italic'), width=5)
        RYY_entry = tk.Entry(self.interactivePane, textvariable=ryy, font=('Comic Sans MS', 11, 'bold italic'), width=5)
        RYZ_entry = tk.Entry(self.interactivePane, textvariable=ryz, font=('Comic Sans MS', 11, 'bold italic'), width=5)

        RZX_entry = tk.Entry(self.interactivePane, textvariable=rzx, font=('Comic Sans MS', 11, 'bold italic'), width=5)
        RZY_entry = tk.Entry(self.interactivePane, textvariable=rzy, font=('Comic Sans MS', 11, 'bold italic'), width=5)
        RZZ_entry = tk.Entry(self.interactivePane, textvariable=rzz, font=('Comic Sans MS', 11, 'bold italic'), width=5)

        PX_entry = tk.Entry(self.interactivePane, textvariable=px, font=('Comic Sans MS', 11, 'bold italic'), width=5)
        PY_entry = tk.Entry(self.interactivePane, textvariable=py, font=('Comic Sans MS', 11, 'bold italic'), width=5)
        PZ_entry = tk.Entry(self.interactivePane, textvariable=pz, font=('Comic Sans MS', 11, 'bold italic'), width=5)

        col1_rel, col2_rel, col3_rel, col4_rel = .35, .45, .55, .65
        row1_rel, row2_rel, row3_rel = .66, .71, .76
        RXX_entry.place(anchor=tk.S, relx=col1_rel, rely=row1_rel)
        RXY_entry.place(anchor=tk.S, relx=col1_rel, rely=row2_rel)
        RXZ_entry.place(anchor=tk.S, relx=col1_rel, rely=row3_rel)

        RYX_entry.place(anchor=tk.S, relx=col2_rel, rely=row1_rel)
        RYY_entry.place(anchor=tk.S, relx=col2_rel, rely=row2_rel)
        RYZ_entry.place(anchor=tk.S, relx=col2_rel, rely=row3_rel)

        RZX_entry.place(anchor=tk.S, relx=col3_rel, rely=row1_rel)
        RZY_entry.place(anchor=tk.S, relx=col3_rel, rely=row2_rel)
        RZZ_entry.place(anchor=tk.S, relx=col3_rel, rely=row3_rel)

        PX_entry.place(anchor=tk.S, relx=col4_rel, rely=row1_rel)
        PY_entry.place(anchor=tk.S, relx=col4_rel, rely=row2_rel)
        PZ_entry.place(anchor=tk.S, relx=col4_rel, rely=row3_rel)

        rxx.set('RXx')
        rxy.set('RXy')
        rxz.set('RXz')
        ryx.set('RYx')
        ryy.set('RYy')
        ryz.set('RYz')
        rzx.set('RZx')
        rzy.set('RZy')
        rzz.set('RZz')
        px.set('Px')
        py.set('Py')
        pz.set('Pz')

        entries_T = [[RXX_entry, RYX_entry, RZX_entry, PX_entry],
                     [RXY_entry, RYY_entry, RZY_entry, PY_entry],
                     [RXZ_entry, RYZ_entry, RZZ_entry, PZ_entry]]
        rxx.trace('w',
                  lambda a, b, c: self.check_fk_ex2(check_TT, entries_T))
        rxy.trace('w',
                  lambda a, b, c: self.check_fk_ex2(check_TT, entries_T))
        rxz.trace('w',
                  lambda a, b, c: self.check_fk_ex2(check_TT, entries_T))
        ryx.trace('w',
                  lambda a, b, c: self.check_fk_ex2(check_TT, entries_T))
        ryy.trace('w',
                  lambda a, b, c: self.check_fk_ex2(check_TT, entries_T))
        ryz.trace('w',
                  lambda a, b, c: self.check_fk_ex2(check_TT, entries_T))
        rzx.trace('w',
                  lambda a, b, c: self.check_fk_ex2(check_TT, entries_T))
        rzy.trace('w',
                  lambda a, b, c: self.check_fk_ex2(check_TT, entries_T))
        rzz.trace('w',
                  lambda a, b, c: self.check_fk_ex2(check_TT, entries_T))
        px.trace('w',
                 lambda a, b, c: self.check_fk_ex2(check_TT, entries_T))
        py.trace('w',
                 lambda a, b, c: self.check_fk_ex2(check_TT, entries_T))
        pz.trace('w',
                 lambda a, b, c: self.check_fk_ex2(check_TT, entries_T))

    def check_dh_2(self, check_T, entries_T):
        ans_T = [('t1', 'l1', '0', 'pi/2'),
                 ('t2', '0', 'l2', '0'),
                 ('t3', '0', 'l3', '0')]

        for i in range(0, 2):
            for j in range(0, 3):
                if entries_T[i][j].get() == ans_T[i][j]:
                    check_T[i][j] = True
                    entries_T[i][j]['bg'] = 'chartreuse2'
                else:
                    check_T[i][j] = False
                    entries_T[i][j]['bg'] = 'firebrick1'
        if check_T:
            self.nextButton.config(state='normal')

    def check_fk_ex2(self, check_T, entries_T):
        ans_T = [('0', '0', '1', '0'),
                 ('1', '0', '0', '0'),
                 ('0', '1', '0', '5')]

        for i in range(0, 2):
            for j in range(0, 3):
                if entries_T[i][j].get() == ans_T[i][j]:
                    check_T[i][j] = True
                    entries_T[i][j]['bg'] = 'chartreuse2'
                else:
                    check_T[i][j] = False
                    entries_T[i][j]['bg'] = 'firebrick1'
        if check_T:
            self.nextButton.config(state='normal')

    def cos_page(self):
        self.interactivePane.create_text(self.interactive_text_x, self.interactive_text_y - 45,
                                         text="The next two sections will cover techniques necessary to\n"
                                              "correctly and more easily perform geometric inverse kinematics"
                                              "\nfor a robot. This means relying on the known [x,y,z] position\n"
                                              "of the manipulator's end effector and the geometries of the\n"
                                              "robot arm to develop equations to find the joint variables of the"
                                              "\narm. The Law of Cosines defines the relationship of the sides"
                                              "\nand angles of a triangle using the cosine function. In inverse\n"
                                              "kinematics, it is most often used in the form seen below to\n"
                                              "help solve for a theta value of the robot. However, despite\n"
                                              "this equation yielding an angle value to is important to never\n"
                                              "use the inverse cosine or inverse sine to solve for an angle\n"
                                              "as they do not take into account the quadrant of the angle.\n"
                                              "For this we will need to use a handy function available in many\n"
                                              "programming languages: atan2"
                                         ,
                                         font=self.font,
                                         anchor='n')
        self.visualizingPane.update()
        w = self.visualizingPane.winfo_width()
        h = self.visualizingPane.winfo_height()
        self.visualizingPane.create_image(w / 2, h / 2, image=self.cos, anchor=tk.CENTER)

    def atan_page(self):
        self.interactivePane.create_text(self.interactive_text_x, self.interactive_text_y - 45,
                                         text="Atan2(y,x) is a version of the arctangent that uses the quadrant\n"
                                              "of the input to produce the appropriate angle output.\n"
                                              "Traditionally the arctangent, and the arccosine and arcsine\n"
                                              "along with it, do not provide the quadrant information. The\n"
                                              "quadrant is important for inverse kinematics and so atan2 is\n"
                                              "used. Additionally when an angle may be found with the asin\n"
                                              "or acos, it is instead better to obtain both the expression for\n"
                                              "sin and cos (see geometry identity below) and then plug both\n"
                                              "into the atan2 function. Notice how the geometry identity\n"
                                              "produces 2 values because of the +/- square root term. This\n"
                                              "corresponds to the various configurations of the robot to\n"
                                              "reach a given point. Most often, these are referred to as elbow\n"
                                              "up and elbow down configurations as the robot configurations\n"
                                              "are reflections of each other."
                                         ,
                                         font=self.font,
                                         anchor='n')
        self.visualizingPane.update()
        w = self.visualizingPane.winfo_width()
        h = self.visualizingPane.winfo_height()
        self.visualizingPane.create_image(w / 2, 70, image=self.sincos, anchor=tk.CENTER)
        self.visualizingPane.create_image(w / 2,  (h / 3)+10, image=self.atan2_im, anchor=tk.CENTER)
        self.visualizingPane.create_image(w / 2, (3 * h / 4)-15, image=self.D, anchor=tk.CENTER)

    def ik1_page(self):
        self.interactivePane.create_text(self.interactive_text_x, self.interactive_text_y,
                                         text="A basic 2D example for geometric inverse. Find the equations\n"
                                              "for theta 1 and theta 2 and then report the elbow up and\n"
                                              "elbow down solutions for l1=l2=5 and x=(5/2)*2^(1/2),\n"
                                              "y=(5/2)*2^(1/2) + 5. Round decimals to three places.",
                                         font=self.font,
                                         anchor='n')
        self.visualizingPane.update()
        w = self.visualizingPane.winfo_width()
        h = self.visualizingPane.winfo_height()
        self.visualizingPane.create_image(w / 2, h/2, image=self.ikin_ex1, anchor=tk.CENTER)

    def ik2_page(self):
        self.interactivePane.create_text(self.interactive_text_x, self.interactive_text_y,
                                         text="A more complicated 3D example. Find the equations for\n"
                                              "the joint variables. Then find the solution for l1=10,\n"
                                              "l2=l3=5 and [x,y,z] = [0,5,15]. Round decimals to three\n"
                                              "places.",
                                         font=self.font,
                                         anchor='n')
        self.visualizingPane.update()
        w = self.visualizingPane.winfo_width()
        h = self.visualizingPane.winfo_height()
        self.visualizingPane.create_image(w / 2, h/2, image=self.ikin_ex2, anchor=tk.CENTER)

    def velkin_page(self):
        self.interactivePane.create_text(self.interactive_text_x, self.interactive_text_y - 45,
                                         text="Robot kinematics are not limited to just position kinematics.\n"
                                              "Velocity kinematics are another very important part in\n"
                                              "understanding and controlling the movements of a robot.\n"
                                              "Similar to position kinematics, velocity kinematics have both a\n"
                                              "forward and inverse (i.e. the joint velocities are used to find\n"
                                              "the end-effector velocity, or the end-effector velocity is used\n"
                                              "to find the joint velocities). This relationship is described by\n"
                                              "the equation below.\n"
                                         ,
                                         font=self.font,
                                         anchor='n')
        self.visualizingPane.create_text(self.interactive_text_x, 20,
                                         text="Q_dot represents the nx1 vector of joint velocities, J is the\n"
                                              "manipulator Jacobian, and p_dot represents the 6x1 vector of\n"
                                              "linear and angular accelerations of the end-effector. The\n"
                                              "Jacobian is a matrix that represents the derivatives of the\n"
                                              "position of the end-effector with respect to each joint variable\n"
                                              "of the robot. It is constructed using the following equation.\n"
                                         ,
                                         font=self.font,
                                         anchor='n')

    def sing_page(self):
        self.interactivePane.create_text(self.interactive_text_x, self.interactive_text_y-45,
                                         text="Robotic arms have special configurations called singularities.\n"
                                              "A singularity occurs when an arm’s joints are in any position\n"
                                              "such that there is an instantaneous loss of a degree of\n"
                                              "freedom. Examples of this are whenever a joint’s rotation\n"
                                              "coincides with a preceding joint’s rotational axis or when a\n"
                                              "robot is stretched to its maximum length in some direction.\n"
                                              "This is mathematically classified by the determinant of the\n"
                                              "Jacobian being equal to 0."
                                         ,
                                         font=self.font,
                                         anchor='n')

    def congrats_page(self):
        place_rainbow_text("Congratulations", self.visualizingPane, 10, 150, 40)
        place_rainbow_text("NERD", self.visualizingPane, 170, 250, 60)
        self.completed = True

    def place_alt_title(self, text):
        title_font = ('Courier', 30, 'bold italic')
        x = 10
        y = 10

        lines = []
        line = ''
        print_text = text
        if len(text) > 20:
            print_text = ''
            words = text.split(' ')

            for word in words:
                if len(line + ' ' + word) < 20:
                    line = line + word + ' '
                else:
                    lines.append(line)
                    line = word + ' '
            lines.append(line)

            for line in lines:
                print_text = print_text + line + '\n'
        self.interactivePane.create_text(x, y, anchor="nw", font=title_font, text=print_text, fill='black')

    def load_next_page(self):
        self.current_page += 1
        self.generic_page_load()

    def load_last_page(self):
        self.current_page -= 1
        self.generic_page_load()

    def generic_page_load(self):
        self.gui.clearScreen()
        self.makePanes()

        self.interactivePane.create_image(0, 0, image=self.blue_purple_bg, anchor='nw')
        self.visualizingPane.create_image(0, 0, image=self.blue_purple_bg, anchor='nw')
        if 0 < self.current_page < len(self.page_titles) - 1:
            self.place_arrows()
        elif self.current_page == 0:
            self.place_arrows(to_main=True)
        else:
            self.place_arrows(complete=True)
        new_title = self.page_titles[self.current_page]
        self.place_alt_title(new_title)
        self.page_loads[new_title]()

    def place_arrows(self, to_main=False, complete=False):
        xpos_left = .025
        ypos = .75
        xpos_right = .7
        if to_main:
            next = self.current_page + 1

            self.backButton = self.placeBackButton(xpos_left, ypos, self.interactivePane, command=self.gui.HomePage,
                                                   text="Main Menu",
                                                   font=self.button_font)
            self.nextButton = self.placeNextButton(xpos_right, ypos, self.interactivePane, command=self.load_next_page,
                                                   text=self.page_titles[next], font=self.button_font)
        elif complete:
            prev = self.current_page - 1
            self.backButton = self.placeBackButton(xpos_left, ypos, self.interactivePane, command=self.load_last_page,
                                                   text=self.page_titles[prev], font=self.button_font)
            self.nextButton = self.placeNextButton(xpos_right, ypos, self.interactivePane, command=self.gui.HomePage,
                                                   text="Main Menu",
                                                   font=self.button_font)
        else:
            prev = self.current_page - 1
            next = self.current_page + 1
            self.backButton = self.placeBackButton(xpos_left, ypos, self.interactivePane, command=self.load_last_page,
                                                   text=self.page_titles[prev], font=self.button_font)
            self.nextButton = self.placeNextButton(xpos_right, ypos, self.interactivePane, command=self.load_next_page,
                                                   text=self.page_titles[next], font=self.button_font)

    """
    Places the button to go to the next page.
    x: relative location in pane where you want it (from 0 to 1)
    y: relative location in pane where you want it (from 0 to 1)
    text: text you want on the button
    command: callback function for the button
    font: the font you want
    """

    def placeNextButton(self, x, y, pane, text=None, command=None, font=None):
        nextButton = tk.Button(pane, bg=pane["background"], relief=tk.FLAT, command=command)
        self.nextButtonImage = tk.PhotoImage(file="next.png")
        nextButton.config(image=self.nextButtonImage, compound='center', text=text, font=font)
        nextButton.place(relx=x, rely=y)
        return nextButton

    """
    Places the button to go to the previous page.
    x: relative location in pane where you want it (from 0 to 1)
    y: relative location in pane where you want it (from 0 to 1)
    text: text you want on the button
    command: callback function for the button
    font: the font you want
    """

    def placeBackButton(self, x, y, pane, text=None, command=None, font=None):
        backButton = tk.Button(pane, bg=pane["background"], relief=tk.FLAT, command=command)
        self.backButtonImage = tk.PhotoImage(file="back.png")
        backButton.config(image=self.backButtonImage, compound='center', text=text, font=font)
        backButton.place(relx=x, rely=y)
        return backButton
