import json
from json import JSONEncoder

class DataModelEncoder(JSONEncoder):
    def default(self, o):
        return o.__dict__

class DataModelBase(object):
    def __init__(self):
        pass

    def to_json(self):
        return json.dumps(self, indent=4, cls=DataModelEncoder)

    def __str__(self):
        return self.to_json()


    def __repr__(self):
        return self.to_json()
