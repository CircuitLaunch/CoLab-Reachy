from collections import OrderedDict
from reachy import parts


def patch_head(head_cls):
    # if it's 'armv7l', assume that it's the raspberry pi 4 on reachy
    head_cls.dxl_motors = OrderedDict([
        ('left_antenna', {
            'id': 30, 'offset': 26.0, 'orientation': 'direct',
            'angle-limits': [-150, 150],
        }),
        ('right_antenna', {
            'id': 31, 'offset': 90.0, 'orientation': 'direct',
            'angle-limits': [-150, 150],
        }),
    ])

    def __init__(self, io, default_camera='right'):
        """Create new Head part."""
        parts.part.ReachyPart.__init__(self, name='head', io=io)

        #self.neck = self.create_orbita_actuator('neck', Head.orbita_config)
        self.attach_dxl_motors(parts.Head.dxl_motors)
        #self.camera = self.io.find_dual_camera(default_camera)

    head_cls.__init__ = __init__

    return head_cls


def patch_right_arm(arm_cls):
    arm_cls.dxl_motors = OrderedDict([
        ('shoulder_pitch', {
            'id': 10, 'offset': 0.0, 'orientation': 'indirect',
            'angle-limits': [-180, 60],
            'link-translation': [0, -0.19, 0], 'link-rotation': [0, 1, 0],
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

    return arm_cls

def patch_force_gripper(forceGripper):
    def __init__(self, root, io):
        """Create a new Force Gripper Hand."""
        parts.hand.Hand.__init__(self, root=root, io=io)

        dxl_motors = OrderedDict({
            name: dict(conf)
            for name, conf in self.dxl_motors.items()
        })

        self.attach_dxl_motors(dxl_motors)

        """
        self._load_sensor = self.io.find_module('force_gripper')
        self._load_sensor.offset = 4
        self._load_sensor.scale = 10000
        """
        
    forceGripper.__init__ = __init__
    
    return forceGripper
