from soundmeter.meter import Meter
from ...model.messages import ThresholdResponseMessage

class Threshold(Meter):
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

            print("###script: ", self.script)
            print("###trigger_callback: ", self.triggered_callback)

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
        self.publish("audioinput/threshold/response", threshold_response_msg.to_json())

        super().start()

    def stop(self):
        super().stop()

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



