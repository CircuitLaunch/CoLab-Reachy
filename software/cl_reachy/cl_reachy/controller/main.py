from ..node import NodeBase
from ..model.messages import SayMessage, ThresholdStartMessage

START = "start"
IDLE = "idle"
SCANNING = "scanning"
GREET = "greet"
INTERACT = "interact"

class MainController(NodeBase):
    def __init__(self, node_name="main", host="127.0.0.1", port=1883,
                    username=None, password=None, subscribe_dict={}, run_sleep=0.1):
        super().__init__(node_name, host, port, username, password, subscribe_dict, run_sleep)

        self.state = START

        self.add_subscribe("+/threshold/triggered", self.handle_threshold_triggered)
        self.add_subscribe("+/someonethere", self.handle_someone_there)
        self.add_subscribe("+/noonethere", self.handle_no_one_there)

    def on_connect(self, client, userdata, flags, rc):
        super().on_connect(client, userdata, flags, rc)

        self.do_start()

    def say(self, msg):
        say_msg = SayMessage(msg)
        payload = say_msg.to_json()
        print(payload)
        self.publish("maincontroller/say/request", payload=payload)

    def do_start(self, client=None, userdata=None, message=None):
        #self.say("starting state")
        print("###starting state")

        threshold_start_msg = ThresholdStartMessage(threshold="+1000", num=1)
        payload = threshold_start_msg.to_json()
        self.publish("maincontroller/threshold/start", payload)

        self.publish("maincontroller/facialrecognition/init")

        self.state = IDLE

    def do_scanning(self):
        #self.say("scanning state")
        print("###scanning state")

        # TODO: add some time settings for nobody there and somebody there
        self.publish("maincontroller/facialrecognition/start")

        self.state = SCANNING

    def handle_threshold_triggered(self, client, userdata, message):
        print("###threshold triggered")
        if self.state == IDLE:
            self.do_scanning()

    def handle_no_one_there(self, client, userdata, message):
        print("###on one there")
        if self.state in [SCANNING, GREET, INTERACT]:
            self.do_start(client, userdata, message)

    def do_greet(self):
        #self.say("greet state")
        print("###greet state")
        self.say("Welcome to Circuit Launch")
        self.publish("console/body/right_arm/wave")
        self.publish("console/body/head/antenna/wiggle")

        self.state = GREET

    def handle_someone_there(self, client, userdata, message):
        print("###handle someone there")
        if self.state == SCANNING:
            self.do_greet()

        if self.state in [GREET, INTERACT]:
            self.do_interact(client, userdata, message)

    def do_interact(self, client, userdata, message):
        print("###interact state")
        #self.say("interact state")
        self.publish("console/body/head/antenna/wiggle")
        self.publish("console/wakeword/start")

def main():
    node = MainController("maincontroller")
    node.run()

if __name__ == "__main__":
    # execute only if run as a script
    main()