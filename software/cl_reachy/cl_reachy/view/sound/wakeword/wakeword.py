from datetime import datetime
import os.path
import pathlib
import pytz
import random
import sys
import signal
from tzlocal import get_localzone
from ....model.messages import LogMessage, SayMessage
from .snowboydecoder import HotwordDetector, set_path

class WakeWord(object):
    def __init__(self, publish, sensitivity=0.5):
        self.publish = publish
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

        self.greetings = ['Hello, Human!', 'Hi, nice to meet you', 'How are you doing today?', '***time greeting***']

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
            return "Are you having a good night tonight?"

    # TODO: maybe this should be moved to the main controller
    def respond_greet(self):
        choice = random.randint(0,len(self.greetings)-1)
        greeting = self.greetings[choice]

        if greeting == '***time greeting***':
            greeting = self.get_time_greeting()

        self.say(greeting)

        self.interrupted = True
        self.publish('wakeword/completed')

    def handle_wakeword_start(self, sensitivity=None, callback=None):
        if sensitivity is None:
            sensitivity = self.sensitivity

        def detected_callback():
            self.respond_greet()

            if callback is not None:
                callback()

        if self.detector is None:
            self.interrupted = False
            self.detector = HotwordDetector(self.model_path, sensitivity=sensitivity)
            self.detector.start(detected_callback=detected_callback,
                                        interrupt_check=self.make_interrupt_callback(),
                                        sleep_time=0.03)

            self.detector.terminate()
            self.detector = None

    def handle_wakeword_stop(self, client, userdata, message):
        self.interrupted = True

    def stop(self):
        self.interrupted = True

