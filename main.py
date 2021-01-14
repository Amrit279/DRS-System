'''
Author: Amrit279
Started Writing: 13 January, 2021
DRS System (Repository on Git Hub)
Purpose: Making it easier for the umpires to make the correct decision on the feild
'''

import capture # Not an in-built or installed module
import tkinter as tk
from tkinter.filedialog import askopenfilename
from tkinter.messagebox import showerror, showinfo, askokcancel, askyesno
from PIL import Image, ImageTk # pip install pillow
import cv2 as cv # pip install opencv-python
import threading
import imutils # pip install imutils
import time
from functools import partial
import os
class DRS(tk.Tk):
    """
    Helps the umpire in making his decision if he is not sure whether the batsman is out or
    not out. You can move frames back and forward and then make your decision whether a
    batsman is out or not.
    """
    def __init__(self):
        """
        Shows a welcome screen image and buttons
        """
        super().__init__()
        capture.makeVideo()
        self.video = cv.VideoCapture("output.avi")
        self.flag = True
        self.WIDTH = 650
        self.HEIGHT = 368
        self.title("Gully Cricket Decision Review System")
        self.wm_iconbitmap("icon.ico")

        with open("Images.txt", "r") as f:
            self.images = f.read().split("\n")
        try:
            self.cv_img = cv.cvtColor(cv.imread(self.images[0]), cv.COLOR_BGR2RGB)
            # Resizing image
            self.cv_img = imutils.resize(image=self.cv_img, width = self.WIDTH, height = self.HEIGHT)
        # If image for the welcome screen not present then asking user to give a welcome screen image
        except cv.error:
            self.val = askokcancel("File Not Found", "welcome.png could not be found. Do you want to replace it with some of your own file or make a welcome.png of your own")
            if self.val:
                self.file = askopenfilename(defaultextension = ".png", filetypes = [("JPG files", "*.jpg"), ("GIF files", "*.gif"), ("PNG files", "*.png")])
            else:
                exit()
            
            # If some file is selected then only do changes
            if self.file != "":
                self.cv_img = cv.cvtColor(cv.imread(self.file), cv.COLOR_BGR2RGB)
                self.cv_img = imutils.resize(image=self.cv_img, width = self.WIDTH, height = self.HEIGHT)
                self.default = askyesno("Make Default", "Do you want to make this as your default welcome screen image")
                if self.default:
                    self.images[0] = self.file
                    with open("Images.txt", "w") as f:
                        f.write("\n".join(self.images) + "\n")
            else:
                exit()   
        self.canvas = tk.Canvas(self, width = self.WIDTH, height = self.HEIGHT)
        self.photo = ImageTk.PhotoImage(image = Image.fromarray(self.cv_img))
        self.canvas.create_image(0, 0, image = self.photo, anchor = tk.NW)
        self.canvas.pack()

        # DRS buttons
        self.but = tk.Button(self, text = "<< Previous (Fast)", padx = 50, command = partial(self.play, -15))
        self.but.pack()
        self.but = tk.Button(self, text = "<< Previous (Slow)", padx = 48.4, command = partial(self.play, -2))
        self.but.pack()
        self.but = tk.Button(self, text = "Next (Fast) >>", padx =60.4, command = partial(self.play, 10))
        self.but.pack()
        self.but = tk.Button(self, text = "Next (Slow) >>", padx = 58, command = partial(self.play, 2))
        self.but.pack()
        self.but = tk.Button(self, text = "Give Out", padx = 75, command = self.out)
        self.but.pack()
        self.but = tk.Button(self, text = "Give Not Out", padx = 63.4, command = self.not_out)
        self.but.pack()
    
    def play(self, speed):
        """
        Plays video frames forward and backward according to the buttons pressed
        """
        self.speed = speed
        self.cframe = self.video.get(cv.CAP_PROP_POS_FRAMES)
        self.video.set(cv.CAP_PROP_BUFFERSIZE, 2)
        self.video.set(cv.CAP_PROP_POS_FRAMES, self.cframe + self.speed)

        self.ret, self.frame = self.video.read()
        if not self.ret:
            showinfo("Video Ended", "The video clip has ended")
            exit()
    
        self.frame = imutils.resize(image=self.frame, width = self.WIDTH, height = self.HEIGHT)
        self.frame = ImageTk.PhotoImage(image= Image.fromarray(self.frame))
        self.canvas.create_image(0, 0, image= self.frame, anchor = tk.NW)

        # Blinking Text
        if self.flag:
            self.canvas.create_text(130, 24, text= "Decision Pending", fill = "black", font = "consolas 21")
        self.flag = not self.flag

    def out(self):
        """
        Starts a thread which runs the pending fuction with 'Out' as argument
        """
        thread = threading.Thread(target= self.pending, args = ("Out",))
        thread.daemon = 1
        thread.start()
        print("Out")

    def not_out(self):
        """
        Starts a thread which runs the pending fuction with 'Not Out'
        """
        thread = threading.Thread(target= self.pending, args = ("Not Out",))
        thread.daemon = 1
        thread.start()
        print("Not Out")

    def pending(self, decision):
        """
        Displays the decision pending image, sponsor image and the out/not out image
        """
        self.decision = None
        try:
            self.frame = cv.cvtColor(cv.imread(self.images[1]), cv.COLOR_BGR2RGB)
            self.frame = imutils.resize(image = self.frame, width = self.WIDTH, height= self.HEIGHT)
        except cv.error:
            self.val = askokcancel("File Not Found", "pending.png could not be found. Do you want to replace it with some of your own file or make a pending.png of your own")
            if self.val:
                self.file = askopenfilename(defaultextension = ".png", filetypes = [("JPG files", "*.jpg"), ("GIF files", "*.gif"), ("PNG files", "*.png")])
            else:
                exit()
            
            # If some file is selected then only do changes
            if self.file != "":
                self.cv_img = cv.cvtColor(cv.imread(self.file), cv.COLOR_BGR2RGB)
                self.cv_img = imutils.resize(self.cv_img, width = self.WIDTH, height = self.HEIGHT)
                self.default = askyesno("Make Default", "Do you want to make this as your default pending screen image")
                if self.default:
                    self.images[1] = self.file
                    with open("Images.txt", "w") as f:
                        f.write("\n".join(self.images) + "\n")
            else:
                exit() 
        self.frame = imutils.resize(image = self.frame, width = self.WIDTH, height = self.HEIGHT)
        self.frame = ImageTk.PhotoImage(image = Image.fromarray(self.frame))
        self.canvas.create_image(0, 0, image = self.frame, anchor = tk.NW)
        time.sleep(1)
        try:
            self.frame = cv.cvtColor(cv.imread(self.images[2]), cv.COLOR_BGR2RGB)
            self.frame = imutils.resize(image=self.frame, width = self.WIDTH, height = self.HEIGHT)
        except cv.error:
            self.val = askokcancel("File Not Found", "sponsor.png could not be found. Do you want to replace it with some of your own file or make a sponsor.png of your own")
            if self.val:
                self.file = askopenfilename(defaultextension = ".png", filetypes = [("JPG files", "*.jpg"), ("GIF files", "*.gif"), ("PNG files", "*.png")])
            else:
                exit()
            
            # If some file is selected then only do changes
            if self.file != "":
                self.cv_img = cv.cvtColor(cv.imread(self.file), cv.COLOR_BGR2RGB)
                self.cv_img = imutils.resize(self.cv_img, width = self.WIDTH, height = self.HEIGHT)
                self.default = askyesno("Make Default", "Do you want to make this as your default sponsor screen image")
                if self.default:
                    self.images[2] = self.file
                    with open("Images.txt", "w") as f:
                        f.write("\n".join(self.images) + "\n")
            else:
                exit() 

        self.frame = imutils.resize(image = self.frame, width = self.WIDTH, height = self.HEIGHT)
        self.frame = ImageTk.PhotoImage(image = Image.fromarray(self.frame))
        self.canvas.create_image(0, 0, image = self.frame, anchor = tk.NW)
        time.sleep(1.5)

        if decision == "Out":
            self.decision = self.images[3]
        else:
            self.decision = self.images[4]
        try:
            self.frame = cv.cvtColor(cv.imread(self.decision), cv.COLOR_BGR2RGB)
            self.frame = imutils.resize(image = self.frame, width = self.WIDTH, height = self.HEIGHT)
        except cv.error:
            if decision == "Out":
                self.val = askokcancel("File Not Found", "out.png could not be found. Do you want to replace it with some of your own file or make a out.png of your own")
            else:
                self.val = askokcancel("File Not Found", "not_out.png could not be found. Do you want to replace it with some of your own file or make a not_out.png of your own")
            if self.val:
                self.file = askopenfilename(defaultextension = ".png", filetypes = [("JPG files", "*.jpg"), ("GIF files", "*.gif"), ("PNG files", "*.png")])
            else:
                exit()
            
            # If some file is selected then only do changes
            if self.file != "":
                self.cv_img = cv.cvtColor(cv.imread(self.file), cv.COLOR_BGR2RGB)
                self.cv_img = imutils.resize(image = self.cv_img, width = self.WIDTH, height = self.HEIGHT)
                if self.decision == "Out":
                    self.default = askyesno("Make Default", "Do you want to make this as your default out screen image")
                else:
                    self.default = askyesno("Make Default", "Do you want to make this as your default not_out screen image")
                if self.default:
                    if decision == "Out":
                        self.images[3] = self.file
                        with open("Images.txt", "w") as f:
                            f.write("\n".join(self.images) + "\n")
                        self.frame = ImageTk.PhotoImage(image = Image.fromarray(self.cv_img))
                        self.canvas.create_image(0, 0, image = self.frame, anchor = tk.NW)
                    else:
                        self.images[4] = self.file
                        with open("Images.txt", "w") as f:
                            f.write("\n".join(self.images) + "\n")
                        self.frame = ImageTk.PhotoImage(image = Image.fromarray(self.cv_img))
                        self.canvas.create_image(0, 0, image = self.frame, anchor = tk.NW)
            else:
                exit() 
        else:
            self.frame = ImageTk.PhotoImage(image = Image.fromarray(self.frame))
            self.canvas.create_image(0, 0, image = self.frame, anchor = tk.NW)

if __name__ == "__main__":
    drs = DRS()
    # Making window non-resizable
    drs.minsize(650, 530)
    drs.maxsize(650, 530)
    drs.mainloop()