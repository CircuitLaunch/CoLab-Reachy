import time
from ...node import NodeBase
from ...ws import WsIO
from .head import Head
from .orbita import Orbita
from .right_arm import RightArm

class Body(NodeBase):
    def __init__(self, node_name="body", host="127.0.0.1", port=1883,
                    username=None, password=None, subscribe_dict={}, run_sleep=0.1):
        super().__init__(node_name, host, port, username, password, subscribe_dict, run_sleep)

        self.io = WsIO.shared_server('head')

        print("Open http://playground.pollen-robotics.com/#quickstart and click on the connect button.")

        waiting = True
        while waiting:
            cont_input = input("continue? ")
            if cont_input == "y" or cont_input == "y":
                waiting = False

        self.head = Head(self.io)
        self.orbita = Orbita(self.io)
        self.right_arm = RightArm(self.io)

        self.add_subscribe('+/sample_motion/request/head', self.handle_head_sample_motion)
        self.add_subscribe('+/sample_motion/request/orbita', self.handle_orbita_sample_motion)
        self.add_subscribe('+/sample_motion/request/right_arm', self.handle_right_arm_sample_motion)

    def handle_head_sample_motion(self, client, userdata, message):
        print("message topic={}".format(message.topic))
        self.head.sample_motion()
        self.publish("body/sample_motion/completed/head")
        print("completed action")

    def handle_orbita_sample_motion(self, client, userdata, message):
        print("message topic={}".format(message.topic))
        self.orbita.sample_motion()
        self.publish("body/sample_motion/completed/orbita")
        print("completed action")

    def handle_right_arm_sample_motion(self, client, userdata, message):
        print("message topic={}".format(message.topic))
        self.right_arm.sample_motion()
        self.publish("body/sample_motion/completed/right_arm")
        print("completed action")


def main():
    node = Body("body")
    node.run()

if __name__ == "__main__":
    # execute only if run as a script
    main()