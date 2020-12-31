import time
from ....node import NodeBase
from .meter import ThresholdMeter
from ....model.messages import AudioInputStateMessage, ThresholdStartMessage

class Threshold(NodeBase):
    def __init__(self, node_name="audioinput", host="127.0.0.1", port=1883,
                    username=None, password=None, subscribe_dict={}, run_sleep=0.1,
                    profile="reachy", threshold="+500"):
        super().__init__(node_name, host, port, username, password, subscribe_dict, run_sleep)
        self.profile = profile
        self.threshold = threshold

        self.threshold_meter = None

        self.add_subscribe('+/threshold/start', self.handle_threshold_start)
        self.add_subscribe('+/threshold/stop', self.handle_threshold_stop)

    @property
    def is_busy(self):
        return (self.threshold_meter is not None)

    def node_init(self):
        if self.is_busy:
            self.stop()

        super().node_init()

    def publish_state(self):
        msg = AudioInputStateMessage(is_busy=self.is_busy, listener="threshold")
        self.publish("threshold/threshold/state", msg.to_json())

    def make_sigint_handler(self):
        def sigint_handler(signum, frame):
            self.threshold_meter.stop()

        return sigint_handler

    def completed(self):
        self.threshold_meter = None
        self.publish_state()

    def handle_threshold_start(self, client, userdata, message):
        print("###handle_threshold_start - 1")
        _message = str(message.payload.decode("utf-8"))
        print("###handle_threshold_start - 2 - _message: ", _message)
        threshold_start_msg = ThresholdStartMessage.from_json(_message)

        if self.is_busy:
            print("###handle_threshold_start - 3")

            # force stop
            self.stop()
            while self.is_busy:
                time.sleep(0.1)

        print("###handle_threshold_start - 4")
        self.threshold_meter = ThresholdMeter(action="exec-stop", threshold=self.threshold,
                                    num=int(threshold_start_msg.num), publish=self.publish, verbose=True,
                                    profile=self.profile)

        print("###handle_threshold_start - 5")
        self.threshold_meter.start(final_callback=self.completed)
        print("###handle_threshold_start - 6")

    def handle_threshold_stop(self, client, userdata, message):
        self.threshold_meter.stop()

    def stop(self):
        if self.threshold_meter is not None:
            self.threshold_meter.graceful()
            while self.threshold_meter is not None and self.threshold_meter.is_running:
                # wait for threshold_meter to stop running
                time.sleep(1)

    def handle_quit(self, command_input=None):
        self.stop()

        super().handle_quit(command_input)






