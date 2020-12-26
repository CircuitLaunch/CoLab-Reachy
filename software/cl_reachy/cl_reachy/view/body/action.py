import threading
from time import sleep

class ActionQueue(object):
    IDLE = "idle"
    RUNNING = "running"
    STOPPED = "stopped"

    def __init__(self, parent):
        self.parent = parent
        self.queue = []

    def make_thread_fnc(self):
        def thread_fnc():
            i = 0
            while self.parent.running == True and self.parent.state != ActionQueue.STOPPED:
                if self.parent.state == ActionQueue.RUNNING and self.len > 0:
                    curr_action = self.remove()
                    if curr_action is not None:
                        curr_action()
                sleep(0.25)

        return thread_fnc

    def run(self):
        self.t = threading.Thread(target=self.make_thread_fnc())
        self.t.start()

    @property
    def len(self):
        return len(self.queue)

    def add(self, action):
        self.queue.append(action)

    def remove(self):
        if self.len == 0:
            return None

        top = self.queue[0]

        if self.len <= 1:
            self.queue = []
        else:
            self.queue = self.queue[1:]

        return top

    def clear(self):
        self.queue = []
