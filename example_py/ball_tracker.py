from go1_functions import *
import numpy as np
import cv2
from math import pi
from keyboard import is_pressed
from time import time, sleep


class main:
    def __init__(self):
        setup()
        self.camera = camera_setup()
        
        self.targetContour = None
        self.x, self.y, self.radius = None, None, None
        self.walkedTime = 0

        self.inTrack = False


    def getImage(self):
        self.img = self.camera.get_image(1,0)


    def findBall(self):       
        hsvimg = cv2.cvtColor(self.img, cv2.COLOR_BGR2HSV)

        orangeLower = np.array([0,30,0], np.uint8)
        orangeUpper = np.array([20,255,255], np.uint8)
        orangeMask = cv2.inRange(hsvimg, orangeLower, orangeUpper)

        redLower = np.array([155,30,0], np.uint8)
        redUpper = np.array([180,255,255], np.uint8)
        redMask = cv2.inRange(hsvimg, redLower, redUpper)

        mask = cv2.bitwise_or(orangeMask, redMask)
        mask = cv2.copyMakeBorder(mask, 1,1,1,1, cv2.BORDER_CONSTANT, value=0)

        contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

        results = []
        for contour in contours:
            (x,y), radius = cv2.minEnclosingCircle(contour)

            if radius > 2:
                area = cv2.contourArea(contour)
                result = area / (pi*radius**2)
                results.append(result)
        else: results.append(-1)
        
        if not len(results): return
        if max(results) < 0.1: return

        self.targetContour = contours[results.index(max(results))]
        (self.x, self.y), self.radius = cv2.minEnclosingCircle(self.targetContour)


    def trackBall(self):
        if self.x < 358//2 - 15:
            move(0,0, .2)
        elif self.x > 358//2 + 15:
            move(0,0, -.2)
        
        else:
            if self.radius < 10:
                s = time()
                move(.8)
                e = time()
                self.walkedTime += e-s + 0.1
            
            elif self.radius >= 10:
                while True:
                    if is_pressed('ctrl'):
                        self.returnToPos()
                        break


    def returnToPos(self):
        while self.walkedTime > 0:
            s = time()
            move(-.8)
            sleep(.1)
            e = time()

            self.walkedTime -= e-s
        
        self.targetContour = None
        self.x, self.y, self.radius = None, None, None
        self.walkedTime = 0

        self.inTrack = False



go1 = main()

while True:
    go1.getImage()
    cv2.imshow('camera', go1.img)

    if is_pressed('shift'):
        go1.inTrack = True

        while go1.inTrack:
            go1.getImage()
            cv2.imshow('camera', go1.img)

            go1.findBall()
            try: go1.trackBall()
            except TypeError: pass
            
            cv2.waitKey(100)

    cv2.waitKey(100)
