import os
from gtts import gTTS
from io import BytesIO
from pydub import AudioSegment
from pydub.playback import play
from tempfile import NamedTemporaryFile
from ...node import NodeBase
from ...model.messages import SayMessage

class SpeechSynthesis(NodeBase):
    def __init__(self, node_name="speechsynthesis", host="127.0.0.1", port=1883,
                    username=None, password=None, subscribe_dict={}, run_sleep=0.1):
        super().__init__(node_name, host, port, username, password, subscribe_dict, run_sleep)

        self.add_subscribe('+/say/request', self.handle_say)

    def speak(self, msg):
        mp3_fp = BytesIO()

        tts = gTTS(msg, lang='en')
        tts.write_to_fp(mp3_fp)

        fp = NamedTemporaryFile()
        tts.write_to_fp(fp)
        fp.flush()

        audio = AudioSegment.from_file_using_temporary_files(fp.name, format="mp3")
        play(audio)
        #os.system("mpg123 -a plughw:0,0 {}".format(fp.name))

        fp.close()

    def handle_say(self, client, userdata, message):
        try:
            _message = str(message.payload.decode("utf-8"))
            say_msg = SayMessage.from_json(_message)

            self.speak(say_msg.msg)

            self.publish("speechsynthesis/say/complete")
        except Exception as ex:
            print("ERROR - handle_say: {}".format(ex))

def main():
    node = SpeechSynthesis("speechsynthesis")
    node.run()

if __name__ == "__main__":
    # execute only if run as a script
    main()

