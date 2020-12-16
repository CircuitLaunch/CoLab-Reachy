import pathlib
import numpy as np
from collections import OrderedDict
import time
from .dynamixel import attach_dxl_motors

class Head(object):
    head_dxl_motors = OrderedDict([
        ('left_antenna', {
            'id': 30, 'offset': 0.0, 'orientation': 'direct',
            'angle-limits': [-150, 150],
        }),
        ('right_antenna', {
            'id': 31, 'offset': 0.0, 'orientation': 'direct',
            'angle-limits': [-150, 150],
        }),
    ])

    def __init__(self, io):
        self.io = io

        self.antennas = attach_dxl_motors(self.io, "head", Head.head_dxl_motors)

        for m in self.antennas:
            self.antennas[m].compliant = False

    def move_left_antenna(self, goal_position):
        self.antennas['left_antenna'].goal_position = goal_position

    def move_right_antenna(self, goal_position):
        self.antennas['right_antenna'].goal_position = goal_position

    def sample_motion(self):
        self.move_left_antenna(150)
        time.sleep(5)
        self.move_left_antenna(0)
        time.sleep(5)
        self.move_left_antenna(-150)
        time.sleep(5)
        self.move_right_antenna(150)
        time.sleep(5)
        self.move_right_antenna(0)
        time.sleep(5)
        self.move_right_antenna(-150)



