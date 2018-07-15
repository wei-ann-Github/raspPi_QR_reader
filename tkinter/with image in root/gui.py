import tkFileDialog

import pandas as pd
import cv2


def openfile():
    filename = tkFileDialog.askopenfilename()
    if filename.endswith('csv'):
        df = pd.read_csv(filename)
    elif filename.endswith('xlsx') or path.endswith('xls'):
        df = pd.read_excel(filename)

    colname = df.columns
    print(colname)

def scan():
    return
