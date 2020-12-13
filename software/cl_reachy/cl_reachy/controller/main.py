from ..node import NodeBase
from ..model.messages import SayMessage, ThresholdStartMessage

START = "start"
IDLE = "idle"
SCANNING = "scanning"

class MainController(NodeBase):
    def __init__(self, node_name="main", host="127.0.0.1", port=1883,
                    username=None, password=None, subscribe_dict={}, run_sleep=0.1):
        super().__init__(node_name, host, port, username, password, subscribe_dict, run_sleep)

        self.state = START

        self.add_subscribe("+/threshold/triggered", self.handle_threshold_triggered)

    def on_connect(self, client, userdata, flags, rc):
        super().on_connect(client, userdata, flags, rc)

        self.state = IDLE
        threshold_start_msg = ThresholdStartMessage(threshold="+2000", num=1)
        payload = threshold_start_msg.to_json()
        self.publish("maincontroller/threshold/start", payload)

    def handle_threshold_triggered(self, client, userdata, message):
        self.state = SCANNING

        say_msg = SayMessage("scanning initiated")
        payload = say_msg.to_json()
        print(payload)

        self.publish("maincontroller/say/request", payload=payload)

        self.publish("maincontroller/facialrecognition/start")


def main():
    node = MainController("maincontroller")
    node.run()

if __name__ == "__main__":
    # execute only if run as a script
    main()