import time

from gui import Gui

from imutils.video import VideoStream


vs = VideoStream(usePiCamera=1, resolution=(320, 360), framerate=32).start()  # original framerate=32
time.sleep(2.0)

msg = '''Hi %s!
Welcome to the <event>!'''
scanner = Gui(vs, found_msg=msg)  # Create the root
scanner.widgets()  # Initialize widget without display them
scanner.grid_layout()  # Display the widgets
scanner.main_loop()
