import pathlib
import os.path
from .pyimagesearch.centroidtracker_mine import CentroidTracker
from imutils.video import VideoStream
import numpy as np
import cv2
import argparse
import imutils
import time
from ...model.frames import FrameData, FrameDataCollection

class FacialRecognition(object):
    def __init__(self, prototxt="deploy.prototxt", model="res10_300x300_ssd_iter_140000.caffemodel", confidence=0.5):
        self.ct = CentroidTracker()
        self.H = None
        self.W = None

        # TODO: maybe move these files to a better location
        self.curr_dir = pathlib.Path(__file__).parent.absolute()
        print(self.curr_dir)
        self.prototxt = os.path.join(self.curr_dir, prototxt)
        self.model = os.path.join(self.curr_dir, model)

        self.confidence = confidence

        print("[INFO] loading model...")
        self.net = cv2.dnn.readNetFromCaffe(self.prototxt, self.model)

        self.frame_data_collection = FrameDataCollection()

    def add_frame_data(self, frame_data):
        self.frame_data_collection.add(frame_data)

    def detect_faces(self, frame):
        rects = []
        objects = {}

        try:
            frame = imutils.resize(frame, width=400)

            if self.W is None or self.H is None:
                self.H, self.W = frame.shape[:2]

            blob = cv2.dnn.blobFromImage(frame, 1.0, (self.W, self.H), (104.0, 177.0, 123.0))
            self.net.setInput(blob)
            detections = self.net.forward()
            rects = []

            for i in range(0, detections.shape[2]):
                if detections[0, 0, i, 2] > self.confidence:
                    box = detections[0, 0, i, 3:7] * np.array([self.W, self.H, self.W, self.H])
                    rects.append(box.astype("int"))

                    (startX, startY, endX, endY) = box.astype("int")
                    cv2.rectangle(frame, (startX, startY), (endX, endY), (0, 255, 0), 2)

            objects = self.ct.update(rects)

            for (objectID, centroid) in objects.items():
                text = "ID {}".format(objectID)
                cv2.putText(frame, text, (centroid[0] - 10, centroid[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
                cv2.circle(frame, (centroid[0], centroid[1]), 4, (0, 255, 0), -1)

            print("###type recs: ", type(recs))
            print("###type objects: ", type(objects))

        except:
            pass

        frame_data = FrameData(rects, objects)

        return frame, frame_data

