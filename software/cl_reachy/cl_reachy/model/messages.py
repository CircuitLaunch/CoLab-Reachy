import json
from collections import namedtuple
from json import JSONEncoder
from .common import DataModelBase

class LogMessage(DataModelBase):
    def __init__(self, msg):
        self.msg = msg

    @staticmethod
    def decoder(msgDict):
        return namedtuple(LogMessage.__name__, msgDict.keys())(*msgDict.values())

    @staticmethod
    def from_json(msgJson):
        return json.loads(msgJson, object_hook=LogMessage.decoder)

class SayMessage(DataModelBase):
    def __init__(self, msg):
        self.msg = msg

    @staticmethod
    def decoder(msgDict):
        return namedtuple(SayMessage.__name__, msgDict.keys())(*msgDict.values())

    @staticmethod
    def from_json(msgJson):
        return json.loads(msgJson, object_hook=SayMessage.decoder)

class HeardMessage(DataModelBase):
    def __init__(self, corrected_time=None, transcript=""):
        self.corrected_time = corrected_time
        self.transcript = transcript

    @staticmethod
    def decoder(msgDict):
        return namedtuple(HeardMessage__name__, msgDict.keys())(*msgDict.values())

    @staticmethod
    def from_json(msgJson):
        return json.loads(msgJson, object_hook=HeardMessage.decoder)

class AudioInputStateMessage(DataModelBase):
    def __init__(self, is_busy, listener):
        self.is_busy = is_busy
        self.listener = listener

    @staticmethod
    def decoder(msgDict):
        return namedtuple(AudioInputStateMessage.__name__, msgDict.keys())(*msgDict.values())

    @staticmethod
    def from_json(msgJson):
        return json.loads(msgJson, object_hook=AudioInputStateMessage.decoder)

class ThresholdStartMessage(DataModelBase):
    def __init__(self, threshold, num, force=False):
        self.threshold = threshold
        self.num = num
        self.force = False

    @staticmethod
    def decoder(msgDict):
        return namedtuple(ThresholdStartMessage.__name__, msgDict.keys())(*msgDict.values())

    @staticmethod
    def from_json(msgJson):
        return json.loads(msgJson, object_hook=ThresholdStartMessage.decoder)

class ThresholdResponseMessage(DataModelBase):
    def __init__(self, running, threshold, num):
        self.running = running
        self.threshold = threshold
        self.num = num

    @staticmethod
    def decoder(msgDict):
        return namedtuple(ThresholdResponseMessage.__name__, msgDict.keys())(*msgDict.values())

    @staticmethod
    def from_json(msgJson):
        return json.loads(msgJson, object_hook=ThresholdResponseMessage.decoder)

class WakeWordStartMessage(DataModelBase):
    def __init__(self, sensitivity=0.5, force=False):
        self.sensitivity = sensitivity
        self.force = False

    @staticmethod
    def decoder(msgDict):
        return namedtuple(WakeWordStartMessage.__name__, msgDict.keys())(*msgDict.values())

    @staticmethod
    def from_json(msgJson):
        return json.loads(msgJson, object_hook=WakeWordStartMessage.decoder)






