from Tkinter import *
import tkFileDialog

import picamera
from picamera.array import PiRGBArray
from picamera import PiCamera
from PIL import Image, ImageTk

import pandas as pd
import cv2
import zbar

class Gui:
    def __init__(self):
        self.root = Tk()
        
        # initialize camera
        self.camera = PiCamera()
        self.camera_height = 1040
        self.camera_width = 1280
        self.camera.resolution = (self.camera_width, self.camera_height)
        self.camera.framerate = 32

        # initialize the QR code scanner.
        self.scanner = zbar.ImageScanner()
        self.last_message = None
        
        # initialize other widgets
        self.l = None  # Text instructions for the entry box to select file.
        self.e = None  # Where the path of the selected file will be shown
        self.browse_button = None  # button to browse for the file where H&PS folks
                                   # have expressed interest in attending the event
        self.start_button = None  # button to start the scanning process
        self.exit = None  # The button to exit the programme.
        self.register = None  # The dataframe containing information of the H&PS folks
                              # who have expressed interest in attending the event.
                              
        # Initialize other variables
        self.filename = None
        
    def __openfile__(self):
        self.filename = tkFileDialog.askopenfilename()
        self.e.delete(0, END)
        self.e.insert(0, self.filename)
        
        if self.filename.endswith('csv'):
            self.register = pd.read_csv(self.filename)
        elif self.filename.endswith('xlsx') or self.filename.endswith('xls'):
            self.register = pd.read_excel(self.filename)

        try:
            colname = self.register.columns
        except:
            print self.register
            
    def __savefile__(self):
        if self.filename is not None and self.filename.endswith('csv'):
            self.register.to_csv(self.filename, index=False, encoding='utf8')
        elif self.filename is not None and (self.filename.endswith('xlsx') or self.filename.endswith('xls')):
            self.register = pd.read_excel(self.filename, index=False)
        else:
            return
        
    def __exit__(self):
        # go back to the initial screen
        self.widgets()
        self.grid_layout()
        pass
        
    def __scan__(self):
        # Screen size
        self.root.attributes('-fullscreen', True)
        self.screen_width = int(self.root.winfo_screenwidth())
        self.screen_height = int(self.root.winfo_screenheight())
        # create a stop button
        stop_button = Button(self.root, text="Stop Scanning", command=self.__exit__))
        stop_button.grid(row=1, column=0)
        
        cap = PiRGBArray(self.camera, size=(self.camera_width, self.camera_height))

        for i in self.camera.capture_continuous(cap, format='bgr', use_video_port=True):
            image = i.array

            # Reading the image for QR code
            image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            # convert the images to PIL format...
            pil = Image.fromarray(image)
            # convert from PIL format to raw for zbar scanning.
            width, height = pil.size
            raw = pil.tobytes()
            
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
                    
            # cap.truncate(0)
            # key = cv2.waitKey(1) & 0xFF
            # if key  == ord("q"):
                    # break
    
    


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
        datum += 1
        self.start_button.grid(row=datum, column=1)
        self.exit.grid(row=datum, column=2)

        # adjust the image panel size last
        # self.root.update()
        # label_height = self.screen_height - 2 * self.start_button.winfo_height()
        
    def main_loop(self):
        self.root.mainloop()