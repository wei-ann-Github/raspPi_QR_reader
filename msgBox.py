from Tkinter import *
import tkMessageBox
from time import sleep


def show_message(name, msg):
    """ Shows a message box with the message and an "OK" button. """
    tkMessageBox.showinfo(name, msg)


root = Tk()
message = "hello world"
name = "no name"
b = Button(root, text="click me", command=lambda: show_message(name, message))
b.pack()

root.mainloop()
