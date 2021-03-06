#!/usr/bin/env python
#
# Project: Lepton Streaming and recording with Flask
# Author: lorenzo [at] karavania [dot] com>
# Date: 2016/11/2
# Website: http://karavania.com
#


from flask import Flask, render_template, Response,redirect, url_for, request
from camera import VideoCamera
from PIL import Image
import subprocess
import cv2
import mraa
app = Flask(__name__)

def gen(camera):
    while True:
        frame = camera.get_frame()
        ret, jpeg = cv2.imencode('.png', frame)
        frame=jpeg.tostring()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/live')
def video_feed():
    return Response(gen(VideoCamera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/rec')
def record():
    camera=VideoCamera()
    frame = camera.get_frame() #Gets the frame
    fourcc = cv2.cv.CV_FOURCC('M','J','P','G') #Codec Stuff
    video = cv2.VideoWriter('video.avi',fourcc,5,(800,600)) #Opens a video file
    print("recording")
    ledstate=0 #GPIO  STUFF
    led=mraa.Gpio(4,False,True)
    led.dir(mraa.DIR_OUT)
    while True:
        if ledstate == 0:
            led.write(1)
            ledstate=1
        else:
            led.write(0)
            ledstate=0
        frame = camera.get_frame()
        video.write(frame)


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
