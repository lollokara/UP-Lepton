import cv2
from PIL import Image
import subprocess
import numpy as np



class VideoCamera(object):
    def __init__(self):
        print("Via")

    def get_frame(self): #exec
        bashCommand = "./lepton_capture"
        process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
        output, error = process.communicate()
        #print(output)
        bashCommand = "convert imageResized.pgm frameResized.png"
        process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
        output, error = process.communicate()
        #print(output)

        image = cv2.imread("frameResized.png")
        with open('image.txt') as f:
            for line in f:
                MaxVal=int(line)
                    #print(MaxVal)
        image = cv2.resize(image, (0,0), fx=10, fy=10)
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        (minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(gray)
        image = cv2.applyColorMap(image, cv2.COLORMAP_JET)
        PixelTemp= 0.0463*MaxVal-349.44
        print(PixelTemp)
        cv2.circle(image, maxLoc, 10, (255, 255, 255), 3)
        PixelTemp=round(PixelTemp,2)
        cv2.putText(image,str(PixelTemp)+"C",(680,590),cv2.FONT_HERSHEY_SIMPLEX,1,(255,255,255),2)
        ret, jpeg = cv2.imencode('.png', image)
        return jpeg.tostring()


def normalize(arr):
    arr = arr.astype('float')
    # Do not touch the alpha channel
    minval = arr[...,0].min()
    maxval = arr[...,0].max()
    if minval != maxval:
        arr[...,0] -= minval
        arr[...,0] *= (255.0/(maxval-minval))
    return arr
