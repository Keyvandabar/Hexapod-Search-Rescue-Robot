#Modified by smartbuilds.io
#Date: 27.09.20
#Desc: This web application serves a motion JPEG stream
# main.py
# import the necessary packages
from flask import Flask, render_template, Response, request
from camera import VideoCamera
import time
import threading
import os
'''
/*
**********************************************
Title: Pi Camera Stream Flask
Author: Eben Kouao
Date: Oct 10, 2020
Code version: *
Availability: https://github.com/EbenKouao/pi-camera-stream-flask
- The primary function of this code allowed me to get a good introduction to opening and 
streaming a flask camera stream with little to no latency in the video stream. After countless
attempts at trying different methods of streaming the video I found this github and source
to provide the best quality vs latency ratio and decided to adopt it to the program.
*** THE PRIMARY FUNCTION OF THIS CODE IS TO ONLY STREAM THE VIDEO TO A LOCAL HTML PAGE
***************************************************
*/
'''
pi_camera = VideoCamera(flip=False) # flip pi camera if upside down.

# App Globals (do not edit)
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html') #you can customze index.html here

def gen(camera):
    #get camera frame
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen(pi_camera),
                    mimetype='multipart/x-mixed-replace; boundary=frame')
@app.route('/',methods=["GET"])  
def getMethod():    
    return "This is GET method" 


if __name__ == '__main__':
    #app.run(debug=True)
    app.run(host='0.0.0.0', debug=False)
    


