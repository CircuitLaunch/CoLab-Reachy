from datetime import datetime
import re
import random
import signal
import sys
import time
import paho.mqtt.client as paho

class NodeBase(object):
    def __init__(self, node_name="nodebase", host="127.0.0.1", port=1883,
                    username=None, password=None, subscribe_dict={}, run_sleep=30):
        self.node_name = node_name
        self.host = host
        self.port = port

        # make sure that the client id is unique otherwise it will keep connecting and disconnecting from mqtt
        random.seed(datetime.now())
        self.client_id = "{}_{}".format(self.node_name, random.randint(0, sys.maxsize))
        #print(self.client_id)

        self.username = username
        self.password = password
        self.subscribe_dict = subscribe_dict
        self.running = False
        self.run_sleep = run_sleep

        self.client = paho.Client(client_id=self.client_id, clean_session=True)
        #self.client.on_log = self.make_on_log()
        self.client.on_disconnect = self.make_on_disconnect()

        if self.username is not None and self.password is not None:
            self.username_pw_set(username=self.username, password=self.password)

        # Register signal handlers
        signal.signal(signal.SIGINT, self.make_sigint_handler())
        signal.signal(signal.SIGALRM, self.make_sigalrm_handler())

    def make_sigint_handler(self):
        def sigint_handler(signum, frame):
            self.node_stop()

        return sigint_handler

    def make_sigalrm_handler(self):
        def sigalrm_handler(signum, frame):
            self.node_stop()

        return sigalrm_handler

    def run(self):
        print("Running...")
        self.client.on_connect = self.make_on_connect()
        self.client.connect(self.host, self.port, keepalive=90)

        self.subscribe_all()
        self.client.on_message=self.make_on_message()

        self.running = True
        self.client.loop_start()
        while self.running:
            time.sleep(self.run_sleep)
        self.client.loop_stop()
        self.client.disconnect()

    def add_subscribe(self, topic, handler):
        self.subscribe_dict[topic] = handler

    def subscribe_all(self):
        stop_topics = ["+/stop/{}".format(self.node_name), "+/stop/all"]
        for stop_topic in stop_topics:
            if stop_topic not in self.subscribe_dict.keys():
                self.subscribe_dict[stop_topic] = self.node_stop

        for key in self.subscribe_dict.keys():
            self.subscribe(key)

    def on_connect(self, client, userdata, flags, rc):
        #print("connecting...")
        # Subscribing in on_connect() means that if we lose the connection and
        # reconnect then subscriptions will be renewed.
        self.subscribe_all()
        self.client.on_message=self.make_on_message()

    def make_on_connect(self):
        def on_connect(client, userdata, flags, rc):
            self.on_connect(client, userdata, flags, rc)

        return on_connect

    def loop_start(self):
        self.client.loop_start()

    def loop_stop(self):
        self.client.loop_stop()

    def node_stop(self):
        self.running = False

    def subscribe(self, topic):
        self.client.subscribe(topic, qos=2)

    def make_regex_from_subscribe_key(self, subscribe_key):
        p = re.compile('[\+#]')
        return p.sub('.+?', subscribe_key)

    def does_topic_match(self, topic, subscribe_key):
        regex_key = self.make_regex_from_subscribe_key(subscribe_key)
        p = re.compile(regex_key)
        return p.match(topic)

    def is_topic_stop(self, topic):
        return self.does_topic_match(topic, "+/stop/{}".format(self.node_name)) or self.does_topic_match(topic, "+/stop/all")

    def on_message(self, client, userdata, message):
        for key in self.subscribe_dict.keys():
            if self.does_topic_match(message.topic, key):
                if self.is_topic_stop(key):
                    # stop method doesn't take any params
                    self.subscribe_dict[key]()
                else:
                    self.subscribe_dict[key](client, userdata, message)

    def make_on_message(self):
        def on_message(client, userdata, message):
            self.on_message(client, userdata, message)

        return on_message

    def publish(self, topic, payload=None, qos=0, retain=False):
        self.client.publish(topic, payload, qos, retain)

    def on_log(self, client, userdata, level, buf):
        print("log: ",buf)

    def make_on_log(self):
        def on_log(client, userdata, level, buf):
            return self.on_log(client, userdata, level, buf)

        return on_log

    def on_disconnect(self, client, userdata, rc):
        if rc != 0:
            print("Unexpected MQTT disconnection. Will auto-reconnect")

    def make_on_disconnect(self):
        def on_disconnect(client, userdata, rc):
            return self.on_disconnect(client, userdata, rc)

        return on_disconnect

def main():
    node = NodeBase("nodebase")
    node.run()

if __name__ == "__main__":
    # execute only if run as a script
    main()



