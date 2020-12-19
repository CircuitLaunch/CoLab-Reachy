%matplotlib notebook

import time
import cv2 as cv
import numpy as np

from matplotlib import pyplot as plt

from reachy import Reachy, parts

reachy = Reachy(
    #head=parts.Head(io='/dev/ttyUSB*'),
    head=parts.Head(io='ws'),
)
for m in reachy.head.motors:
    m.compliant = False
    

for m in reachy.head.motors:
    m.goal_position = 45
    time.sleep(0.1)

for m in reachy.head.motors:
    m.goal_position = 0
    time.sleep(0.1)

for m in reachy.head.motors:
    m.goal_position = -45
    time.sleep(0.1)

for m in reachy.head.motors:
    m.goal_position = 0
    time.sleep(0.1)

for m in reachy.head.motors:
    m.goal_position = 45
    time.sleep(0.1)

for m in reachy.head.motors:
    m.goal_position = 0
    time.sleep(0.1)
    
for m in reachy.head.motors:
    m.goal_position = -45
    time.sleep(0.1)