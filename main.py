import capture # Not an in-built or installed module
import tkinter as tk
from tkinter.filedialog import askopenfilename
from tkinter.messagebox import showerror
from PIL import Image, ImageTk # pip install pillow
import cv2 as cv # pip install opencv-python
import threading
import imutils # pip install imutils
import time
from functools import partial
class DRS(tk.Tk):
    """
    Helps the umpire in making his decision if he is not sure whether the batsman is out or
    not out. You can move frames back and forward and then make your decision whether a
    batsman is out or not.
    """
    def __init__(self):
        super().__init__()
        capture.makeVideo()
        self.WIDTH = 650
        self.HEIGHT = 368
        self.title("Decision Review System")
        try:
            self.cv_img = cv.cvtColor(cv.imread("welcome.png"), cv.COLOR_BGR2RGB)
        except cv.error:
            self.file = askopenfilename(defaultextension = ".png", filetypes = [("JPG files", "*.jpg"), ("GIF files", "*.gif"), ("PNG files", "*.png")])
            self.cv_img = cv.cvtColor(cv.imread(self.file), cv.COLOR_BGR2RGB)
            
        self.canvas = tk.Canvas(self, width = self.WIDTH, height = self.HEIGHT)
        self.photo = ImageTk.PhotoImage(image = Image.fromarray(self.cv_img))
        self.canvas.create_image(0, 0, image = self.photo, anchor = tk.NW)
        self.canvas.pack()

        self.but = tk.Button(self, text = "<< Previous (Fast)", padx = 2.6)
        self.but.pack()
        self.but = tk.Button(self, text = "<< Previous (Slow)")
        self.but.pack()
        self.but = tk.Button(self, text = "Next (Fast) >>", padx = 13.4)
        self.but.pack()
        self.but = tk.Button(self, text = "Next (Slow) >>", padx = 11)
        self.but.pack()
        self.but = tk.Button(self, text = "Give Out", padx = 27.5, command = self.out)
        self.but.pack()
        self.but = tk.Button(self, text = "Give Not Out", padx = 16.4, command = self.not_out)
        self.but.pack()

    def out(self):
        thread = threading.Thread(target= self.pending, args = ("Out",))
        thread.daemon = 1
        thread.start()
        print("Out")

    def not_out(self):
        thread = threading.Thread(target= self.pending, args = ("Not Out",))
        thread.daemon = 1
        thread.start()
        print("Not Out")

    def pending(self, decision):
        self.decision = None
        try:
            self.frame = cv.cvtColor(cv.imread("pending.png"), cv.COLOR_BGR2RGB)
        except cv.error:
            showerror("File Not Found", "pending.png cannot be found")
            exit()
        self.frame = imutils.resize(self.frame, width = self.WIDTH, height = self.HEIGHT)
        self.frame = ImageTk.PhotoImage(image = Image.fromarray(self.frame))
        self.canvas.create_image(0, 0, image = self.frame, anchor = tk.NW)
        time.sleep(1)
        try:
            self.frame = cv.cvtColor(cv.imread("sponsor1.png"), cv.COLOR_BGR2RGB)
        except cv.error:
            showerror("File Not Found", "sponsor.png cannot be found")
            exit()

        self.frame = imutils.resize(self.frame, width = self.WIDTH, height = self.HEIGHT)
        self.frame = ImageTk.PhotoImage(image = Image.fromarray(self.frame))
        self.canvas.create_image(0, 0, image = self.frame, anchor = tk.NW)
        time.sleep(1.5)

        if decision == "Out":
            self.decision = "out.png"
        else:
            self.decision = "not_out.png"
        try:
            self.frame = cv.cvtColor(cv.imread(self.decision), cv.COLOR_BGR2RGB)
        except cv.error:
            showerror("File Not Found", "out/not_out.png cannot be found")
            exit()
        self.frame = imutils.resize(self.frame, width = self.WIDTH, height = self.HEIGHT)
        self.frame = ImageTk.PhotoImage(image = Image.fromarray(self.frame))
        self.canvas.create_image(0, 0, image = self.frame, anchor = tk.NW)

if __name__ == "__main__":
    drs = DRS()
    drs.mainloop()