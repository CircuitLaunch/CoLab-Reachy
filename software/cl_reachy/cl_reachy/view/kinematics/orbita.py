import pathlib
import numpy as np
from collections import OrderedDict
import time

class Orbita(object):
    def __init__(self, io):
        self.io = io

        curr_dir = pathlib.Path(__file__).parent.absolute()
        self.hardware_zero = np.load('{}/orbita_head_hardware_zero.npy'.format(curr_dir))

        self.disks_motor = io.find_orbita_disks()
        self.disk_bottom, self.disk_middle, self.disk_top = self.disks_motor

        for d in self.disks_motor:
            d.compliant = False

        self.setup_orbita_disks(self.disks_motor, self.hardware_zero)

    def setup_orbita_disks(self, disks, hardware_zero):
        """Configure each of the three disks.
        .. note:: automatically called at instantiation.
        """
        for disk in disks:
            disk.setup()

        def _find_zero(disk, z):
            A = 360 / (52 / 24)
            p = disk.rot_position

            zeros = [z, -(A - z), A + z]
            distances = [abs(p - z) for z in zeros]
            best = np.argmin(distances)

            return zeros[best]

        time.sleep(0.25)

        for d, z in zip(disks, hardware_zero):
            d.offset = _find_zero(d, z) + 60

    def move_motors(self, bottom_rot_position, middle_rot_position, top_rot_position):
        self.disk_bottom.target_rot_position = bottom_rot_position
        self.disk_middle.target_rot_position = middle_rot_position
        self.disk_top.target_rot_position = top_rot_position

    def sample_motion(self):
        self.move_motors(-180, -180, -180)
        time.sleep(10)
        self.move_motors(180, 180, 180)


