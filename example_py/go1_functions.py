#!/usr/bin/python
import sys

sys.path.append('../lib/python/amd64')
import robot_interface as sdk
import pexpect
from selenium import webdriver
from urllib.request import urlopen
import numpy as np
import cv2


def setup():
    global udp, cmd, state
    HIGHLEVEL = 0xee
    udp = sdk.UDP(HIGHLEVEL, 8080, '192.168.123.161', 8082)
    cmd = sdk.HighCmd()
    state = sdk.HighState()
    udp.InitCmdData(cmd)

def reset():
    udp.Recv()
    udp.GetRecv(state)
    
    cmd.mode = 0
    cmd.gaitType = 0
    cmd.speedLevel = 0
    cmd.footRaiseHeight = 0
    cmd.bodyHeight = 0
    cmd.euler = [0, 0, 0]
    cmd.velocity = [0, 0]
    cmd.yawSpeed = 0.0
    cmd.reserve = 0


def move(vx: float, vy: float=0, rotate: float=0): # FOR POSITIVE VALUES | vx: front (m/s) | vy: left (m/s) | rotate: anti-clockwise (rad/s)
    cmd.mode = 2
    
    cmd.velocity = [vx, vy]
    cmd.yawSpeed = rotate

    udp.SetSend(cmd)
    udp.Send()

def look(values: list): # [roll, pitch, yaw] FOR POSITIVE VALUES | roll: rotate clockwise around x-axis | pitch: look down | yaw: look left || all is (rad)
    cmd.mode = 1

    cmd.euler = values

    udp.SetSend(cmd)
    udp.Send()


class speaker_setup:
    def __init__(self) -> None:
        self.child = pexpect.spawn('ssh pi@192.168.12.1')

        self.child.expect('pi@192.168.12.1\'s password: ')
        self.child.sendline('123')

        self.child.sendline('ssh unitree@192.168.123.13')
        self.child.expect('unitree@192.168.123.13\'s password: ')
        self.child.sendline('123')

        self.child.sendline('cd audio')
        self.child.sendline('echo speaker setup finished')

        while True:
            self.child.expect('\r\n')
            if self.child.before == b'speaker setup finished': break

    def play_audio(self, file: str):
        self.child.sendline(f'aplay -D plughw:2,0 {file}')
        self.child.sendline('echo audio played')
        while True:
            self.child.expect('\r\n')
            if self.child.before == b'audio played': break
    def set_volume(self, volume: float):
        self.child.sendline(f'amixer -c 2 set Speaker {volume}')

class led_setup:
    def __init__(self) -> None:
        self.child = pexpect.spawn('ssh pi@192.168.12.1')

        self.child.expect('pi@192.168.12.1\'s password: ')
        self.child.sendline('123')

        self.child.sendline('ssh unitree@192.168.123.13')
        self.child.expect('unitree@192.168.123.13\'s password: ')
        self.child.sendline('123')

        self.child.sendline('cd Unitree/sdk/faceLightSDK_Nano/bin')
        self.child.sendline('echo LED setup finished')

        while True:
            self.child.expect('\r\n')
            if self.child.before == b'LED setup finished': break

    def led_on(self, color: str): # white, black(off), red, green, blue, yellow
        self.child.sendline(f'./{color}')
        self.child.expect('\n')
        self.child.send('\003')
    def led_off(self):
        self.child.sendline('./black')
        self.child.expect('\n')
        self.child.send('\003')

class ultrasonic_setup:
    def __init__(self) -> None:
        self.child = pexpect.spawn('ssh pi@192.168.12.1')

        self.child.expect('pi@192.168.12.1\'s password: ')
        self.child.sendline('123')
        self.child.sendline('~/Unitree/autostart/utrack/ultrasonic_listener_example/bin/ultrasonic_listener_lcm')

        while True:
            self.child.expect('\r\n')
            if self.child.before == b'The ultrasonic listener is initialized!': break

    def get_ultrasonic(self): # return [front, right, left, back]
        self.child.expect('\r\n')
        output = self.child.before.decode('utf-8')
        output = [ele for ele in output.split(' ') if ele]
        output = [output[6], output[9], output[12], output[15]]

        output = [float(ele) for ele in output]
        return output

class camera_setup:
    def __init__(self) -> None:
        self.driver = webdriver.Firefox()
        self.driver.get('http://192.168.123.161/vision')

    def get_image(self, camera_type: int, image_type: int=0): # CAMERA TYPE | 0: left | 1: front | 2: right | 3: bottom front || IMAGE TYPE (ONLY FOR 0-2) | 0: adjusted | 1: raw
        if camera_type in [0,1,2]:
            cmd = f'''
                list = document.getElementsByClassName('canvasContainer')
                canvas = list[{camera_type}].querySelectorAll('canvas')[{image_type}]
                return canvas.toDataURL()
                '''
        elif camera_type == 3:
            cmd = f'''
                list = document.getElementsByClassName('canvasContainer')
                canvas = list[{camera_type}].querySelectorAll('canvas')[0]
                return canvas.toDataURL()
                '''
        

        data_uri = self.driver.execute_script(cmd)
        with urlopen(data_uri) as response: data = response.read()
        data = bytearray(data)

        img = np.asarray(data, dtype='uint8')
        img = cv2.imdecode(img, cv2.IMREAD_COLOR)

        return img


if __name__ == '__main__':
    pass
