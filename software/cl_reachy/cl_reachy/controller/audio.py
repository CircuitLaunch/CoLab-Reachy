import threading
from ..node import NodeBase
from ..view.sound.threshold import Threshold
from ..view.sound.wakeword.wakeword import WakeWord
from ..model.messages import AudioInputStateMessage, ThresholdStartMessage, WakeWordStartMessage

THRESHOLD = Threshold.__name__
RECOGNITION = "Recognition"
WAKEWORD = "WakeWord"

class AudioInputController(NodeBase):
    def __init__(self, node_name="audioinput", host="127.0.0.1", port=1883,
                    username=None, password=None, subscribe_dict={}, run_sleep=0.1,
                    wakeword_sensitivity=0.5):
        super().__init__(node_name, host, port, username, password, subscribe_dict, run_sleep)

        self.mic_owner = None
        self.wakeword_sensitivity = wakeword_sensitivity

        self.add_subscribe('+/threshold/start', self.handle_threshold_start)
        self.add_subscribe('+/threshold/stop', self.handle_threshold_stop)
        self.add_subscribe('+/speechrecognition/start', self.handle_speech_recognition_start)
        self.add_subscribe('+/speechrecognition/stop', self.handle_speech_recognition_stop)
        self.add_subscribe('+/wakeword/start', self.handle_wakeword_start)
        self.add_subscribe('+/wakeword/stop', self.handle_wakeword_stop)

    @property
    def is_busy(self):
        return (self.mic_owner is not None)

    @property
    def mic_owner_name(self):
        if self.mic_owner is None:
            return None

        return type(self.mic_owner).__name__

    def make_sigint_handler(self):
        def sigint_handler(signum, frame):
            if self.is_busy and self.mic_owner_name == THRESHOLD:
                self.mic_owner.stop()

            self.node_stop()

        return sigint_handler

    def publish_state(self):
        msg = AudioInputStateMessage(is_busy=self.is_busy, mic_owner=self.mic_owner_name)
        self.publish("audioinput/state", msg.to_json())

    def completed(self):
        self.mic_owner = None
        self.publish_state()

    def handle_threshold_start(self, client, userdata, message):
        _message = str(message.payload.decode("utf-8"))
        threshold_start_msg = ThresholdStartMessage.from_json(_message)

        if self.is_busy:
            if threshold_start_msg.force:
                # force stop
                self.stop()
            else:
                # the mic is busy. don't start. just publish the state
                self.publish_state()
                return

        self.mic_owner = Threshold(action="exec-stop", threshold=threshold_start_msg.threshold,
                                    num=int(threshold_start_msg.num), publish=self.publish)

        self.publish_state()

        def start():
            self.mic_owner.start(final_callback=self.completed)

        t = threading.Thread(target=start)
        t.start()

    def handle_threshold_stop(self, client, userdata, message):
        if self.mic_owner_name == THRESHOLD:
            self.mic_owner.stop()
            self.mic_owner = None

    def handle_speech_recognition_start(self, client, userdata, message):
         pass

    def handle_speech_recognition_stop(self, client, userdata, message):
        pass

    def handle_wakeword_start(self, client, userdata, message):
        _message = str(message.payload.decode("utf-8"))
        wakeword_start_msg = WakeWordStartMessage.from_json(_message)

        if self.is_busy:
            if wakeword_start_msg.force:
                # force stop
                self.stop()
            else:
                # the mic is busy. don't start. just publish the state
                self.publish_state()
                return

        wakeword = WakeWord(publish=self.publish, sensitivity=self.wakeword_sensitivity)
        self.mic_owner = wakeword

        def set_not_busy():
            self.mic_owner = None

        wakeword.handle_wakeword_start(wakeword_start_msg.sensitivity, callback=set_not_busy)

    def handle_wakeword_stop(self, client, userdata, message):
        if self.mic_owner == WAKEWORD:
            self.wakeword.handle_wakeword_stop()
            self.mic_owner = None

    def stop(self):
        if self.mic_owner is not None:
            self.mic_owner.stop()
            self.mic_owner = None

        super().stop()

def main():
    node = None
    try:
        node = AudioInputController("audioinput")
        node.run()
    except KeyboardInterrupt:
        if node is not None:
            node.stop()

if __name__ == "__main__":
    main()

