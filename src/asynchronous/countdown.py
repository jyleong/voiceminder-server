import threading
import time

class CountDown(threading.Thread):

    def __init__(self, method):
        threading.Thread.__init__(self)
        self.event = threading.Event()
        # lambda method we must provide method arguemtsn to it
        self.method = method

    def run(self):
        print("COUTNDOWN: Starting countdown threading method")
        while not self.event.is_set():
            print("COUNTDOWN: executing lambda method...")
            self.method()
            time.sleep(5)
            self.event.wait(1)

    def stop(self):
        self.event.set()
