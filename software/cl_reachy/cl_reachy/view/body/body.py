import os
from ...node import NodeBase
class Body(NodeBase):

from reachy import Reachy, parts
from ...node import NodeBase

REACHY_SIM = os.environ['REACHY_SIM']

if REACHY_SIM == 0:
    # monkey patch Reachy
    parts.arm.RightArm.dxl_motors = OrderedDict([
        ('shoulder_pitch', {
            # OK
            'id': 10, 'offset': -90.0, 'orientation': 'indirect',
            'angle-limits': [-180, 60],
            'link-translation': [0, -0.19, 0], 'link-rotation': [0, 1, 0],
        }),
        ('shoulder_roll', {
            # TODO: still need to fix offset
            'id': 11, 'offset': 0, 'orientation': 'indirect',
            'angle-limits': [-180, 10],
            'link-translation': [0, 0, 0], 'link-rotation': [1, 0, 0],
        }),
        ('arm_yaw', {
            # OK
            'id': 12, 'offset': 5.0, 'orientation': 'indirect',
            'angle-limits': [-90, 90],
            'link-translation': [0, 0, 0], 'link-rotation': [0, 0, 1],
        }),
        ('elbow_pitch', {
            # OK
            'id': 13, 'offset': 45.0, 'orientation': 'indirect',
            'angle-limits': [-125, 0],
            'link-translation': [0, 0, -0.28], 'link-rotation': [0, 1, 0],
        }),
    ])

    parts.hand.RightForceGripper.dxl_motors = OrderedDict([
        ('forearm_yaw', {
            'id': 14, 'offset': 0.0, 'orientation': 'indirect',
            'angle-limits': [-100, 100],
            'link-translation': [0, 0, 0], 'link-rotation': [0, 0, 1],
        }),
        ('wrist_pitch', {
            'id': 15, 'offset': -90.0, 'orientation': 'indirect',
            'angle-limits': [-45, 45],
            'link-translation': [0, 0, -0.25], 'link-rotation': [0, 1, 0],
        }),
        ('wrist_roll', {
            'id': 16, 'offset': -92.0, 'orientation': 'direct',
            'angle-limits': [-45, 45],
            'link-translation': [0, 0, -0.0325], 'link-rotation': [1, 0, 0],
        }),
        ('gripper', {
            'id': 17, 'offset': -4.0, 'orientation': 'direct',
            'angle-limits': [-69, 20],
            'link-translation': [0, -0.01, -0.075], 'link-rotation': [0, 0, 0],
        }),
    ])

    parts.head.Head.dxl_motors = OrderedDict([
        ('left_antenna', {
            'id': 30, 'offset': 26.0, 'orientation': 'direct',
            'angle-limits': [-150, 150],
        }),
        ('right_antenna', {
            'id': 31, 'offset': 90.0, 'orientation': 'direct',
            'angle-limits': [-150, 150],
        }),
    ])

    def head_init(self, io, default_camera='right'):
        """Create new Head part."""
        ReachyPart.__init__(self, name='head', io=io)

        #self.neck = self.create_orbita_actuator('neck', Head.orbita_config)
        self.attach_dxl_motors(Head.dxl_motors)
        #self.camera = self.io.find_dual_camera(default_camera)

    parts.head.Head.__init__ = head_init

class Body(NodeBase):
    def __init__(self, node_name="speechsynthesis", host="127.0.0.1", port=1883,
                    username=None, password=None, subscribe_dict={}, run_sleep=0.1):
        super().__init__(node_name, host, port, username, password, subscribe_dict, run_sleep)

        self.io = "ws"
        if REACHY_SIM == 0:
            self.io = '/dev/ttyUSB*'

        self.reachy = Reachy(head=parts.Head(io=self.io),
                                right_arm=parts.RightArm(io='ws', hand='force_gripper'),
        )

        self.left_antenna = self.reachy.head.motors[0]
        self.right_antenna = self.reachy.head.motors[1]

        self.turn_on_fans()
        self.set_compliance_all(False)
        self.move_all_to_zero()

    def set_compliance_head(self, compliance):
        for m in self.reachy.head.motors:
            m.compliant = compliance

    def set_compliance_right_arm(self, compliance):
        for m in self.reachy.right_arm.motors:
            m.compliant = compliance

    def set_compliance_all(self, compliance):
        self.set_compliance_head(compliance)
        self.set_compliance_hand(compliance)

    def turn_on_fans(self):
        self.reachy.right_arm.shoulder_fan.on()
        self.reachy.right_arm.elbow_fan.on()
        self.reachy.right_arm.wrist_fan.on()

    def turn_off_fans(self):
        self.reachy.right_arm.shoulder_fan.off()
        self.reachy.right_arm.elbow_fan.off()
        self.reachy.right_arm.wrist_fan.off()

    def is_angle_within_limits(self, angle, limits):
        return (angle >= limits[0] and angle <= limits[1])

    def move_motor(self, motor, goal_position, limits):
        if not self.is_angle_within_limits(goal_position, limits):
            return False

        self.goal_position = goal_position
        return True

    def move_left_antenna(self, goal_position):
        limits = parts.head.Head.dxl_motors['left_antenna']['angle-limits']
        return self.move_motor(self.left_antenna, goal_position, limits)

    def move_right_antenna(self, goal_position):
        limits = parts.head.Head.dxl_motors['right_antenna']['angle-limits']
        return self.move_motor(self.right_antenna, goal_position, limits)

    def move_antennas_to_zero(self):
        # TODO: make a trajectory for this
        self.move_left_antenna(0)
        self.move_right_antenna(0)

    def move_arm_to_zero(self):
        self.reachy.goto({
            'right_arm.shoulder_pitch': 0,
            'right_arm.shoulder_roll': 0,
            'right_arm.arm_yaw': 0,
            'right_arm.elbow_pitch': 0,
            'right_arm.hand.forearm_yaw': 0,
            'right_arm.hand.wrist_pitch': 0,
            'right_arm.hand.wrist_roll': 0,
            'right_arm.hand.gripper': 0,
        }, duration=3, wait=True)

    def move_all_to_zero(self):
        self.move_antennas_to_zero()
        self.move_arm_to_zero()

    def force_stop(self):
        self.set_compliance_right_arm(True)
        self.set_compliance_head(True)

    def final(self):
        self.set_compliance_all(False)

        self.move_all_to_zero()

        self.set_compliance_all(True)

        self.turn_off_fans()
