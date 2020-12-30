import threading
import time
from ..model.messages import LogMessage, SayMessage, ThresholdStartMessage, WakeWordStartMessage
from ..node import NodeBase

class Console(NodeBase):
    def __init__(self, node_name="console", host="127.0.0.1", port=1883,
                    username=None, password=None, subscribe_dict={}, run_sleep=0.1):
        super().__init__(node_name, host, port, username, password, subscribe_dict, run_sleep)

        self.run_thread = None

        _command_dict = {
            "stop_all": self.handle_stop_all,
            "log": self.handle_log,
            "say": self.handle_say,
            "facial_recognition_start": self.handle_facial_recognition_start,
            "facial_recognition_stop": self.handle_facial_recognition_stop,
            "sample_motion_head": self.handle_sample_motion_head,
            "sample_motion_orbita": self.handle_sample_motion_orbita,
            "sample_motion_right_arm": self.handle_sample_motion_right_arm,

            # audio in
            "threshold_start": self.handle_threshold_start,
            "wakeword_start": self.handle_start_wakeword,
            "speech_recogn_start": self.handle_speech_recogn_start,
            "deepspeek_start": self.handle_deepspeek_start,
            "deepspeek_stop": self.handle_deepspeek_stop,

            # body
            "body_init": self.handle_body_init,
            "body_shutdown": self.handle_body_shutdown,
            "body_stop": self.handle_body_stop,
            "wave": self.handle_wave_arm,
            "wiggle": self.handle_wiggle_antennas,
            "move_antennas_to_zero": self.handle_move_antennas_to_zero,
            "move_right_arm_to_zero": self.handle_move_right_arm_to_zero,
        }
        self.command_dict.update(_command_dict)

        _command_desc_dict = {
            "stop_all": "stop all nodes (including the console app)",
            "log": "send message to logger",
            "say": "say message",
            "facial_recognition_start": "start facial recognition",
            "facial_recognition_stop": "stop facial recognition",
            "sample_motion_head": "move the head",
            "sample_motion_orbita": "move the orbita",
            "sample_motion_right_arm": "move the right arm",

            # audio in
            "threshold_start": "start threshold",
            "wakeword_start": "start wakeword",
            "speech_recogn_start": "start speech recognition",
            "deepspeek_start": "start deepspeek",
            "deepspeek_stop": "stop deepspeek",

            # body
            "body_init": "init body",
            "body_shutdown": "shutdown body",
            "body_stop": "emergency stop body",
            "wave": "wave arm",
            "wiggle": "wiggle antennas",
            "move_antennas_to_zero": "move head to zero",
            "move_right_arm_to_zero": "move_right_arm_to_zero",
        }
        self.command_desc_dict.update(_command_desc_dict)


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

    def handle_body_init(self, command_input):
        self.publish("console/body/init")

    def handle_body_shutdown(self, command_input):
        self.publish("console/body/shutdown")

    def handle_body_stop(self, command_input):
        self.publish("console/body/stop")

    def handle_wave_arm(self, command_input):
        self.publish("console/body/right_arm/wave")

    def handle_wiggle_antennas(self, command_input):
        self.publish("console/body/head/antenna/wiggle")

    def handle_move_antennas_to_zero(self, command_input):
        self.publish("console/body/head/antenna/zero")

    def handle_move_right_arm_to_zero(self, command_input):
        self.publish("console/body/right_arm/zero")

    def handle_start_wakeword(self, command_input):
        wakeword_start_msg = WakeWordStartMessage()
        self.publish("console/wakeword/start", wakeword_start_msg.to_json())

    def handle_speech_recogn_start(self, command_input):
        self.publish("console/speechrecognition/start")

    def handle_deepspeek_start(self, command_input):
        self.publish("console/deepspeech/listen/start")

    def handle_deepspeek_stop(self, command_input):
        self.publish("console/deepspeech/listen/stop")

def main():
    node = Console("console")
    node.run()

if __name__ == "__main__":
    # execute only if run as a script
    main()
