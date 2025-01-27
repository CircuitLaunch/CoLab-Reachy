import os
import pathlib
import pydub
import signal
import time
from soundmeter.meter import Meter
from ....model.messages import ThresholdResponseMessage

# TODO: fix segfault
# threshold works fine but segfaults for some reason when trying quit.  The following error message is captured with faulthandler:
# > quit
# Fatal Python error: Segmentation fault
#
# Thread 0xb5beb460 (most recent call first):
#   File "/home/pi/venvs/reachy-env/lib/python3.7/site-packages/paho/mqtt/client.py", \
# line 2919 in _packet_queue
#   File "/home/pi/venvs/reachy-env/lib/python3.7/site-packages/paho/mqtt/client.py", \
# line 2723 in _send_disconnect
#   File "/home/pi/venvs/reachy-env/lib/python3.7/site-packages/paho/mqtt/client.py", \
# line 1374 in disconnect
#   File "/home/pi/CoLab-Reachy/software/cl_reachy/cl_reachy/node.py", line 103 in run\
# _mqtt
#   File "/usr/lib/python3.7/logging/__init__.py", line 861 in release
#   File "/usr/lib/python3.7/logging/__init__.py", line 2050 in shutdown
#
# Thread 0xb6db9860 (most recent call first):
#
# Thread 0x2872076b (most recent call first):
#
# Thread 0xSegmentation fault
# -------------------------------------------
#
# The error looks like it's occurring in the logger in the paho mqtt client thread though.
import faulthandler
faulthandler.enable()

# SoundMeter sets its config file in a funny way.  It's either based on the user home directory or
# set by the SOUNDMETER_TEST_CONFIG environment variable. Set SOUNDMETER_TEST_CONFIG so it can get
# config file from resources.
curr_dir = pathlib.Path(__file__).parent.absolute()
resources_dir = os.path.join(curr_dir, "resources")
os.environ['SOUNDMETER_TEST_CONFIG'] = os.path.join(resources_dir, "config")

class ThresholdMeter(Meter):
    def __init__(self, collect=False, seconds=None, action=None,
                 threshold=None, num=None, script=None, log=None,
                 verbose=False, segment=None, profile=None, publish=None, *args, **kwargs):
        super().__init__(collect=collect, seconds=seconds, action=action,
                 threshold=threshold, num=num, script=script, log=log,
                 verbose=verbose, segment=segment, profile=profile, *args, **kwargs)
        self.callback = None
        self.publish = publish
        self.final_callback = None

        """
        soundmeter --trigger +2000 --action exec --exec ~/.soundmeter/trigger.sh
        """

    def execute(self, rms):
        if self.action == 'stop':
            msg = 'Stop Action triggered'
            print(msg)
            if self.log:
                self.logging.info(msg)
            raise self.__class__.StopException('stop')

        elif self.action == 'exec-stop':
            msg = 'Exec-Stop Action triggered'
            print(msg)
            if self.log:
                self.logging.info(msg)
            v = 'Executing %s' % self.script
            self.verbose_info(v)
            if self.script:
                self.popen(rms)
            elif self.triggered_callback:
                self.triggered_callback()
            raise self.__class__.StopException('exec-stop')

        elif self.action == 'exec':
            msg = 'Exec Action triggered'
            print(msg)
            if self.log:
                self.logging.info(msg)
            v = 'Executing %s' % self.script
            self.verbose_info(v)

            if self.script:
                self.popen(rms)
            elif self.triggered_callback:
                self.triggered_callback()

    def triggered_callback(self):
        threshold_response_msg = ThresholdResponseMessage(True, self.threshold, self.num)
        self.publish("audioinput/threshold/triggered", threshold_response_msg.to_json())

    def start(self, final_callback=None):
        self.final_callback = final_callback

        threshold_response_msg = ThresholdResponseMessage(True, self.threshold, self.num)
        # TODO: update topic - get rid of audioinput
        self.publish("audioinput/threshold/response", threshold_response_msg.to_json())

        segment = self.segment or self.config.AUDIO_SEGMENT_LENGTH
        self.num_frames = int(
            self.config.RATE / self.config.FRAMES_PER_BUFFER * segment)
        if self.seconds:
            signal.setitimer(signal.ITIMER_REAL, self.seconds)
        if self.verbose:
            self._timer = time.time()
        if self.collect:
            print('Collecting RMS values...')
        if self.action:
            # Interpret threshold
            self.get_threshold()

        try:
            self.is_running = True
            record = self.record()
            while not self._graceful:
                record.send(True)  # Record stream `AUDIO_SEGMENT_LENGTH' long

                data = self.output.getvalue()
                segment = pydub.AudioSegment(data)
                rms = segment.rms
                if self.collect:
                    self.collect_rms(rms)
                self.meter(rms)
                if self.action:
                    if self.is_triggered(rms):
                        self.execute(rms)
                self.monitor(rms)
            self.is_running = False
            self.stop()

        except self.__class__.StopException:
            self.is_running = False
            self.stop()

    def stop(self):
        """Stop the stream and terminate PyAudio"""
        self.prestop()
        if not self._graceful:
            self._graceful = True
        self.stream.stop_stream()
        self.audio.terminate()
        msg = 'Stopped'
        self.verbose_info(msg, log=False)
        # Log 'Stopped' anyway
        if self.log:
            self.logging.info(msg)
        if self.collect:
            if self._data:
                print('Collected result:')
                print('    min: %10d' % self._data['min'])
                print('    max: %10d' % self._data['max'])
                print('    avg: %10d' % int(self._data['avg']))
        self.poststop()

    def poststop(self):
        if self.final_callback:
            self.final_callback()