from gui import Gui

# from Tkinter import *
# import tkFileDialog

# from PIL import ImageTk, Image


scanner = Gui()
scanner.widgets()
scanner.grid_layout()
scanner.main_loop()




def label_w_h(proportion, max_height, max_width):
    # width based on max_height
    w = int(proportion * max_height)

    if w <= max_width:
        return w, max_height
    else:
        return max_width, int(max_width / proportion)


"""
# test with a sample picture.
# for picamera, do camera.resolution = (1024, 768)
path = "img/falcon.jpg"
# convert picture to PIL format
image = Image.open(path)
# resize the PIL image
image_width, image_height = image.size
image_proportion = image_width*1.0/image_height
resize = label_w_h(image_proportion, screen_height, screen_width)
image = image.resize(resize, Image.ANTIALIAS)
# convert PIL image tto Tk image
img = ImageTk.PhotoImage(image)
# draw image in Label
image_l = Label(root, image=img, height=label_height, width=screen_width)
# Label grid.
image_l.grid(row=0, column=0, columnspan=3, sticky='EW')

root.mainloop()
"""
