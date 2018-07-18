import cv2
import cv2.cv as cv
import Image
import picamera
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import zbar

from beep import playBeep

camera = PiCamera()
HEIGHT, WIDTH = 400, 400
camera.resolution = (WIDTH, HEIGHT) # (width, height)
camera.framerate = 32
cap = PiRGBArray(camera, size=(WIDTH, HEIGHT))

scanner = zbar.ImageScanner()
last_message = None

for i in camera.capture_continuous(cap, format='bgr', use_video_port=True):
	frame = i.array

	# using openCV to display a camera preview window
	image = cv2.resize(frame, (48, 48))
	cv2.imshow("winQR reader", frame)

	# Reading the image for QR code
	gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY, dstCn=0)
	pil = Image.fromarray(gray)
	width, height = pil.size
	raw = pil.tobytes()
	# Create a reader
	image = zbar.Image(width, height, 'Y800', raw)
	scanner.scan(image)
	# Extract result
	for symbol in image:
		playBeep()
		last_message = symbol.data
		# returns a beep sound.
		# Match data with DB and mark attendanc
		# Fetch data from DB and returns a pop-up message
		print "The QR code says: %s" %symbol.data
		time.sleep(3)
	cap.truncate(0)
	key = cv2.waitKey(1) & 0xFF
	if key  == ord("q"):
		break

camera.close()
cv2.destroyAllWindows()
