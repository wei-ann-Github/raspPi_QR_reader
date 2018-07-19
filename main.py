from gui import Gui
from time import sleep
from imutils.video import VideoStream


vs = VideoStream(usePiCamera=True, resolution=(320, 240), framerate=32).start()

msg = '''Hi %s!
Welcome to the <event>!'''
scanner = Gui(vs, msg_if_found=msg)  # Create the root
scanner.widgets()  # Initialize widget without display them
scanner.grid_layout()  # Display the widgets
scanner.main_loop()
