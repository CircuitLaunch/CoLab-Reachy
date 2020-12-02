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






