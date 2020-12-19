import os
from collections import OrderedDict
from reachy.parts.part import ReachyPart
from reachy.parts.arm import RightArm
from reachy.parts.hand import RightForceGripper
from reachy.parts.head import Head

REACHY_SIM = os.environ['REACHY_SIM'] if 'REACHY_SIM' in os.environ.keys() else 0

if REACHY_SIM == 0:
    # monkey patch Reachy
    RightArm.dxl_motors = OrderedDict([
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

    RightForceGripper.dxl_motors = OrderedDict([
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

    Head.dxl_motors = OrderedDict([
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

    Head.__init__ = head_init
