from go1_functions import *
from time import sleep


speaker = audio_setup()

speaker.set_volume(20)
speaker.play_audio('beep.wav')

sleep(.5)

speaker.set_volume(10)
speaker.play_audio('beep.wav')

speaker.child.close()
