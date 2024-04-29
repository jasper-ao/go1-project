from go1_functions import *
from time import sleep


led = led_setup()

for ele in ['red', 'green', 'blue', 'yellow', 'white']:
    led.led_on(ele)
    sleep(.5)
led.led_off()

led.child.close()
