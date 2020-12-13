import cv2
import threading
import time
from ...node import NodeBase
from .facialrecogn import FacialRecognition
from ...model.messages import SayMessage

class Camera(NodeBase):
    def __init__(self, node_name="camera", host="127.0.0.1", port=1883,
                    username=None, password=None, subscribe_dict={}, run_sleep=0.1):
        super().__init__(node_name, host, port, username, password, subscribe_dict, run_sleep)

        self.capture_frames = False
        self.vid = cv2.VideoCapture(0)

        self.add_subscribe('+/facialrecognition/start', self.handle_facial_recognition_start)
        self.add_subscribe('+/facialrecognition/stop', self.handle_facial_recognition_stop)

        # TODO: don't use default params
        self.fr = FacialRecognition(confidence=0.9)

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

    def process_frame(self):
        cnt = 0
        while self.capture_frames:
            ret, frame = self.vid.read()
            if not ret:
                continue

            frame, frame_data = self.fr.detect_faces(frame)
            #self.publish("camera/frame", frame_data.to_json())
            #print(frame_data.to_json())

            # imshow needs to be run in the main thread
            cv2.imshow('frame', frame)

            key = cv2.waitKey(1) & 0xFF
            if key == ord('q'):
                self.capture_frames = False
                break

            cnt += 1
            print("###cnt: ", cnt)

            if cnt % 20 == 0:
                num_of_people = frame_data.num_of_people
                if num_of_people == 0:
                    say_msg = SayMessage("There are no people in the frame")
                elif num_of_people == 1:
                    say_msg = SayMessage("There is one person in the frame")
                else:
                    say_msg = SayMessage("There are {} people in the frame".format(num_of_people))
                payload = say_msg.to_json()
                print(payload)

                self.publish("maincontroller/say/request", payload=payload)

        cv2.destroyAllWindows()
        self.publish("camera/photo/complete")

    def handle_facial_recognition_start(self, client, userdata, message):
        print("###handle_facial_recognition_start")
        self.capture_frames = True

    def handle_facial_recognition_stop(self, client, userdata, message):
        print("###handle_facial_recognition_stop")
        self.capture_frames = False

def main():
    node = Camera("camera")
    node.run()

if __name__ == "__main__":
    # execute only if run as a script
    main()