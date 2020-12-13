from ..node import NodeBase
from ..view.sound.threshold import Threshold
from ..model.messages import AudioInputStateMessage, ThresholdStartMessage

THRESHOLD = Threshold.__name__
RECOGNITION = "Recognition"
NONE = "None"

class AudioInputController(NodeBase):
    def __init__(self, node_name="audioinput", host="127.0.0.1", port=1883,
                    username=None, password=None, subscribe_dict={}, run_sleep=0.1):
        super().__init__(node_name, host, port, username, password, subscribe_dict, run_sleep)

        self.mic_owner = None

        self.add_subscribe('+/threshold/start', self.handle_threshold_start)
        self.add_subscribe('+/threshold/stop', self.handle_threshold_stop)
        self.add_subscribe('+/speechrecognition/start', self.handle_speech_recognition_start)
        self.add_subscribe('+/speechrecognition/stop', self.handle_speech_recognition_stop)

    @property
    def is_busy(self):
        return (self.mic_owner is not None)

    @property
    def mic_owner_name(self):
        if self.mic_owner is None:
            return NONE

        return type(self.mic_owner).__name__

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
                self.mic_owner.stop()
            else:
                # the mic is busy. don't start. just publish the state
                self.publish_state()
                return

        self.mic_owner = Threshold(action="exec-stop", threshold=threshold_start_msg.threshold,
                                    num=int(threshold_start_msg.num), publish=self.publish)
        self.publish_state()
        self.mic_owner.start(final_callback=self.completed)

    def handle_threshold_stop(self, client, userdata, message):
        if self.mic_owner_name == THRESHOLD:
            self.mic_owner.stop()

    def handle_speech_recognition_start(self, client, userdata, message):
         pass

    def handle_speech_recognition_stop(self, client, userdata, message):
        pass

    def stop(self):
        if self.mic_owner is not None:
            self.mic_owner.stop()

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
