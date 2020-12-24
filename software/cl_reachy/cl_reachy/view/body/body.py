import os
import numpy as np
import platform
import time
#from . import config
from ...node import NodeBase
from reachy import Reachy, parts
from .action import ActionQueue
from .patch import patch_head, patch_right_arm

REACHY_SIM = os.environ['REACHY_SIM'] if 'REACHY_SIM' in os.environ.keys() else 0

class Body(NodeBase):
    def __init__(self, node_name="speechsynthesis", host="127.0.0.1", port=1883,
                    username=None, password=None, subscribe_dict={}, run_sleep=0.1):
        super().__init__(node_name, host, port, username, password, subscribe_dict, run_sleep)

        self.io = '/dev/ttyUSB*'

        if platform.uname().machine == 'armv7l':
            # If it's 'armv7l', assume that it's the raspberry pi 4 on the real Reachy.
            # Patch the offsets and don't load the orbita.
            self.io = "ws"
            parts.Head = patch_head(parts.Head)
            parts.RightArm = patch_right_arm(parts.RightArm)

        self.reachy = Reachy(head=parts.Head(io=self.io), right_arm=parts.RightArm(io='ws', hand='force_gripper'),)

        self.running = True

        command_input = input("press enter after connecting to Reachy>")

        self.initialize()

        self.add_subscribe('+/body/init', self.handle_initialize)
        self.add_subscribe('+/body/shutdown', self.handle_shutdown)
        self.add_subscribe('+/body/stop', self.handle_force_stop)
        self.add_subscribe('+/body/right_arm/wave', self.handle_wave_arm)
        self.add_subscribe('+/body/head/antenna/wiggle', self.handle_wiggle_antennas)
        self.add_subscribe('+/body/head/antenna/zero', self.handle_wave_arm)
        self.add_subscribe('+/body/right_arm/zero', self.handle_wiggle_antennas)

        self.state = ActionQueue.RUNNING

    def initialize(self):
        # move to the stop state for now
        self.state = ActionQueue.STOPPED

        self.set_compliance_all(False)

        # move to zero
        self.move_all_to_zero()

        # turn compliance back on
        self.set_compliance_all(True)

        # turn the fans on for the arm
        self.turn_on_fans()

        # only set the status to RUNNING after everything has been initialized
        self.state = ActionQueue.RUNNING

        self.state = ActionQueue.IDLE
        self.action_queue = ActionQueue(self)

        self.action_queue.run()

    def handle_initialize(self, client=None, userdata=None, message=None):
        self.initialize()

    def shutdown(self, client=None, userdata=None, message=None):
        self.state = ActionQueue.STOPPED

        # set to status to STOPPED first
        self.clear_action_queue()
        self.set_compliance_all(False)

        # move to zero
        self.move_all_to_zero()

        # turn compliance back on
        self.set_compliance_all(True)

        # turn the fans off for the arm
        self.turn_off_fans()

    def handle_shutdown(self, client=None, userdata=None, message=None):
        self.shutdown()

    def force_stop(self):
        self.state = ActionQueue.STOPPED

        # this should only be done in an emergency
        self.set_right_arm_compliance(True)
        self.set_head_compliance(True)

    def handle_force_stop(self, client=None, userdata=None, message=None):
        self.force_stop()

    def reset(self):
        self.state = ActionQueue.IDLE
        self.action_queue.clear()

    def turn_on_fans(self):
        self.reachy.right_arm.shoulder_fan.on()
        self.reachy.right_arm.elbow_fan.on()
        self.reachy.right_arm.wrist_fan.on()

    def turn_off_fans(self):
        self.reachy.right_arm.shoulder_fan.off()
        self.reachy.right_arm.elbow_fan.off()
        self.reachy.right_arm.wrist_fan.off()

    def set_head_compliance(self, compliance):
        for m in self.reachy.head.motors:
            m.compliant = compliance

    def set_right_arm_compliance(self, compliance):
        for m in self.reachy.right_arm.motors:
            m.compliant = compliance

    def set_compliance_all(self, compliance):
        self.set_head_compliance(compliance)
        self.set_right_arm_compliance(compliance)

    def move_antennas_to_zero(self, client=None, userdata=None, message=None):
        self.set_head_compliance(False)

        for m in self.reachy.head.motors:
            m.goal_position = 0

        self.set_head_compliance(True)

    def move_right_arm_to_zero(self, client=None, userdata=None, message=None):
        self.set_right_arm_compliance(False)

        self.reachy.goto({
            'right_arm.shoulder_pitch': 0,
            'right_arm.shoulder_roll': 90,
            'right_arm.arm_yaw': 0,
            'right_arm.elbow_pitch': 0,
            'right_arm.hand.forearm_yaw': 0,
            'right_arm.hand.wrist_pitch': 0,
            'right_arm.hand.wrist_roll': 0,
            'right_arm.hand.gripper': 0,
        }, duration=3, wait=True)

        self.set_right_arm_compliance(True)

    def move_all_to_zero(self):
        self.move_antennas_to_zero()
        self.move_right_arm_to_zero()

    """
    def make_wave_arm(self):
        def wave_arm():
            self.set_right_arm_compliance(False)

            #Wave Frame 1, bring arm up
            self.reachy.goto({
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
            self.reachy.goto({
                'right_arm.hand.wrist_roll': 40,
                'right_arm.hand.gripper': 0,
            }, duration=0.75, wait=True)

            self.reachy.goto({
                'right_arm.hand.wrist_roll': -40,
                'right_arm.hand.gripper': 0,
            }, duration=0.75, wait=True)

            self.reachy.goto({
                'right_arm.hand.wrist_roll': 40,
                'right_arm.hand.gripper': 0,
            }, duration=0.75, wait=True)

            self.reachy.goto({
                'right_arm.hand.wrist_roll': -40,
                'right_arm.hand.gripper': 0,
            }, duration=0.75, wait=True)

            time.sleep(2) #wait 2 seconds

            #Wave Frame 3, return to home position
            self.reachy.goto({
                'right_arm.shoulder_pitch': 0,
                'right_arm.shoulder_roll': 0,
                'right_arm.arm_yaw': 0,
                'right_arm.elbow_pitch': 0,
                'right_arm.hand.forearm_yaw': 0,
                'right_arm.hand.wrist_pitch': 0,
                'right_arm.hand.wrist_roll': 0,
                'right_arm.hand.gripper': 0,
            }, duration=2, wait=True)


            self.move_right_arm_to_zero()
            self.set_right_arm_compliance(True)

        return wave_arm
    """

    def make_wave_arm(self):
        def wave_arm():
            self.set_right_arm_compliance(False)

            self.move_right_arm_to_zero()

            # Moving arm and hand into position
            pos_RA = {
                'right_arm.shoulder_pitch': 0, #-20
                #'right_arm.shoulder_roll': 0, # -10
                'right_arm.arm_yaw': -60, # -10
                'right_arm.elbow_pitch': -90, # -120
                'right_arm.hand.forearm_yaw': -60, # 0
                'right_arm.hand.wrist_pitch': 0, # 0
                'right_arm.hand.wrist_roll': -30, # 0
                'right_arm.hand.gripper': 0, # 0
            }

            # Loop Hand Wave
            pos_RB = {
                'right_arm.shoulder_pitch': 0,
                #'right_arm.shoulder_roll': 0,
                'right_arm.arm_yaw': -60,
                'right_arm.elbow_pitch': -90,
                'right_arm.hand.forearm_yaw': -60,
                'right_arm.hand.wrist_pitch': 0,
                'right_arm.hand.wrist_roll': 30, # 40
                'right_arm.hand.gripper': 0,
            }

            pos_RC = {
                'right_arm.shoulder_pitch': 0,
                #'right_arm.shoulder_roll': 0,
                'right_arm.arm_yaw': -60,
                'right_arm.elbow_pitch': -90,
                'right_arm.hand.forearm_yaw': -60,
                'right_arm.hand.wrist_pitch': 0,
                'right_arm.hand.wrist_roll': -30, # -40
                'right_arm.hand.gripper': 0,
            }

            # rehome start and finish, with loop
            self.reachy.head.left_antenna.goto(0, duration = 2, wait = True)
            self.reachy.head.right_antenna.goto(0, duration = 2, wait = True)
            self.reachy.goto(goal_positions = zero_posR, duration=2, wait=True)
            time.sleep(2)

            self.reachy.goto(goal_positions = pos_RA, duration = 2.5, wait = True)
            #reachy.head.left_antenna.goto(-45, duration = 2, wait = False) # depends on actual calibration - may need opp sign
            for m in range(3):
                self.reachy.goto(goal_positions = pos_RB, duration = 1, wait = True)
                self.reachy.goto(goal_positions = pos_RC, duration = 1, wait = True)
                time.sleep(1)

            #reachy.head.left_antenna.goto(0, duration = 2, wait = False)
            self.reachy.goto(goal_positions = zero_posR, duration = 2, wait=True)
            time.sleep(2)

    def handle_wave_arm(self, client=None, userdata=None, message=None):
        self.action_queue.add(self.make_wave_arm())

    """
    def make_wiggle_antennas(self):
        def wiggle_antennas():
            print("###adding wiggle to queue")

            self.set_head_compliance(False)

            print("###wiggle - 1")

            for m in self.reachy.head.motors:
                m.goal_position = 0

            print("###wiggle - 2")

            for m in self.reachy.head.motors:
                m.goal_position = 45

            print("###wiggle - 3")

            for m in self.reachy.head.motors:
                m.goal_position = 0

            print("###wiggle - 4")

            t = np.linspace(0, 10, 1000)
            pos = 30 * np.sin(2 * np.pi * 0.5 * t)


            print("###wiggle - 5")

            for p in pos:
                for m in self.reachy.head.motors:
                    m.goal_position = p
                time.sleep(0.01)

            print("###wiggle - 6")

            self.set_head_compliance(False)


        return wiggle_antennas
    """

    def make_wiggle_antennas(self):
        def wiggle_antennas():
            self.set_head_compliance(False)

            for m in self.reachy.head.motors:
                m.goal_position = 45
            time.sleep(0.1)

            for m in self.reachy.head.motors:
                m.goal_position = 0
            time.sleep(0.1)

            for m in self.reachy.head.motors:
                m.goal_position = -45
            time.sleep(0.1)

            for m in self.reachy.head.motors:
                m.goal_position = 0
            time.sleep(0.1)

            for m in self.reachy.head.motors:
                m.goal_position = 45
            time.sleep(0.1)

            for m in self.reachy.head.motors:
                m.goal_position = 0
            time.sleep(0.1)

            for m in self.reachy.head.motors:
                m.goal_position = -45
            time.sleep(0.1)

            self.set_head_compliance(False)

        return wiggle_antennas

    def handle_wiggle_antennas(self, client=None, userdata=None, message=None):
        self.action_queue.add(self.make_wiggle_antennas())

def main():
    node = Body("body")
    node.run()

if __name__ == "__main__":
    # execute only if run as a script
    main()
