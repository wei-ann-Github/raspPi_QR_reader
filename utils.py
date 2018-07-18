import zbar
import cv2
from beep import playBeep
from PIL import Image

scanner = zbar.ImageScanner()

def find_qr(frame):
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY, dstCn=0) 
    pil = Image.fromarray(gray)
    width, height = pil.size
    raw = pil.tobytes()
    # Create a reader
    image = zbar.Image(width, height, 'Y800', raw)
    scanner.scan(image)
    # Extract result
    for symbol in image:
        # returns a beep sound.
        playBeep()
        # Match data with DB and mark attendanc
        data = symbol.data
        return data

def find_name(df, name, columname="EID"):    
    loc = df[df[columname]==name].index
    if loc.shape[0] > 0:  # if the name is in df
        df.loc[loc, 'attendance'] = "Y"
        # retrieve house name
        house = df.loc[loc, "house"]
    else:  # else the name has not preregistered
        # add name into df
        loc = df.index.max() + 1
        df.loc[loc, columname] = name
        df.loc[loc, 'attendance'] = "Y"
        # find house from the H&PS namelist
    
    return house
    