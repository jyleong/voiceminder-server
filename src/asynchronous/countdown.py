import threading
import time

class CountDown(threading.Thread):

    def __init__(self, method):
        threading.Thread.__init__(self)
        self.event = threading.Event()
        self.count = 5
        # lambda method we must provide method arguemtsn to it
        self.method = method

    def run(self):
        print("Starting countdown threading method")
        while self.count > 0 and not self.event.is_set():
            self.method()
            time.sleep(1)
            self.count -= 1
            self.event.wait(1)

    def stop(self):
        self.event.set()
