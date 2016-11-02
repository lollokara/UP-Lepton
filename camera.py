#
# Project: Lepton Streaming and recording with Flask
# Author: lorenzo [at] karavania [dot] com>
# Date: 2016/11/2
# Website: http://karavania.com
#


import cv2
from PIL import Image
import subprocess
import numpy as np



class VideoCamera(object):
    def __init__(self):
        print("Via")

    def get_frame(self): #exec
        bashCommand = "./lepton_capture" #Gets the frame from the C code that saves the frame on disk
        process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
        output, error = process.communicate()
        #print(output)
        bashCommand = "convert imageResized.pgm frameResized.png" #Converts the unusable format PGM to OpenCV Friendly one
        process = subprocess.Popen(bashCommand.split(), stdout=subprocess.PIPE)
        output, error = process.communicate()
        #print(output)
        image = cv2.imread("frameResized.png") #Loads the frame
        with open('image.txt') as f:
            for line in f:
                MaxVal=int(line) #reads the raw max value
                    #print(MaxVal)
        image = cv2.resize(image, (0,0), fx=10, fy=10) #Scaling... 80*60 is too small
        gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
        (minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(gray)
        image = cv2.applyColorMap(image, cv2.COLORMAP_JET) #Add the colormap
        PixelTemp= 0.0463*MaxVal-349.44 #Formula found around internet to get an estimate temperature
        #print(PixelTemp)
        cv2.circle(image, maxLoc, 10, (255, 255, 255), 3) #Draw a cirle around the hottest point
        PixelTemp=round(PixelTemp,2)
        cv2.putText(image,str(PixelTemp)+"C",(680,590),cv2.FONT_HERSHEY_SIMPLEX,1,(255,255,255),2) #Writes the temp...

        return image #return the whole frame
