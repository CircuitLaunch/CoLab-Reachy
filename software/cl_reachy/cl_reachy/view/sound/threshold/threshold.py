import time
from ....node import NodeBase
from .meter import ThresholdMeter
from ....model.messages import AudioInputStateMessage, ThresholdStartMessage

class Threshold(NodeBase):
    def __init__(self, node_name="audioinput", host="127.0.0.1", port=1883,
                    username=None, password=None, subscribe_dict={}, run_sleep=0.1,
                    profile="soundmeter"):
        super().__init__(node_name, host, port, username, password, subscribe_dict, run_sleep)
        self.profile = profile

        self.threshold_meter = None

        self.add_subscribe('+/threshold/start', self.handle_threshold_start)
        self.add_subscribe('+/threshold/stop', self.handle_threshold_stop)

    @property
    def is_busy(self):
        return (self.threshold_meter is not None)

    def publish_state(self):
        msg = AudioInputStateMessage(is_busy=self.is_busy, listener="threshold")
        self.publish("threshold/state", msg.to_json())

    def make_sigint_handler(self):
        def sigint_handler(signum, frame):
            self.threshold_meter.stop()

        return sigint_handler

    def completed(self):
        self.threshold_meter = None
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

        self.threshold_meter = ThresholdMeter(action="exec-stop", threshold="+500",
                                    num=int(threshold_start_msg.num), publish=self.publish, verbose=True,
                                    profile=self.profile)

        self.threshold_meter.start(final_callback=self.completed)

    def handle_threshold_stop(self, client, userdata, message):
        if self.mic_owner_name == THRESHOLD:
            self.threshold_meter.stop()
            self.threshold_meter = None

    def stop(self):
        if self.threshold_meter is not None:
            self.threshold_meter.graceful()
            while self.threshold_meter is not None and self.threshold_meter.is_running:
                # wait for threshold_meter to stop running
                time.sleep(1)

    def handle_quit(self, command_input=None):
        self.stop()

        super().handle_quit(command_input)

def main():
    node = None
    try:
        node = Threshold("threshold")
        node.run()
    except KeyboardInterrupt:
        if node is not None:
            node.stop()

if __name__ == "__main__":
    main()




