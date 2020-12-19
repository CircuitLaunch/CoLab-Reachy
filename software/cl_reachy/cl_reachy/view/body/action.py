import threading
from time import sleep

class ActionQueue(object):
    IDLE = "idle"
    RUNNING = "running"
    STOPPED = "stopped"

    def __init__(self, parent):
        print("###ActionQueue - 1")
        self.parent = parent
        self.queue = []
        print("###ActionQueue - 2- queue: ", self.queue)

    def make_thread_fnc(self):
        print("###make_thread_fnc")
        def thread_fnc():
            print("###thread_fnc - parent.running: ", self.parent.running)
            print("###thread_fnc - parent.state: ", self.parent.state)
            i = 0
            while self.parent.running == True and self.parent.state != ActionQueue.STOPPED:
                if i % 1000 == 0:
                    print(i, "###parent.state: ", self.parent.state)
                    print(i, "###len: ", self.len)
                i += 1

                if self.parent.state == ActionQueue.RUNNING and self.len > 0:
                    curr_action = self.remove()
                    print("###curr_action: ", curr_action)
                    curr_action()
                    print("###finished action")
                    #self.parent.state = ActionQueue.IDLE
                sleep(0.25)
                #print("###after sleep")

            print("###thread finished: ", self.parent.running, self.parent.state)

        return thread_fnc

    def run(self):
        print("###ActionQueue - run - 1")
        self.t = threading.Thread(target=self.make_thread_fnc())
        self.t.start()

        print("###ActionQueue - run - 2")

    @property
    def len(self):
        return len(self.queue)

    def add(self, action):
        self.queue.append(action)
        print("###add - queue: ", self.queue)


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
