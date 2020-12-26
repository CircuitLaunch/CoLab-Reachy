from ..node import NodeBase
from ..model.messages import SayMessage, ThresholdStartMessage

START = "start"
IDLE = "idle"
SCANNING = "scanning"
WELCOME = "welcome"
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
        self.add_subscribe("+/wakeword/heard", self.handle_wakeword_heard)

    def on_connect(self, client, userdata, flags, rc):
        super().on_connect(client, userdata, flags, rc)

        self.do_start()

    def say(self, msg):
        say_msg = SayMessage(msg)
        payload = say_msg.to_json()
        print(payload)
        self.publish("maincontroller/say/request", payload=payload)

    def do_start(self, client=None, userdata=None, message=None):
        print("###start")
        threshold_start_msg = ThresholdStartMessage(threshold="+1000", num=1)
        payload = threshold_start_msg.to_json()
        self.publish("main/threshold/start", payload)

        self.publish("main/facialrecognition/init")

        self.state = IDLE

    def do_scanning(self):
        print("###scanning")
        # TODO: add some time settings for nobody there and somebody there
        self.publish("maincontroller/facialrecognition/start")

        self.state = SCANNING

    def handle_threshold_triggered(self, client, userdata, message):
        if self.state == IDLE:
            self.do_scanning()

    def handle_no_one_there(self, client, userdata, message):
        if self.state in [SCANNING, GREET, INTERACT]:
            self.do_start(client, userdata, message)

    def do_welcome(self):
        print("###welcome")
        self.say("Welcome to Circuit Launch")
        self.publish("main/body/right_arm/wave")
        self.publish("main/body/head/antenna/wiggle")

        self.state = WELCOME

    def handle_someone_there(self, client, userdata, message):
        if self.state == SCANNING:
            self.do_welcome()

        if self.state in [WELCOME, INTERACT]:
            self.do_greet()

    def do_greet(self):
        print("###greet")
        self.publish("main/body/head/antenna/wiggle")
        self.publish("main/wakeword/start")

        self.state = GREET

    def handle_wakeword_heard(self, client, userdata, message):
        if self.state == WELCOME:
            self.do_interact()

    def do_interact(self, client, userdata, message):
        print("###interact")
        self.publish("main/speechrecognition/start")

def main():
    node = MainController("maincontroller")
    node.run()

if __name__ == "__main__":
    # execute only if run as a script
    main()
