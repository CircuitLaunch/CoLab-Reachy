import time
import sys
from ..node import NodeBase
from ..model.messages import RightArmMessage, SayMessage, ThresholdStartMessage

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

    def subscribe_all(self):
        stop_topics = ["+/stop/{}".format(self.node_name), "+/stop/all"]
        for stop_topic in stop_topics:
            if stop_topic not in self.subscribe_dict.keys():
                self.subscribe_dict[stop_topic] = self.node_stop

        # ignore init all. only listen for main controller init.
        init_topic = "+/init/{}".format(self.node_name)
        if init_topic not in self.subscribe_dict.keys():
            self.subscribe_dict[init_topic] = self.node_init

        for key in self.subscribe_dict.keys():
            self.subscribe(key)

    def on_connect(self, client, userdata, flags, rc):
        super().on_connect(client, userdata, flags, rc)

        self.handle_start()

    """
    def node_init(self):
        self.handle_start()
        super().node_init()
    """

    def say(self, msg):
        say_msg = SayMessage(msg)
        payload = say_msg.to_json()
        print(payload)
        self.publish("maincontroller/say/request", payload=payload)

    def handle_start(self, client=None, userdata=None, message=None):
        print("###start")
        self.publish("main/init/all")

        # TODO: do better synchronization instead of just a sleep
        print("staring", end='')
        for i in range(10):
            print(".", end='')
            sys.stdout.flush()
            time.sleep(1)
        print()

        threshold_start_msg = ThresholdStartMessage(num=1)
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
            self.handle_start(client, userdata, message)

    def do_welcome(self):
        print("###welcome")
        #self.say("Welcome to Circuit Launch")

        right_arm_msg = RightArmMessage("Welcome to Circuit Launch")
        self.publish("main/body/right_arm/wave", right_arm_msg.to_json())
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
    node = MainController("main")
    node.run()

if __name__ == "__main__":
    # execute only if run as a script
    main()
