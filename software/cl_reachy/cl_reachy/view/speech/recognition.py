from ...node import NodeBase

class SpeechRecognition(NodeBase):
    def __init__(self, node_name="speechrecognition", host="127.0.0.1", port=1883,
                    username=None, password=None, subscribe_dict={}, run_sleep=0.1):
        super().__init__(node_name, host, port, username, password, subscribe_dict, run_sleep)

        # TODO

def main():
    node = SpeechRecognition("speechrecognition")
    node.run()

if __name__ == "__main__":
    # execute only if run as a script
    main()
