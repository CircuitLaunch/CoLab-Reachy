import cv2
import threading
import time
from ...node import NodeBase
from .facialrecogn import FacialRecognition

class Camera(NodeBase):
    def __init__(self, node_name="camera", host="127.0.0.1", port=1883,
                    username=None, password=None, subscribe_dict={}, run_sleep=0.1):
        super().__init__(node_name, host, port, username, password, subscribe_dict, run_sleep)

        self.taking_photo = False

        self.add_subscribe('+/photo/request', self.handle_take_photo)

        # TODO: don't use default params
        self.fr = FacialRecognition()

    def run(self):
        self.run_thread = threading.Thread(target=super().run)
        self.run_thread.start()

        self.running = True

        while self.running:
            if self.taking_photo:
                self.take_photo()
                self.taking_photo = False
            time.sleep(self.run_sleep)

        exit()

    def take_photo(self):
        vid = cv2.VideoCapture(0)
        ret, frame = vid.read()
        vid.release()
        if not ret:
            raise Exception("Taking photo failed")

        frame, rects = self.fr.detect_faces(frame)

        # imshow needs to be run in the main thread
        cv2.imshow('frame', frame)
        #cv2.waitKey()
        while(True):
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            time.sleep(self.run_sleep)

        cv2.destroyAllWindows()

        self.publish("camera/photo/complete")

    def handle_take_photo(self, client, userdata, message):
        self.taking_photo = True

def main():
    node = Camera("camera")
    node.run()

if __name__ == "__main__":
    # execute only if run as a script
    main()