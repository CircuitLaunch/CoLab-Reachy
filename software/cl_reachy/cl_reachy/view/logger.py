import logging
from ..node import NodeBase
from ..model.messages import LogMessage
import traceback

class Logger(NodeBase):
    def __init__(self, node_name="logger", host="127.0.0.1", port=1883,
                    username=None, password=None, subscribe_dict={}, run_sleep=0.1):
        super().__init__(node_name, host, port, username, password, subscribe_dict, run_sleep)

        self.add_subscribe('+/log', self.handle_log)

        self.logger = logging.getLogger('logger')
        self.logger.addHandler(logging.StreamHandler())
        self.logger.setLevel(logging.DEBUG)

    def handle_log(self, client, userdata, message):
        try:
            _message = str(message.payload.decode("utf-8"))
            log_msg = LogMessage.from_json(_message)
            log_msg_str = str(log_msg)
        except Exception as ex:
            self.logger.error(ex)
            traceback.print_exc()
            log_msg_str = str(message.payload.decode("utf-8"))

        self.logger.info("message received {}".format(log_msg_str))
        self.logger.info("message topic={}".format(message.topic))
        self.logger.info("message qos={}".format(message.qos))
        self.logger.info("message retain flag={}".format(message.retain))
        self.logger.info("")

def main():
    node = Logger("logger")
    node.run()

if __name__ == "__main__":
    # execute only if run as a script
    main()