import tkinter
import tkMessageBox
from time import sleep

def message(name, msg):
    """ Shows a message box with the message and an "OK" button. """
    response = None
    response = tkMessageBox.showinfo(name, msg)

    if response:
        return
    else:
        sleep(10)
        return

