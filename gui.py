from Tkinter import *
import tkFileDialog

import picamera
from picamera.array import PiRGBArray
from picamera import PiCamera
from PIL import Image, ImageTk

import pandas as pd
import cv2

from utils import find_qr, find_name, show_warning, show_message


class Gui:
    def __init__(self, msg_if_found):
        self.root = Tk()
        self.found_msg = msg_if_found
        
        # initialize VideoStream
        self.vs = vs
        self.frame = None
        self.thread = None  # to control the video polling loop
        self.stopEvent = None
        self.last_message = None
        
        # initialize other widgets
        self.l = None  # Text instructions for the entry box to select file.
        self.e = None  # Where the path of the selected file will be shown
        self.browse_button = None  # button to browse for the file where H&PS folks
                                   # have expressed interest in attending the event
        self.start_button = None  # button to start the scanning process
        self.exit = None  # The button to exit the programme.

        self.rsvp_df = None  # The dataframe containing information of the H&PS folks
                              # who have expressed interest in attending the event.
                              
        # Initialize other variables
        self.filename = None
        
    def __openfile__(self):
        self.filename = tkFileDialog.askopenfilename()
        self.e.delete(0, END)
        self.e.insert(0, self.filename)
        
        if self.filename.endswith('csv'):
            self.rsvp_df = pd.read_csv(self.filename)
        elif self.filename.endswith('xlsx') or self.filename.endswith('xls'):
            self.rsvp_df = pd.read_excel(self.filename)

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
                        house, self.rsvp_df = find_name(self.rsvp_df, data, filename=self.filename, columname="EID")
                        show_message(data, self.found_msg % (data, house))
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
        except RuntimeError, e:
            print("[INFO] caught a RuntimeError")
            
            image = ImageTk.PhotoImage(image)  # ...and then to ImageTk format
            # Show image in root.
            image_l = Label(self.root, image=image, height=height, width=screen_width)
            # Label grid.
            image_l.grid(row=0, column=0, sticky='EW')
            
            
            
            # Create a reader
            scan_image = zbar.Image(width, height, 'Y800', raw)
            scanner.scan(scan_image)
            # Extract result
            for symbol in scan_image:
                # returns a beep sound.
                playBeep()
                last_message = symbol.data    
                # Match data with DB and mark attendance, log timestamp
                # Fetch data from DB and returns a pop-up message
                print "The QR code says: %s" %symbol.data  # for the moment the encoded symbol is printed on the console
                # Save the file after scanning.
                self.__savefile__()   


    def __exit__(self):
        # remember to save first before exiting.
        self.__savefile__()
        
        # Exit.
        self.root.destroy()
    
    def widgets(self):
        self.l = Label(self.root, text="Select Attendance File")
        self.e = Entry(self.root)
        self.browse_button = Button(self.root, text="Browse", command=self.__openfile__)
        self.start_button = Button(self.root, text="Start Scanning", command=self.__scan__)
        self.exit = Button(self.root, text="Save & Exit", command=self.__exit__)
        
    def grid_layout(self):
        datum = 0
        datum += 1
        self.l.grid(row=datum, column=0, sticky="E")
        self.e.grid(row=datum, column=1, columnspan=2, sticky="EW")
        self.browse_button.grid(row=datum, column=3, sticky="W")
        # To get the height of row 1
        self.root.update()
        widget_heights = max(self.l.winfo_height(), self.e.winfo_height(), self.browse_button.winfo_height())
        datum += 1
        self.start_button.grid(row=datum, column=1)
        self.exit.grid(row=datum, column=2)
        # To get the height of row 2
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
        
    def main_loop(self):
        self.root.mainloop()
