%matplotlib notebook

import time
import numpy as np

from matplotlib import pyplot as plt

from reachy import Reachy, parts

#Change this for USB port
reachy = Reachy(
    #right_arm=parts.RightArm(io='/dev/ttyUSB*', hand='force_gripper'),
    right_arm=parts.RightArm(io='ws', hand='force_gripper'),
)

for m in reachy.right_arm.motors:
    m.compliant = False

    #Wave Frame 1, bring arm up
reachy.goto({
    'right_arm.shoulder_pitch': -20,
    'right_arm.shoulder_roll': -10,
    'right_arm.arm_yaw': -10,    
    'right_arm.elbow_pitch': -120,
    'right_arm.hand.forearm_yaw': 0,
    'right_arm.hand.wrist_pitch': 0,
    'right_arm.hand.wrist_roll': 0,
    'right_arm.hand.gripper': 0,
}, duration=2, wait=True)

#Wave Frame 2 (Hand Wave)
reachy.goto({

    'right_arm.hand.wrist_roll': 40,
    'right_arm.hand.gripper': 0,
}, duration=0.75, wait=True)

reachy.goto({

    'right_arm.hand.wrist_roll': -40,
    'right_arm.hand.gripper': 0,
}, duration=0.75, wait=True)

reachy.goto({

    'right_arm.hand.wrist_roll': 40,
    'right_arm.hand.gripper': 0,
}, duration=0.75, wait=True)

reachy.goto({

    'right_arm.hand.wrist_roll': -40,
    'right_arm.hand.gripper': 0,
}, duration=0.75, wait=True)

sleep(2) #wait 2 seconds

#Wave Frame 3, return to home position
reachy.goto({
    'right_arm.shoulder_pitch': 0,
    'right_arm.shoulder_roll': 0,
    'right_arm.arm_yaw': 0,    
    'right_arm.elbow_pitch': 0,
    'right_arm.hand.forearm_yaw': 0,
    'right_arm.hand.wrist_pitch': 0,
    'right_arm.hand.wrist_roll': 0,
    'right_arm.hand.gripper': 0,
}, duration=2, wait=True)