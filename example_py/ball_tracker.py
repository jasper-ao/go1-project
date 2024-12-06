from go1_functions import *
import numpy as np
import cv2
from math import pi
import pynput.keyboard as keyboard
from time import time, sleep


setup()
camera = camera_setup()

inSearch = False
inReturn = False
inRotate = False
def on_press(key):
    global inSearch, inReturn, walkedTime, inRotate
    if key == keyboard.Key.shift_l and not inSearch:
        walkedTime = 0
        inSearch = True
    elif key == keyboard.Key.shift_r and inSearch and not inReturn:
        inReturn = True

    elif key == keyboard.Key.ctrl_l and inSearch:
        walkedTime = 0
        inSearch = False
        inReturn = False
        inRotate = False

listener = keyboard.Listener(on_press=on_press).start()


walkedTime = 0
def main():
    global walkedTime, inRotate

    while True:
        img = camera.get_image(1,0)
        img = cv2.rectangle(img, [0,0],[358,190], [0,0,0], -1)
        cv2.imshow('img', img)

        if inSearch:
            startTime = time()

            mask = maskImage(img)
            mask = cv2.copyMakeBorder(mask, 1,1,1,1, cv2.BORDER_CONSTANT, value=0)
            cv2.imshow('mask', mask)
            
            goToBall(mask, img)

            endTime = time()
            if not inRotate:
                walkedTime += endTime-startTime + 0.1
            elif inRotate:
                inRotate = False
            # print(walkedTime)
        
        cv2.waitKey(100)


def maskImage(img):
    hsvimg = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

    orangeLower = np.array([0,30,0], np.uint8)
    orangeUpper = np.array([20,255,255], np.uint8)
    orangeMask = cv2.inRange(hsvimg, orangeLower, orangeUpper)

    redLower = np.array([155,30,0], np.uint8)
    redUpper = np.array([180,255,255], np.uint8)
    redMask = cv2.inRange(hsvimg, redLower, redUpper)

    mask = cv2.bitwise_or(orangeMask, redMask)
    return mask


def goToBall(mask, img):
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
    # if max(results) < .5: return

    targetContour = contours[results.index(max(results))]
    (x,y), radius = cv2.minEnclosingCircle(targetContour)
    # (y360, x358, 3)

    global inRotate
    if x < 358//2 - 20:
        move(0,0, .2)
        inRotate = True
    elif x > 358//2 + 20:
        move(0,0, -.2)
        inRotate = True
    
    else:
        if radius < 10:
            move(.8)
        
        elif radius >= 10:
            # print('stopped')
            global inSearch, inReturn, walkedTime
            print(f'-------------final: {walkedTime}-------------')

            while not inReturn: pass

            while walkedTime > 0 and inSearch:
                startTime = time()

                move(-.8)
                sleep(.1)

                endTime = time()
                walkedTime -= endTime-startTime
                # print(walkedTime)
                        
            inSearch = False
            inReturn = False
            walkedTime = 0
            print('=====================')

    cv2.drawContours(img, targetContour, -1, 150, 4)
    cv2.imshow('img', img)

    cv2.drawContours(mask, targetContour, -1, 150, 8)
    cv2.imshow('mask', mask)


main()
