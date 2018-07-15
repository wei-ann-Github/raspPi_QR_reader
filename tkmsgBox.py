import Tkinter as tk
import tkMessageBox

root = tk.Tk()
root.withdraw()

def message(window_name, msg):
	tkMessageBox.showinfo(window_name, msg)
	root.update()
