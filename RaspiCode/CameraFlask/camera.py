#Modified by smartbuilds.io
#Date: 27.09.20
#Desc: This scrtipt script..

import cv2
from imutils.video.pivideostream import PiVideoStream
import imutils
import time
import numpy as np
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

class VideoCamera(object):
    def __init__(self, flip = False):
        self.vs = PiVideoStream().start()
        self.flip = flip
        time.sleep(2.0)

    def __del__(self):
        self.vs.stop()

    def flip_if_needed(self, frame):
        if self.flip:
            return np.flip(frame, 0)
        return frame

    def get_frame(self):
        frame = self.flip_if_needed(self.vs.read())
        ret, jpeg = cv2.imencode('.jpg', frame)
        return jpeg.tobytes()
