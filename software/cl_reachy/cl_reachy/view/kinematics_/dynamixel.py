import pathlib
import numpy as np
from collections import OrderedDict
import time

from scipy.spatial.transform import Rotation as R
from ...ws import WsMotor

def rot(axis, deg):
    """Compute 3D rotation matrix given euler rotation."""
    return R.from_euler(axis, np.deg2rad(deg)).as_matrix()

class DynamixelMotor(object):
    """DynamixelMotor abstraction class.
    Args:
        root_part (str): name of the part where the motor is attached to (eg 'right_arm.hand')
        name (str): name of the motor (eg. 'shoulder_pitch')
        luos_motor (:py:class:`pyluos.modules.DxlMotor`): pyluos motor
        config (dict): extra motor config (must include 'offset' and 'orientation' fields)
    Wrap the pyluos motor object to simplify and make the API homogeneous.
    """

    def __init__(self, root_part, name, luos_motor, config):
        """Create a DynamixelMotor given its pyluos equivalent."""
        self._root_part = root_part
        self._name = name

        self._motor = luos_motor

        self._offset = config['offset']
        self._direct = config['orientation'] == 'direct'

        self._timer = None
        self._use_static_fix = False

    def __repr__(self):
        """Motor representation."""
        mode = 'compliant' if self.compliant else 'stiff'
        return f'<DxlMotor "{self.name}" pos="{self.present_position}" mode="{mode}">'

    @property
    def name(self):
        """Fullname of the motor (eg. right_arm.hand.gripper)."""
        return f'{self._root_part.name}.{self._name}'

    # Position
    @property
    def present_position(self):
        """Present position (in degrees) of the motor."""
        return self._as_local_pos(self._motor.rot_position)

    @property
    def goal_position(self):
        """Get current goal position (in degrees) of the motor."""
        return self._as_local_pos(self._motor.target_rot_position)

    @goal_position.setter
    def goal_position(self, value):
        if not self.compliant:
            self._motor.target_rot_position = self._to_motor_pos(value)

            if self._use_static_fix:
                self._schedule_static_error_fix(delay=1)

    @property
    def offset(self):
        """Get motor real zero (in degrees)."""
        return self._offset

    def is_direct(self):
        """Check whether the motor is direct or not."""
        return self._direct

    def _as_local_pos(self, pos):
        return (pos if self.is_direct() else -pos) - self.offset

    def _to_motor_pos(self, pos):
        return (pos + self.offset) * (1 if self.is_direct() else -1)

    # Speed
    @property
    def moving_speed(self):
        """Get the maximum speed (in degree per second) of the motor."""
        return self._motor.target_rot_speed

    @moving_speed.setter
    def moving_speed(self, value):
        self._motor.target_rot_speed = value

    # Compliancy
    @property
    def compliant(self):
        """Check whether or not the motor is compliant."""
        return self._motor.compliant

    @compliant.setter
    def compliant(self, value):
        self._motor.compliant = value

    @property
    def torque_limit(self):
        """Check the maximum torque allowed (in %) of the motor."""
        return self._motor.power_ratio_limit

    @torque_limit.setter
    def torque_limit(self, value):
        self._motor.power_ratio_limit = value

    # Temperature
    @property
    def temperature(self):
        """Check the current motor temp. (in °C)."""
        return self._motor.temperature

    def goto(self,
             goal_position, duration,
             starting_point='present_position',
             wait=False, interpolation_mode='linear'):
        """Set trajectory goal for the motor.
        Args:
            goal_position (float): target position (in degrees)
            duration (float): duration of the movement (in seconds)
            starting_point (str): register used to determine the starting point (eg. 'goal_position' can also be used in some specific case)
            wait (bool): whether or not to wait for the end of the motion
            interpolation_mode (str): interpolation technique used for computing the trajectory ('linear', 'minjerk')
        Returns:
            reachy.trajectory.TrajectoryPlayer: trajectory player that can be used to monitor the trajectory, stop it, etc
        """
        if interpolation_mode not in interpolation_modes.keys():
            available = tuple(interpolation_modes.keys())
            raise ValueError(f'interpolation_mode should be one of {available}')

        traj_player = interpolation_modes[interpolation_mode](getattr(self, starting_point), goal_position, duration)
        traj_player.start(self)

        if wait:
            traj_player.wait()

        return traj_player

    def use_static_error_fix(self, activate):
        """Trigger the static error fix.
        Args:
            activate (bool): whether to activate/deactivate the static error issue fix
        If activated, the static error fix will check the reach position a fixed delay after the send of a new goal position.
        The static error may result in the motor's load increasing, and yet not managing to move.
        To prevent this behavior we automatically adjust the target goal position to reduce this error.
        """
        self._use_static_fix = activate

    # Patch dynamixel controller issue when the motor forces
    # while not managing to reach the goal position
    def _schedule_static_error_fix(self, delay):
        if self._timer is not None:
            self._timer.cancel()
        self._timer = Timer(delay, self._fix_static_error)
        self._timer.start()

    def _fix_static_error(self, threshold=2):
        error = (self.present_position - self.goal_position)

        if abs(error) > threshold:
            pos = self.goal_position + error / 2
            logger.info('Fix static error controller', extra={
                'goal_position': self.goal_position,
                'present_position': self.present_position,
                'fixed_goal_position': pos,
            })

            self._motor.target_rot_position = self._to_motor_pos(pos)
            self._timer = None

def find_dxl(io, part_name, dxl_name, dxl_config):
    """Get a specific dynamixel motor from the IO.
    Only goal position is used atm.
    """
    pos = dxl_config['offset'] * (-1 if dxl_config['orientation'] == 'indirect' else 1)
    m = WsMotor(name=f'{part_name}.{dxl_name}', initial_position=pos)

    io.motors.append(m)
    io.ws.motors[m.name] = m
    return m

def attach_dxl_motors(io, part_name, dxl_motors):
    """Attach given dynamixel motors to a part.
    Args:
        dxl_motors (dict): motors config, the config must at least include an id for each motor (see attach_kinematic_chain for extra parameters)
    """
    motors_dict = {}



    class Root(object):
        def __init__(self, name):
            self.name = name

    root = Root(part_name)

    for motor_name, config in dxl_motors.items():
        dxl = find_dxl(io, part_name, motor_name, config)
        m = DynamixelMotor(root, motor_name, dxl, config)
        motors_dict[motor_name] = m

    return motors_dict

