imoprt picamera

camera = picamera.PiCamera()

try:
    camera.start_preview()
    camera.sleep(10)
    camera.stop_preview()
finally:
    camera.close()