from go1_functions import *
import cv2

camera = camera_setup()

while True:
    res = camera.get_image(1, 1)
    cv2.imshow('camera', res)

    if cv2.waitKey(33) == ord('q'):
        break

camera.driver.quit()
