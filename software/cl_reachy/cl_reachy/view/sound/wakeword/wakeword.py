from datetime import datetime
import os
import pathlib
import random
import time
import threading
from tzlocal import get_localzone
from ....model.messages import AudioInputStateMessage, SayMessage
from ....node import NodeBase
from .snowboydecoder import set_path
from .hotword import HotwordDetectorWithDevice

class WakeWordListener(object):
    def __init__(self, publish, sensitivity=0.5, input_device_index=2):
        self.publish = publish
        self.sensitivity = sensitivity
        self.input_device_index = input_device_index

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

    """
    def node_init(self):
        self.interrupted = True
    """

    def make_interrupt_callback(self):
        def interrupt_callback():
            return self.interrupted

        return interrupt_callback

    def say(self, msg):
        say_msg = SayMessage(msg)

        payload = say_msg.to_json()

        self.publish("wakeword/say/request", payload=payload)

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
        print("listening...")
        if sensitivity is None:
            sensitivity = self.sensitivity

        def detected_callback():
            self.respond_greet()

            if callback is not None:
                callback()

        if self.detector is None:
            self.interrupted = False
            self.detector = HotwordDetectorWithDevice(self.model_path, sensitivity=sensitivity, input_device_index=self.input_device_index )
            self.detector.start(detected_callback=detected_callback,
                                        interrupt_check=self.make_interrupt_callback(),
                                        sleep_time=0.03)

            self.detector.terminate()
            self.detector = None

    def handle_wakeword_stop(self, client, userdata, message):
        self.interrupted = True

    def stop(self):
        self.interrupted = True

class WakeWord(NodeBase):
    def __init__(self, node_name="wakeword", host="127.0.0.1", port=1883,
                    username=None, password=None, subscribe_dict={}, run_sleep=0.1,
                    wakeword_sensitivity=0.5, input_device_index=2):
        super().__init__(node_name, host, port, username, password, subscribe_dict, run_sleep)

        self.listener = None
        self.wakeword_sensitivity = wakeword_sensitivity
        self.input_device_index = input_device_index

        self.add_subscribe('+/wakeword/start', self.handle_wakeword_start)
        self.add_subscribe('+/wakeword/stop', self.handle_wakeword_stop)

    @property
    def is_busy(self):
        return (self.listener is not None)

    def make_sigint_handler(self):
        def sigint_handler(signum, frame):
            self.node_stop()

        return sigint_handler

    def publish_state(self):
        msg = AudioInputStateMessage(is_busy=self.is_busy, listener="wakeword")
        self.publish("wakeword/state", msg.to_json())

    def completed(self):
        self.publish_state()
        time.sleep(1)
        self.listener = None

    def handle_wakeword_start(self, client, userdata, message):
        _message = str(message.payload.decode("utf-8"))
        #wakeword_start_msg = WakeWordStartMessage.from_json(_message)

        if self.is_busy:
            self.stop()

        """
        if self.is_busy:
            if wakeword_start_msg.force:
                # force stop
                self.stop()
            else:
                # the mic is busy. don't start. just publish the state
                self.publish_state()
                return
        """

        wakeword = WakeWordListener(publish=self.publish, sensitivity=self.wakeword_sensitivity,
                                        input_device_index=self.input_device_index)
        self.listener = wakeword

        def callback():
            print("wakeword heard")
            self.publish("wakeword/wakeword/heard")
            self.listener = None

        self.publish_state()

        wakeword.handle_wakeword_start(callback=callback)

    def handle_wakeword_stop(self, client, userdata, message):
        if self.listener == WAKEWORD:
            self.wakeword.handle_wakeword_stop()
            self.listener = None

    def stop(self):
        if self.listener is not None:
            self.listener.stop()
            self.listener = None

    def handle_quit(self, command_input=None):
        self.stop()
        super().handle_quit()

    def make_handle_stop(self):
        def handle_stop(sig, frame):
            self.running = False

        return handle_stop




