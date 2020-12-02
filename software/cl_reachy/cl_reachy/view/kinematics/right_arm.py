import pathlib
import numpy as np
from collections import OrderedDict
import time
from .dynamixel import attach_dxl_motors

class RightArm(object):
    right_arm_dxl_motors = OrderedDict([
        ('shoulder_pitch', {
            'id': 10, 'offset': 90.0, 'orientation': 'indirect',
            'angle-limits': [-180, 60],
            'link-translation': [0, -0.19, 0], 'link-rotation': [0, 1, 0],
        }),
        ('shoulder_roll', {
            'id': 11, 'offset': 90.0, 'orientation': 'indirect',
            'angle-limits': [-100, 90],
            'link-translation': [0, 0, 0], 'link-rotation': [1, 0, 0],
        }),
        ('arm_yaw', {
            'id': 12, 'offset': 0.0, 'orientation': 'indirect',
            'angle-limits': [-90, 90],
            'link-translation': [0, 0, 0], 'link-rotation': [0, 0, 1],
        }),
        ('elbow_pitch', {
            'id': 13, 'offset': 0.0, 'orientation': 'indirect',
            'angle-limits': [0, 125],
            'link-translation': [0, 0, -0.28], 'link-rotation': [0, 1, 0],
        }),
    ])

    def __init__(self, io):
        self.io = io

        self.arm_motors = attach_dxl_motors(self.io, "right_arm", RightArm.right_arm_dxl_motors)

        for m in self.arm_motors:
            self.arm_motors[m].compliant = False

    def move_part(self, name, goal_position):
        self.arm_motors[name].goal_position = goal_position

    def move_shoulder_pitch(self, goal_position):
        # TODO: add limits
        self.move_part('shoulder_pitch', goal_position)

    def move_shoulder_roll(self, goal_position):
        # TODO: add limits
        self.move_part('shoulder_roll', goal_position)

    def move_arm_yaw(self, goal_position):
        # TODO: add limits
        self.move_part('arm_yaw', goal_position)

    def move_elbow_pitch(self, goal_position):
        # TODO: add limits
        self.move_part('elbow_pitch', goal_position)

    def sample_motion(self):
        goal_positions = [0.0, -1.0, -2.0, -4.0, -8.0, -16.0, -32.0, -64.0,
                            -32.0, -16.0, -8.0, -4.0, -2.0, -1.0, 0.0]

        for goal_position in goal_positions:
            print(goal_position)
            self.move_elbow_pitch(goal_position)
            time.sleep(0.5)
