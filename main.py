import capture # Not an in-built or installed module
import tkinter as tk
from PIL import Image, ImageTk # pip install pillow
import cv2 as cv # pip install opencv-python
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
        self.cv_img = cv.cvtColor(cv.imread("welcome.png"), cv.COLOR_BGR2RGB)
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
        self.but = tk.Button(self, text = "Give Out", padx = 27.5)
        self.but.pack()
        self.but = tk.Button(self, text = "Give Not Out", padx = 16.4)
        self.but.pack()

if __name__ == "__main__":
    drs = DRS()
    drs.mainloop()