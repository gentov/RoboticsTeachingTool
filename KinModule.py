# Owen Smith
# 6/16/2020

from Module import Module as Mod
from PIL import ImageTk, Image
import tkinter as tk


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
        self.green_pattern_bg = ImageTk.PhotoImage(fit_canvas_im)

        self.interactive_text_x = 255
        self.interactive_text_y = 90

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
                                              "\n\nTest your understanding of position displacement below!\n",
                                         font=self.font,
                                         anchor='n')

    def rot_page(self):
        self.interactivePane.create_text(self.interactive_text_x, self.interactive_text_y,
                                         text="A point vector [x, y, z] represented in\n"
                                              "a rotated frame is defined by p1 = R*p0, where p0 is the initial"
                                              "\npoint, p1 is the new point, and R is a rotation matrix. We’ll"
                                              "\ngo into more detail on the rotation matrix in the next section,"
                                              "\nbut it is a representation of the angle of the new frame’s axes"
                                              "\nwith respect to the previous frame’s axes (Figure 2).",
                                         font=self.font,
                                         anchor='n')

    def trans_mat_page(self):
        self.interactivePane.create_text(self.interactive_text_x, self.interactive_text_y,
                                         text="Transformation matrices",
                                         font=self.font,
                                         anchor='n')

    def dh_page(self):
        self.interactivePane.create_text(self.interactive_text_x, self.interactive_text_y,
                                         text="Denavit-Hartenberg parameters",
                                         font=self.font,
                                         anchor='n')

    def fk1_page(self):
        self.interactivePane.create_text(self.interactive_text_x, self.interactive_text_y,
                                         text="This 2D example is a simple introduction",
                                         font=self.font,
                                         anchor='n')

    def fk2_page(self):
        self.interactivePane.create_text(self.interactive_text_x, self.interactive_text_y,
                                         text="A more complicated 3D example",
                                         font=self.font,
                                         anchor='n')

    def cos_page(self):
        self.interactivePane.create_text(self.interactive_text_x, self.interactive_text_y,
                                         text="The law of cosines is cool",
                                         font=self.font,
                                         anchor='n')

    def atan_page(self):
        self.interactivePane.create_text(self.interactive_text_x, self.interactive_text_y,
                                         text="Using atan2 is important",
                                         font=self.font,
                                         anchor='n')

    def ik1_page(self):
        self.interactivePane.create_text(self.interactive_text_x, self.interactive_text_y,
                                         text="A basic 2D example for geometric inverse",
                                         font=self.font,
                                         anchor='n')

    def ik2_page(self):
        self.interactivePane.create_text(self.interactive_text_x, self.interactive_text_y,
                                         text="A more complicated 3D example",
                                         font=self.font,
                                         anchor='n')

    def velkin_page(self):
        self.interactivePane.create_text(self.interactive_text_x, self.interactive_text_y,
                                         text="Velocity Kinematics use the Manipulator Jacobian",
                                         font=self.font,
                                         anchor='n')

    def sing_page(self):
        self.interactivePane.create_text(self.interactive_text_x, self.interactive_text_y,
                                         text="Singularities exist when determinant of Jacobian",
                                         font=self.font,
                                         anchor='n')

    def congrats_page(self):
        self.interactivePane.create_text(self.interactive_text_x, self.interactive_text_y,
                                         text="Congratulations nerd!", font=self.font,
                                         anchor='n')
        self.completed = True

    def place_rainbow_title(self, text):
        title_font = ('Courier', 30, 'bold italic')
        rainbow_fill = ['red', 'dark orange', 'gold', 'green3', 'blue', 'dark violet']
        y = 20
        char_count = 0
        space_count = 0
        for i in range(0, len(text)):

            char = text[i]
            if char == ' ':
                space_count += 1
            color_idx = (i - space_count) % len(rainbow_fill)
            color = rainbow_fill[color_idx]
            if char_count > 13 and char == ' ':
                y += 35
                char_count = 0
            x = 20 + (24 * char_count)
            self.interactivePane.create_text(x, y, anchor="nw", font=title_font, text=char, fill=color)
            char_count += 1

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
        self.visualizingPane.create_image(0, 0, image=self.green_pattern_bg, anchor='nw')
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

            self.placeBackButton(xpos_left, ypos, self.interactivePane, command=self.gui.HomePage, text="Main Menu",
                                 font=self.button_font)
            self.placeNextButton(xpos_right, ypos, self.interactivePane, command=self.load_next_page,
                                 text=self.page_titles[next], font=self.button_font)
        elif complete:
            prev = self.current_page - 1
            self.placeBackButton(xpos_left, ypos, self.interactivePane, command=self.load_last_page,
                                 text=self.page_titles[prev], font=self.button_font)
            self.placeNextButton(xpos_right, ypos, self.interactivePane, command=self.gui.HomePage, text="Main Menu",
                                 font=self.button_font)
        else:
            prev = self.current_page - 1
            next = self.current_page + 1
            self.placeBackButton(xpos_left, ypos, self.interactivePane, command=self.load_last_page,
                                 text=self.page_titles[prev], font=self.button_font)
            self.placeNextButton(xpos_right, ypos, self.interactivePane, command=self.load_next_page,
                                 text=self.page_titles[next], font=self.button_font)
