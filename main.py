#!/usr/bin/env python
#
# Project: Video Streaming with Flask
# Author: lorenzo [at] karavania [dot] com>
# Date: 2016/11/2
# Website: http://karavania.com
#


from flask import Flask, render_template, Response
from camera import VideoCamera
from PIL import Image
import subprocess
import cv2

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

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
def video_feed():
    
    return render_template('rec.html')

if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
