import threading
import time
from ..model.messages import LogMessage, SayMessage, ThresholdStartMessage
from ..node import NodeBase

class Console(NodeBase):
    def __init__(self, node_name="console", host="127.0.0.1", port=1883,
                    username=None, password=None, subscribe_dict={}, run_sleep=0.1):
        super().__init__(node_name, host, port, username, password, subscribe_dict, run_sleep)

        self.run_thread = None

        self.command_dict = {
            "help": self.handle_help,
            "stop": self.handle_stop,
            "stop_all": self.handle_stop_all,
            "log": self.handle_log,
            "say": self.handle_say,
            "facial_recognition_start": self.handle_facial_recognition_start,
            "facial_recognition_stop": self.handle_facial_recognition_stop,
            "sample_motion_head": self.handle_sample_motion_head,
            "sample_motion_orbita": self.handle_sample_motion_orbita,
            "sample_motion_right_arm": self.handle_sample_motion_right_arm,
            "threshold_start": self.handle_threshold_start,
        }

        self.command_desc_dict = {
            "help": "general help",
            "stop": "stop the console app",
            "stop_all": "stop all nodes (including the console app)",
            "log": "send message to logger",
            "say": "say message",
            "facial_recognition_start": "start facial recognition",
            "facial_recognition_stop": "stop facial recognition",
            "sample_motion_head": "move the head",
            "sample_motion_orbita": "move the orbita",
            "sample_motion_right_arm": "move the right arm",
            "threshold_start": "start threshold",
        }

    def handle_help(self, command_input):
        print("Commands: ")
        print("=========")

        for key in sorted(self.command_desc_dict.keys()):
            print("{} - {}".format(key, self.command_desc_dict[key]))

        print()

    def handle_stop(self, command_input):
        self.publish("console/stop/console")

    def handle_stop_all(self, command_input):
        self.publish("console/stop/all")

    def get_msg_from_command_input(self, command, command_input):
        start_idx = len(command)+1
        return command_input[start_idx:]

    def handle_log(self, command_input):
        msg = self.get_msg_from_command_input("log", command_input)

        log_msg = LogMessage(msg)
        payload = log_msg.to_json()

        self.publish("console/log", payload=payload)

    def handle_say(self, command_input):
        msg = self.get_msg_from_command_input("say", command_input)

        say_msg = SayMessage(msg)

        payload = say_msg.to_json()
        print(payload)

        self.publish("console/say/request", payload=payload)


    def handle_facial_recognition_start(self, command_input):
        self.publish("console/facialrecognition/start")

    def handle_facial_recognition_stop(self, command_input):
        self.publish("console/facialrecognition/stop")

    def handle_sample_motion_head(self, command_input):
        self.publish("console/sample_motion/request/head")

    def handle_sample_motion_orbita(self, command_input):
        self.publish("console/sample_motion/request/orbita")

    def handle_sample_motion_right_arm(self, command_input):
        self.publish("console/sample_motion/request/right_arm")

    def handle_threshold_start(self, command_input):
        threshold_start_msg = ThresholdStartMessage(threshold="+2000", num=1)
        self.publish("console/threshold/start", threshold_start_msg.to_json())

    def get_command_handler(self, command_input):
        try:
            command = command_input.split(' ')[0]
        except:
            return None

        if command in self.command_dict.keys():
            return self.command_dict[command]

        return None

    def run(self):
        self.run_thread = threading.Thread(target=super().run)
        self.run_thread.start()

        self.running = True
        while self.running:
            command_input = input("> ")
            command_handler = self.get_command_handler(command_input)
            if command_handler is not None:
                command_handler(command_input)

        exit()

def main():
    node = Console("console")
    node.run()

if __name__ == "__main__":
    # execute only if run as a script
    main()