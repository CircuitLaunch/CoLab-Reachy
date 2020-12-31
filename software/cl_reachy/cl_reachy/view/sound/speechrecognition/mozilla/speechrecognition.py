import logging
import numpy as np
import os
import pathlib
import threading, collections, queue, os, os.path
from .....node import NodeBase
from .....model.messages import HeardMessage
from .mic_vad_streaming import VADAudio
import deepspeech

class DeepSpeech(NodeBase):
    def __init__(self, node_name="deepspeech", host="127.0.0.1", port=1883,
                    username=None, password=None, subscribe_dict={}, run_sleep=0.1,
                    vad_aggressiveness=3, model_path="deepspeech-0.9.3-models.tflite",
                    scorer_path="deepspeech-0.9.3-models.scorer", input_device_index=None, rate=16000):
        super().__init__(node_name, host, port, username, password, subscribe_dict, run_sleep)

        self.vad_aggressiveness=vad_aggressiveness

        self.curr_dir = pathlib.Path(__file__).parent.absolute()
        self.resources_dir = os.path.join(self.curr_dir, "resources")

        self.model_path = os.path.join(self.resources_dir, model_path)
        self.scorer_path = os.path.join(self.resources_dir, scorer_path)
        print("###scorer_path: ", self.scorer_path)

        self.input_device_index = input_device_index

        self.rate = rate

        self.model = None
        self.vad_audio = None

        self.add_subscribe('+/deepspeech/listen/start', self.handle_listen_start)
        self.add_subscribe('+/deepspeech/listen/stop', self.handle_listen_stop)

    def publish_heard(self, text):
        heard_msg = HeardMessage(transcript=text)
        self.publish("deepspeech/heard/response", heard_msg.to_json())

    def handle_listen_start(self, client, userdata, message):
        print("listening...")
        if self.model is None:
            self.model = deepspeech.Model(self.model_path)
            self.model.enableExternalScorer(self.scorer_path)

        if self.vad_audio is None:
            # Start audio with VAD
            self.vad_audio = VADAudio(aggressiveness=self.vad_aggressiveness,
                                device=self.input_device_index,
                                input_rate=self.rate,
                                file=None)
            frames = self.vad_audio.vad_collector()

            # Stream from microphone to DeepSpeech using VAD
            stream_context = self.model.createStream()
            wav_data = bytearray()
            for frame in frames:
                if not self.running:
                    self.vad_audio.running = False
                    break

                if frame is not None:
                    logging.debug("streaming frame")
                    stream_context.feedAudioContent(np.frombuffer(frame, np.int16))
                else:
                    text = stream_context.finishStream()
                    text = text.strip()
                    if text != "":
                        self.publish_heard(text)
                        print("Recognized: %s" % text)
                    stream_context = self.model.createStream()

        self.model = None
        self.vad_audio = None
        print("stopped")

    def handle_listen_stop(self, client, userdata, message):
        # this should stop the generator
        print("stopping...")
        if self.vad_audio is not None:
            self.vad_audio.running = False