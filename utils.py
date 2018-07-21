import zbar
import cv2
from PIL import Image
import tkMessageBox
from beep import playBeep

scanner = zbar.ImageScanner()

def find_qr(frame, last_message):
    # return None
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY, dstCn=0)
    pil = Image.fromarray(gray)
    width, height = pil.size
    raw = pil.tobytes()
    image = zbar.Image(width, height, 'Y800', raw)
    scanner.scan(image)
    # Extract result
    for symbol in image:
        if last_message == symbol.data:
            continue
        playBeep()
        # returns a beep sound.
        # Match data with DB and mark attendanc
        # Fetch data from DB and returns a pop-up message
        print "The QR code says: %s" %symbol.data
        return symbol.data

def find_name(df, data, filename=None, columname="EID"):
    house = "your"
    loc = df[df[columname]==data].index
    if loc.shape[0] > 0:  # if the name is in df
        df.loc[loc, 'attendance'] = "Y"
        # retrieve house name
        house = "the " + df.loc[loc, "house"].values[0]
    else:  # else the name has not RSVP
        # add name into df
        loc = df.index.max() + 1
        df.loc[loc, columname] = data
        df.loc[loc, 'attendance'] = "Y"
        df.loc[loc, 'house'] = "-"
        # find house from the H&PS namelist
    if filename is not None:
        df.to_csv(filename, index=False, encoding='utf-8')
    return house, df

def show_message(msg):
    """ Shows a message box with the message and an "OK" button. """
    tkMessageBox.showinfo('Welcome', msg)

def show_warning():
    tkMessageBox.showwarning("WARNING", "The RSVP file has not been loaded yet!")
