from __future__ import print_function

from gui import *

from Tkinter import *
import tkFileDialog

from PIL import ImageTk, Image
import picamera
from picamera import PiCamera
from picamera.array import PiRGBArray


def gui():
    root = Tk()
    root.attributes('-fullscreen', True)
    screen_width = int(root.winfo_screenwidth())
    screen_height = int(root.winfo_screenheight())

    # Widgets
    l = Label(root, text="Select Attendance File")
    e = Entry(root)
    browse_button = Button(root, text="Browse", command=openfile)
    start_button = Button(root, text="Start Scanning", command=scan)

    # Grid
    ## Row 0
    datum = 0  # 0 is for display the image from the picamera
    ## Row 1
    datum += 1
    l.grid(row=datum, column=0, sticky="E")
    e.grid(row=datum, column=1, sticky="EW")
    browse_button.grid(row=datum, column=2, sticky="W")
    ## Row 2
    datum += 1
    start_button.grid(row=datum, column=1)

    # adjust the image panel size last
    root.update()
    label_height = screen_height - 2 * start_button.winfo_height()

    return root

def label_w_h(proportion, max_height, max_width):
    # width based on max_height
    w = int(proportion * max_height)

    if w <= max_width:
        return w, max_height
    else:
        return max_width, int(max_width / proportion)


def picture():
    """ With Static image in root """
    # test with a sample picture.
    # for picamera, do camera.resolution = (1024, 768)
    path = "img/windowsPhone.jpg"
    # convert picture to PIL format
    image = Image.open(path)
    # resize the PIL image
    image_width, image_height = image.size
    image_proportion = image_width*1.0/image_height
    resize = label_w_h(image_proportion, screen_height, screen_width)
    image = image.resize(resize, Image.ANTIALIAS)
    # convert PIL image to Tk image
    img = ImageTk.PhotoImage(image)
    # draw image in Label
    image_l = Label(root, image=img, height=label_height, width=screen_width)
    # Label grid.
    image_l.grid(row=0, column=0, columnspan=3, sticky='EW')

    root.mainloop()

def camera():
    camera = PiCamera()
    camera_height = 1040
    camera_width = 1280
    camera.resolution = (camera_width, camera_height)
    camera.framerate = 32
    
    return camera


def live_feed():
    """ With picamera image in root. """
    camera = camera()
    
    cap = PiRGBArray(camera, size=(camera_width, camera_height))

    for i in camera.capture_continuous(cap, format='bgr', use_video_port=True):
        image = i.array  # image.size gives a single integer.
        # Image.shape gives a (height, width, channel) array

        # Reading the image for QR code
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        # convert the images to PIL format...
        pil = Image.fromarray(image)
        # convert from PIL format to raw for zbar scanning.
        width, height = pil.size
        print("before resizing", width, height)
        image_proportion = width*1.0/height
        resize = label_w_h(image_proportion, screen_height, screen_width)
        pil = pil.resize(resize, Image.ANTIALIAS)
        print("after resizing", resize)
        
        image = ImageTk.PhotoImage(pil)  # ...and then to ImageTk format
        # Show image in root.
        image_l = Label(root, image=image, height=label_height, width=screen_width)
        # Label grid.
        image_l.grid(row=0, column=0, columnspan=3, sticky='EW')
        
        
        # Create a reader
        # scan_image = zbar.Image(width, height, 'Y800', raw)
        # scanner.scan(scan_image)
        # Extract result
        # for symbol in scan_image:
            # returns a beep sound.
            # playBeep()
            # last_message = symbol.data    
            # Match data with DB and mark attendance, log timestamp
            # Fetch data from DB and returns a pop-up message
            # print "The QR code says: %s" %symbol.data  # for the moment the encoded symbol is printed on the console
            # Save the file after scanning.
            # self.__savefile__()
                
        cap.truncate(0)
        # cap.truncate()
        # cap.seek(0)
        #if process(cap):
            # break
        # key = cv2.waitKey(1) & 0xFF
        # if key  == ord("q"):
                # break
        root.mainloop()
        image_l.grid_forget()
        
    root.mainloop()
    
    
def photobooth():
    # import the necessary packages
    # from __future__ import print_function  # Required but place in from of the script in main.py
    from photoboothapp import PhotoBoothApp
    from imutils.video import VideoStream
    import argparse
    import time
     
    # construct the argument parse and parse the arguments
    ap = argparse.ArgumentParser()
    # ap.add_argument("-o", "--output", required=True, help="path to output directory to store snapshots")
    ap.add_argument("-o", "--output", required=False, help="path to output directory to store snapshots")
    ap.add_argument("-p", "--picamera", type=int, default=-1, help="whether or not the Raspberry Pi camera should be used")
    args = vars(ap.parse_args())
     
    # initialize the video stream and allow the camera sensor to warmup
    print("[INFO] warming up camera...")
    # vs = VideoStream(usePiCamera=args["picamera"] > 0).start()
    vs = VideoStream(usePiCamera=1, resolution=(320, 240), framerate=32).start()
    time.sleep(2.0)
     
    # start the app
    pba = PhotoBoothApp(vs, args["output"])
    pba.root.mainloop()

# picture()
# root = gui()
# live_feed()
# root.mainloop() # try this instead of main loop https://stackoverflow.com/questions/29158220/tkinter-understanding-mainloop

photobooth()