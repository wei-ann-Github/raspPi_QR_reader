""" Source: https://www.pyimagesearch.com/2016/05/30/displaying-a-video-feed-with-opencv-and-tkinter/ """
import time
import threading  # For handling polling of new frames from our video stream separately from root.mainloop()
from Tkinter import *
import tkFileDialog

import picamera
from picamera.array import PiRGBArray
from picamera import PiCamera
from PIL import Image, ImageTk

import imutils
import pandas as pd
import cv2

from utils import find_qr, find_name, show_warning, show_message


class Gui:
    def __init__(self, vs, found_msg="", return_msg=""):
        self.root = Tk()
        # self.root.bind('<Return>', self.walkin)
        self.root.wm_title("QR Code Scanner")
        self.root.attributes('-fullscreen', True)
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(3, weight=1)
        
        self.found_msg = found_msg
        self.return_msg = return_msg
        self.event_name = "the event"
        
        # initialize VideoStream
        self.vs = vs
        self.frame = None
        self.thread = None  # to control the video polling loop
        self.stopEvent = None

        # initialize the QR code scanner.
        self.last_message = None
        
        # initialize other widgets
        self.panel = None  # Label widget for displaying the image.
        self.l = None  # Text instructions for the entry box to select file.
        self.e = None  # Where the path of the selected file will be shown
        # self.name_entry self.name_entry= None  # Users can enter their name here.
        self.browse_button = None  # button to browse for the file where H&PS folks
        # have expressed interest in attending the event
        self.start_button = None  # button to start the scanning process
        self.start_btn_text = StringVar()
        self.exit = None  # The button to exit the programme.
        self.rsvp_df = None  # The dataframe containing information of the H&PS folks
        # who have expressed interest in attending the event.
        self.houselist_df = None  # The dataframe containing the house list of H&PS folks
        self.event_l = None  # Text instructions to enter the event name
        self.event_e = None  # Entry box to enter the event name

        # Initialize dimensions
        self.button_width = 15
        self.image_panel_height = 200
        self.num_columns = 4  # number of columns of widget
        
        # Initialize other variables
        self.filename = None
        
    def __openFile__(self):
        self.filename = tkFileDialog.askopenfilename()
        self.e.delete(0, END)
        self.e.insert(0, self.filename)
        
        if self.filename.endswith('csv'):
            self.rsvp_df = pd.read_csv(self.filename)
        elif self.filename.endswith('xlsx') or self.filename.endswith('xls'):
            self.rsvp_df = pd.read_excel(self.filename)

        if 'attendance' not in self.rsvp_df.columns:
            self.rsvp_df['attendance'] = None
        
        try:
            colname = self.rsvp_df.columns
        except:
            print self.rsvp_df
            
    def __stop_scan__(self):
        if self.start_button.cget('text') == "Stop Scanning":
            self.start_button.configure(text = "Start Scanning", command=self.__scan__)
            
        # Stop the camera.
        self.vs.stop()  # maybe this is correct.
        self.stopEvent = None
        
        # reshow the grids hidden.
        # self.name_entry.grid_remove()
        self.e.unbind('<Return>')
        self.l.config(text="Select Attendance File")
        self.browse_button.grid()
        # self.e.grid()
            
    def videoLoop(self):  # width is redundant
        try:
            # keep looping over frames until we are instructed to stop
            while not self.stopEvent.is_set():
                # grab the frame from the video stream and resize it to
                # have a maximum width of 300 pixels
                self.frame = self.vs.read()
                # self.frame = imutils.resize(self.frame, width=width)
                # self.frame = imutils.resize(self.frame, width=self.root.winfo_screenwidth())
                self.frame = imutils.resize(self.frame, height=self.image_panel_height)
                # OpenCV represents images in BGR order; however PIL
                # represents images in RGB order, so we need to swap
                # the channels, then convert to PIL and ImageTk format
                image = cv2.cvtColor(self.frame, cv2.COLOR_BGR2RGB)  # Perform the swap
                image = Image.fromarray(image)  # W X H
                image = ImageTk.PhotoImage(image)
                
                data = find_qr(self.frame, self.last_message)
                # data = None
                if data is not None:
                    self.last_message = data
                    if self.rsvp_df is not None:
                        house, self.rsvp_df, flag = find_name(self.rsvp_df, data, filename=self.filename, columname="EID")
                        if flag:
                            show_message("Hi %s, welcome back!" % (data, house)[:1])
                        else:
                            show_message(self.found_msg % (data, house)[:1])
                    else:
                        show_warning()

                # if the panel is not None, we need to initialize it
                if self.panel is None:
                    self.panel = Label(image=image)
                    # self.panel.image = image
                    self.panel.grid(row=0, column=0, columnspan=self.num_columns, sticky="EW")
                # otherwise, simply update the panel
                else:
                    self.panel.configure(image=image)
                    self.panel.image = image

                name = find_qr(self.frame, self.last_message)

                if name is not None:
                    self.last_message = name
                    if self.rsvp_df is not None:
                        house, self.rsvp_df, seen = find_name(self.rsvp_df, name, filename=self.filename,
                                                              columname="name")
                        name = ' '.join([item.upper() for item in name.split('.')[:-1]])
                        if not seen:
                            show_message(self.found_msg % (name, house)[:1])
                        elif seen:
                            show_message(self.return_msg % (name, house)[:1])
                    else:
                        show_warning()

        except RuntimeError, e:
            print("[INFO] caught a RuntimeError")
            
    def __scan__(self):
        if self.rsvp_df is None:
            show_warning()
            return
        self.e.delete(0, 'end')
        # Change the text in self.start_button to stop.
        if self.start_button.cget('text') == "Start Scanning":
            self.start_button.configure(text="Stop Scanning", command=self.__stop_scan__)
            self.start_btn_text.set("Stop Scanning")

#        # Get the name of the event.
#        if len(self.event_e.get("1.0", 'end-1c')) > 0:
#            self.event_name = self.event_e.get("1.0", 'end-1c')
            
        self.stopEvent = threading.Event()
        print("self.stopEvent set")
        width = self.root.winfo_screenwidth()
        height = self.root.winfo_screenheight()
        self.thread = threading.Thread(target=self.videoLoop, args=())
        self.thread.start()
        self.root.wm_protocol("WM_DELETE_WINDOW", self.onClose)
        
        # Hide the interfaces not meant for the video stream window
        # self.e.grid_remove()
        self.start_button.grid_remove()
        self.browse_button.grid_remove()
        self.event_l.grid_remove()
        self.event_e.grid_remove()
        self.l.config(text="Enter you name")
        # self.name_entry.grid()
        # self.name_entry.bind('<Return>', self.walkin)
        self.e.bind('<Return>', self.walkin)
            
    def widgets(self):
        self.panel = Label(image=None)
        self.l = Label(self.root, text="Select Attendance File")
        self.e = Entry(self.root)
        # self.name_entry = Entry(self.root)
        self.browse_button = Button(self.root, text="Browse", command=self.__openFile__, width=self.button_width)
        self.start_button = Button(self.root, text="Start Scanning", command=self.__scan__, width=self.button_width)
        # self.start_button = Button(self.root, textvariable=self.start_btn_text, command=self.__scan__,
        # width=self.button_width)
        self.start_btn_text.set("Start Scanning")
        self.exit = Button(self.root, text="Save & Exit", command=self.onClose, width=self.button_width)
        self.event_l = Label(self.root, text="Enter the name of the event")
        self.event_e = Entry(self.root)
        
    def grid_layout(self):
        widget_heights = 0
        
        datum = 0  # Datum zero is for the camera feed.
        self.panel.grid(row=datum, column=0, columnspan=self.num_columns + 1, sticky="EW")
        
        datum += 1
        self.l.grid(row=datum, column=0, sticky="E")
        self.e.grid(row=datum, column=1, columnspan=2, sticky="EW")
        # self.name_entry.grid(row=datum, column=1, columnspan=2, sticky="EW")
        # self.name_entry.grid_remove()
        self.browse_button.grid(row=datum, column=3, sticky="W")
        self.root.update()
        widget_heights += max(self.l.winfo_height(), self.e.winfo_height(), self.browse_button.winfo_height())

        datum += 1
        self.event_l.grid(row=datum, column=0, sticky="E")
        self.event_e.grid(row=datum, column=1, columnspan=2, sticky="EW")

        datum += 1
        self.start_button.grid(row=datum, column=1)
        self.exit.grid(row=datum, column=2)
        self.root.update()
        widget_heights += max(self.start_button.winfo_height(), self.exit.winfo_height())
        
        self.image_panel_height = self.root.winfo_screenheight() - widget_heights
        
    def onClose(self):
        # Write the data to frame
        if self.filename is not None:
            self.rsvp_df.to_csv(self.filename, index=False)
        # set the stop event, cleanup the camera, and allow the rest of
        # the quit process to continue
        if self.stopEvent is not None:
            print("[INFO] closing...")
            self.stopEvent.set()
            self.vs.stop()    
        self.root.quit()
        
    def walkin(self, *args):
        if self.e.get().strip() != '':
            name = self.e.get().split("@")[0].strip().lower()
            _, self.rsvp_df, seen = find_name(self.rsvp_df, name, filename=self.filename, columname="name")
            name = ' '.join([item.upper() for item in name.split('.')[:-1]])
            if not seen:
                show_message(self.found_msg % name)
            elif seen:
                show_message(self.return_msg % name)
        self.e.delete(0, 'end')
        
    def main_loop(self):
        self.root.mainloop()
