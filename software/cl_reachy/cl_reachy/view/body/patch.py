

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

        head_cls.__init__(self, io, default_camera='right'):
            """Create new Head part."""
            ReachyPart.__init__(self, name='head', io=io)

            #self.neck = self.create_orbita_actuator('neck', Head.orbita_config)
            self.attach_dxl_motors(Head.dxl_motors)
            #self.camera = self.io.find_dual_camera(default_camera)

    return head_cls