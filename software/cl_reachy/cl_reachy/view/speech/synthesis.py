import os
import platform
import pyttsx3
from ...node import NodeBase
from ...model.messages import SayMessage

class SpeechSynthesis(NodeBase):
    def __init__(self, node_name="speechsynthesis", host="127.0.0.1", port=1883,
                    username=None, password=None, subscribe_dict={}, run_sleep=0.1):
        super().__init__(node_name, host, port, username, password, subscribe_dict, run_sleep)

        self.add_subscribe('+/say/request', self.handle_say)

    def speak(self, msg):
        if platform.system() == "Darwin":
             os.system("say \"{}\"".format(msg))
        else:
            self.synthesizer = pyttsx3.init()
            self.synthesizer.say(msg)
            self.synthesizer.runAndWait()

    def handle_say(self, client, userdata, message):
        try:
            _message = str(message.payload.decode("utf-8"))
            say_msg = SayMessage.from_json(_message)

            print(say_msg.msg)
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

