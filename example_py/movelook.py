from go1_functions import *
from time import sleep


setup()
for i in range(12000):
    reset()

    if i < 1000: move(.2)
    elif i < 2000: move(-.2)

    elif i < 3000: move(0, .2)
    elif i < 4000: move(0, -.2)

    elif i < 5000: move(0,0, .3)
    elif i < 6000: move(0,0, -.3)
    
    elif i < 7000: look([.3, 0,0])
    elif i < 8000: look([-.3, 0,0])
    
    elif i < 9000: look([0, .2, 0])
    elif i < 10000: look([0, -2, 0])

    elif i < 11000: look([0,0, .15])
    elif i < 12000: look([0,0, -.15])
    
    sleep(.001)
