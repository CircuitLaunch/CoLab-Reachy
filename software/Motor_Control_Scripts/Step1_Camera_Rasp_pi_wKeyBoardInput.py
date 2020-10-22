'''
This is a code that runs on Rasp pi.

What it does: Allowing the user to input keyboard commands and communicate
them (say number 1 or 0) over I2C.

Rasp Pi controls the Arduino


'''
from picamera import PiCamera
from time import sleep
import sys

from smbus2 import SMBus


addr = 0x8 # bus address
bus = SMBus(1) # indicates /dev/ic2-1

numb = 1

print ("Enter 1 for ON or 0 for OFF")
while numb == 1:

        ledstate = input(">>>>   ")

        if ledstate == "1":
                bus.write_byte(addr, 0x1) # switch it on
        elif ledstate == "0":
                bus.write_byte(addr, 0x0) # switch it on
        else:
                numb = 0



camera = PiCamera()
#camera.rotation = 90 # comment out if your camera is in correct orientation

camera.start_preview(alpha=200) # Add alpha parameter to make it slightly see through in ops - adjust to different resolution
sleep(5) # at least 2 seconds so that camera can sense lighting conditions
camera.capture('testimage.jpg') # change location and file name, if needed
camera.stop_preview()

sys.exit() # esc in case of issues, added to make sure no system hang