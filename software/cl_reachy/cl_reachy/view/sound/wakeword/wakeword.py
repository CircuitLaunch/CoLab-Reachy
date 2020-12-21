from datetime import datetime
import os.path
import pathlib
import pytz
import random
import sys
import signal
from tzlocal import get_localzone
from ....node import NodeBase
from ....model.messages import LogMessage, SayMessage
from .snowboydecoder import HotwordDetector, set_path

class WakeWord(NodeBase):
    def __init__(self, node_name="wakeword", host="127.0.0.1", port=1883,
                    username=None, password=None, subscribe_dict={}, run_sleep=0.1,
                    sensitivity=0.5):
        super().__init__(node_name, host, port, username, password, subscribe_dict, run_sleep)
        self.sensitivity = sensitivity

        # TODO: maybe move these files to a better location
        self.curr_dir = pathlib.Path(__file__).parent.absolute()
        print(self.curr_dir)
        self.resources = os.path.join(self.curr_dir, "resources")
        self.model_path = os.path.join(self.resources, "models", "reachy.umdl")

        # set PYTHONPATH to use the right shared library
        set_path()

        self.interrupted = False
        self.detector = None

        signal.signal(signal.SIGINT, self.make_handle_stop())

        self.greetings = ['Hello, Human!', 'Hi, nice to meet you', 'How are you doing today?', '***time greeting***']

        self.add_subscribe('+/wakeword/start', self.handle_wakeword_start)
        self.add_subscribe('+/wakeword/stop', self.handle_wakeword_stop)

    def make_signal_stop(self):
        def signal_handler(signal, frame):
            self.interrupted = True
            sleep(5)
            super().make_handle_stop()()

        return signal_handler

    def make_interrupt_callback(self):
        def interrupt_callback():
            return self.interrupted

        return interrupt_callback

    def say(self, msg):
        say_msg = SayMessage(msg)

        payload = say_msg.to_json()

        self.publish("console/say/request", payload=payload)

    def get_time_greeting(self):
        now = datetime.now().astimezone(get_localzone())

        if now.hour >= 4 and now.hour < 12:
            return "Good morning"
        elif now.hour >= 12 and now.hour < 6:
            return "Good afternoon"
        elif now.hour >= 6 and now.hour < 10:
            return "Good evening"
        else:
            return "Good night"

    def make_respond_greet(self):
        def respond_greet():
            choice = random.randint(0,len(self.greetings)-1)
            greeting = self.greetings[choice]

            if greeting == '***time greeting***':
                greeting = self.get_time_greeting()

            self.say(greeting)

            self.interrupted = True
            self.publish('wakeword/completed')

        return respond_greet

    def handle_wakeword_start(self, client, userdata, message):
        if self.detector is None:
            self.interrupted = False
            self.detector = HotwordDetector(self.model_path, sensitivity=self.sensitivity)
            self.detector.start(detected_callback=self.make_respond_greet(),
                                        interrupt_check=self.make_interrupt_callback(),
                                        sleep_time=0.03)

            self.detector.terminate()
            self.detector = None

    def handle_wakeword_stop(self, client, userdata, message):
        self.interrupted = True

    def run(self):
        super().run()

        self.interrupted = True
        if self.detector is not None:
            self.detector.terminate()
        self.detector = None

def main():
    node = WakeWord("wakeword")
    node.run()

if __name__ == "__main__":
    # execute only if run as a script
    main()
