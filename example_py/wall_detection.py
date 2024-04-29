from go1_functions import *


ultrasonic = ultrasonic_setup()
setup()

try:
    while True:
        front, right, left, back = ultrasonic.get_ultrasonic()
        reset()

        vx, vy, = 0, 0
        if front < .3: vx += -.2
        if right < .3: vy += .2
        if left < .3: vy += -.2
        if vx == vy == 0: vx = .2

        move(vx, vy)

except KeyboardInterrupt:
    ultrasonic.child.close()
