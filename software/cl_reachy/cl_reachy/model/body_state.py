import json
from collections import namedtuple
from json import JSONEncoder
from .common import DataModelBase

class DynamixelState(DataModelBase):
    def __init__(self, name, present_position, compliant):
        # TODO - some properties should stay local to the view but other
        #        properties should be in the model with the controller
        self.name = name
        self.present_position = present_position
        self.compliant = compliant

    @staticmethod
    def decoder(msgDict):
        return namedtuple(LogMessage.__name__, msgDict.keys())(*msgDict.values())

    @staticmethod
    def from_json(msgJson):
        return json.loads(msgJson, object_hook=HeadState.decoder)

class HeadState(DataModelBase):
    def __init__(self, left_antenna_state, right_antenna_state):
        self.left_antenna_state = left_antenna_state
        self.right_antenna_state = right_antenna_state

    @staticmethod
    def decoder(msgDict):
        return namedtuple(HeadState.__name__, msgDict.keys())(*msgDict.values())

    @staticmethod
    def from_json(msgJson):
        return json.loads(msgJson, object_hook=HeadState.decoder)

class OrbitaState(DataModelBase):
    def __init__(self):
        # TODO
        pass

    @staticmethod
    def decoder(msgDict):
        return namedtuple(OrbitaState.__name__, msgDict.keys())(*msgDict.values())

    @staticmethod
    def from_json(msgJson):
        return json.loads(msgJson, object_hook=OrbitaState.decoder)

class RightArmState(DataModelBase):
    def __init__(self, shoulder_pitch_state, shoulder_roll_state, arm_yaw_state, elbow_pitch_state):
        # TODO
        self.shoulder_pitch_state = shoulder_pitch_state
        self.shoulder_roll_state = shoulder_roll_state
        self.arm_yaw_state = arm_yaw_state
        self.elbow_pitch_state = elbow_pitch_state

    @staticmethod
    def decoder(msgDict):
        return namedtuple(RightArmState.__name__, msgDict.keys())(*msgDict.values())

    @staticmethod
    def from_json(msgJson):
        return json.loads(msgJson, object_hook=RightArmState.decoder)