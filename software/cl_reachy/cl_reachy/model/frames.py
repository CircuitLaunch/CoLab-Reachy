import json
from collections import namedtuple
from json import JSONEncoder
from copy import deepcopy
from .common import DataModelBase, DataModelEncoder
import numpy as np

COMING = 1
GOING = -1
STANDING_STILL = 0

class FrameData(DataModelBase):
    def __init__(self, rects, centroid_objs):
        self.rects = rects
        self.centroid_objs = centroid_objs

        self.rect_dict = self.make_rect_dict(self.rects)
        self.area_dict = self.make_area_dict(self.rect_dict)

    def get_ids(self):
        return self.centroid_objs.keys()

    def is_centroid_in_rect(self, centroid, rect):
        centroidX, centroidY = centroid
        (startX, startY, endX, endY) = rect

        return (centroidX >= startX and centroidX <= endX and centroidY >= startY and centroidY <= endY)

    def get_area(self, rect):
        (startX, startY, endX, endY) = rect

        return (endX - startX) * (endY - startY)

    def make_rect_dict(self, rects):
        rect_dict = {}

        for (objectID, centroid) in self.centroid_objs.items():
            for rect in rects:
                if self.is_centroid_in_rect(centroid, rect):
                    rect_dict[objectID] = rect
                    break

        return rect_dict

    def make_area_dict(self, rect_dict):
        area_dict = {}

        for (objectID, rect) in self.rect_dict.items():
            area_dict[objectID] = self.get_area(rect)

    def get_area_by_id(self, id):
        if id in self.area_dict.keys():
            return self.area_dict[id]

        return None

    @staticmethod
    def decoder(msgDict):
        return namedtuple(FrameData.__name__, msgDict.keys())(*msgDict.values())

    @staticmethod
    def from_json(msgJson):
        obj = json.loads(msgJson, object_hook=FrameData.decoder)
        obj.rects = [np.asarray(rect, dtype=np.in32) for rect in obj.rects]
        obj.centroid_objs = {key: np.asarray(val, dtype=np.int32) for key, val in obj.centroid_objs.items()}

        return obj

    def to_json(self):
        _self = deepcopy(self)
        _self.rects = [rect.tolist() for rect in self.rects]
        _self.centroid_objs = {key: val.tolist() for key, val in _self.centroid_objs.items()}

        return json.dumps(_self, indent=4, cls=DataModelEncoder)

    def __str__(self):
        return "rects: {}, centriods: {}".format(self.rects, self.centroid_objs)

class FrameDataCollection(object):
    def __init__(self, collection=[], max_size=10):
        self.collection = collection
        self.max_size = max_size

    def len(self):
        return len(self.collection)

    def add(self, frame_data):
        self.collection.append(frame_data)

        if self.len() > self.max_size:
            start_idx = self.len - self.max_size
            self.collection = self.collection[start_idx:]

    def get_last_ids(self):
        if self.collection is None or self.len() == 0:
            return []

        return self.collection[-1].get_ids()

    def is_coming_or_going(self, id, threshold=1.0, num_of_frames=2):
        if num_of_frames > self.len():
            num_of_frames = self.len()

        if num_of_frames == 0:
            return STANDING_STILL

        areas = [self.collection[i].get_area_by_id(id) for i in range(self.len()-num_of_frames, self.len(), -1)]

        area_diffs = [areas[i+1] - areas[i] for i in range(0, len(areas)-1)]

        coming_cnt = 0
        going_cnt = 0
        standing_still_cnt = 0

        for area_diff in area_diffs:
            if abs(area_diff) < threshold:
                standing_still_cnt += 1
            elif area_diff <= -threshold:
                going_cnt += 1
            else:
                coming_cnt += 1

        if standing_still_cnt >= coming_cnt and standing_still_cnt >= going_cnt:
            return STANDING_STILL

        if coming_cnt > going_cnt:
            return COMING

        return GOING


