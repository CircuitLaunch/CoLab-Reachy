import cv2
import threading
import time
from datetime import datetime
from ...node import NodeBase
from ...view.cv.facialrecogn import FacialRecognition
from ...model.messages import SayMessage

SOMEONE_THERE = 1
NO_ONE_THERE = 0

class CameraController(NodeBase):
    def __init__(self, node_name="camera", host="127.0.0.1", port=1883,
                    username=None, password=None, subscribe_dict={}, run_sleep=0.1,
                    show_frames=1):
        super().__init__(node_name, host, port, username, password, subscribe_dict, run_sleep)
        self.show_frames = show_frames

        self.init()

        self.vid = cv2.VideoCapture(0)

        self.add_subscribe('+/facialrecognition/init', self.handle_facial_recognition_init)
        self.add_subscribe('+/facialrecognition/start', self.handle_facial_recognition_start)
        self.add_subscribe('+/facialrecognition/stop', self.handle_facial_recognition_stop)

        # TODO: don't use default params
        self.fr = FacialRecognition(confidence=0.85)

    def init(self):
        self.state = NO_ONE_THERE

        self.last_time_someone_seen = None
        self.last_time_someone_seen_threshold = 60
        self.last_time_no_one_seen_threshold = 60
        self.start_time = datetime.now()

        self.capture_frames = False

    def run(self):
        self.run_thread = threading.Thread(target=super().run)
        self.run_thread.start()

        self.running = True

        while self.running:
            if self.capture_frames:
                self.process_frame()

            time.sleep(self.run_sleep)

        self.shutdown()

    def shutdown(self):
        self.vid.release()
        exit()

    def process_someone_there(self):
        print("someone is here  ")
        if self.state == NO_ONE_THERE:
            self.state = SOMEONE_THERE

            self.publish("camera/someonethere")

        self.last_time_someone_seen = datetime.now()

    def how_long_no_one_seen(self):
        now = datetime.now()

        if self.last_time_someone_seen is None:
            return (now - self.start_time).seconds

        return (now - self.last_time_someone_seen).seconds

    def process_no_one_there(self):
        print("no one is there")
        how_long_no_one_seen = self.how_long_no_one_seen()

        if how_long_no_one_seen is not None and how_long_no_one_seen > self.last_time_no_one_seen_threshold:
            self.state = NO_ONE_THERE
            self.publish("camera/noonethere")

    def process_frame(self):
        print("processing frames...")
        cnt = 0
        last_num_of_people = 0
        while self.running and self.capture_frames:
            ret, frame = self.vid.read()
            if not ret:
                continue

            frame, frame_data = self.fr.detect_faces(frame)
            #self.publish("camera/frame", frame_data.to_json())
            #print(frame_data.to_json())

            if self.show_frames:
                # imshow needs to be run in the main thread
                cv2.imshow('frame', frame)

                key = cv2.waitKey(1) & 0xFF
                if key == ord('q'):
                    self.capture_frames = False
                    break
            else:
                time.sleep(0.1)

            cnt += 1


            num_of_people = frame_data.num_of_people
            if num_of_people > 0:
                self.process_someone_there()
            else:
                self.process_no_one_there()

            print("###last_time_someone_seen: ", self.last_time_someone_seen)
            print("###last_time_someone_seen_threshold: ", self.last_time_someone_seen_threshold)
            print("###how_long_no_one_seen: ", self.how_long_no_one_seen())
            print("###===========================")

        cv2.destroyAllWindows()
        self.publish("camera/photo/complete")

    def handle_facial_recognition_init(self, client, userdata, message):
        self.init()

    def handle_facial_recognition_start(self, client, userdata, message):
        print("###handle_facial_recognition_start")
        self.capture_frames = True

    def handle_facial_recognition_stop(self, client, userdata, message):
        print("###handle_facial_recognition_stop")
        self.capture_frames = False

