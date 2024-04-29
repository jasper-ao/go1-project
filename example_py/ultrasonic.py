from go1_functions import *


ultrasonic = ultrasonic_setup()
for i in range(200):
    print(ultrasonic.get_ultrasonic())

ultrasonic.child.close()
