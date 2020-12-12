import sqlite3
import time

ALERT_NOT_SENT: int = 0  # int used as a bool to mean that an alert and new and has not been sent over the wire yet.


class LocalDB(object):
    """
    Minimalist SQLite wrapper to ensure the connection is closed upon program termination.
    """

    def __init__(self):
        self.conn = sqlite3.connect("alert.db")

    def __del__(self):
        self.conn.close()


def persist_alert(connection, alert, deployed_on):
    """
    Write an alert to local SQLite storage.
    """
    start_time = time.perf_counter()
    cursor = connection.cursor()
    vals = (
        ALERT_NOT_SENT,
        alert.event_time,
        alert.created_by.type,
        alert.created_by.guid,
        deployed_on,
        alert.location.longitude,
        alert.location.latitude,
        alert.face_detection_model.name,
        alert.face_detection_model.guid,
        alert.face_detection_model.threshold,
        alert.mask_classifier_model.name,
        alert.mask_classifier_model.guid,
        alert.mask_classifier_model.threshold,
        alert.probability,
        alert.image.format,
        alert.image.size.width,
        alert.image.size.height,
        alert.image.data,
    )
    cursor.execute(
        """INSERT INTO 
            alert (sent, created_at, device_type, device_id, device_deployed_on, longitude, latitude, face_model_name, face_model_guid, face_model_threshold, mask_model_name, mask_model_guid, mask_model_threshold, probability, image_format, image_width, image_height, image_data) 
            VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?) """,
        vals,
    )
    connection.commit()
    print(f"Alert persisted on local storage (transaction took {(time.perf_counter() - start_time) * 1000} ms)\n")
