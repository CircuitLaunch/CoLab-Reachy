import datetime
import io
import os
import sys

import yaml

from PIL import Image
import alert_pb2

cur_dir: str = sys.path[0]
CONFIG_PATH: str = os.path.join(cur_dir, "config.yaml")
with open(CONFIG_PATH, "r") as f:
    operational_config = yaml.safe_load(f)
if "device" not in operational_config:
    raise Exception("Failed to load configuration")

DATE_FORMAT: str = "%Y-%m-%d %H:%M:%S.%f"


face_model = operational_config["models"]["face_detection"]["model"]
face_threshold = operational_config["models"]["face_detection"]["threshold"]
mask_model = operational_config["models"]["mask_classifier"]["model"]
mask_labels = operational_config["models"]["mask_classifier"]["labels"]
mask_threshold = operational_config["models"]["mask_classifier"]["threshold"]
mask_model_guid: str = operational_config["models"]["mask_classifier"]["guid"]
face_model_guid: str = operational_config["models"]["face_detection"]["guid"]
device: dict = operational_config["device"]
deployment: dict = operational_config["deployment"]


def image_to_byte_array(image: Image, fmt: str = "jpeg"):
    """

    Returns:

    """
    img_byte_arr = io.BytesIO()
    image.save(img_byte_arr, format=fmt)
    img_byte_arr = img_byte_arr.getvalue()
    return img_byte_arr


def create_alert(img: Image, proba: float) -> alert_pb2.Alert:
    """
    create_alert is an Alert Factory creating an alert from an image.

    Returns: alert as per the protocol buffer definition.

    """
    alert = alert_pb2.Alert()

    alert.event_time = datetime.datetime.utcnow().strftime(DATE_FORMAT)

    alert.created_by.type = device["type"]
    alert.created_by.guid = device["guid"]
    alert.created_by.enrolled_on = device["enrolled_on"]

    alert.location.latitude = deployment["latitude"]
    alert.location.longitude = deployment["longitude"]

    alert.face_detection_model.name = face_model
    alert.face_detection_model.guid = face_model_guid
    alert.face_detection_model.threshold = face_threshold

    alert.mask_classifier_model.name = mask_model
    alert.mask_classifier_model.guid = mask_model_guid
    alert.mask_classifier_model.threshold = mask_threshold

    alert.probability = proba

    alert.image.format = "jpeg"
    alert.image.size.width = img.size[0]
    alert.image.size.height = img.size[1]
    alert.image.data = image_to_byte_array(img)

    return alert
