import threading
import time

class CountDown(threading.Thread):

    def __init__(self, method):
        threading.Thread.__init__(self)
        self.event = threading.Event()
        # lambda method we must provide method arguemtsn to it
        self.method = method
        self.duration = 5

    def run(self):
        print("COUTNDOWN: Starting countdown threading method")
        while not self.event.is_set():
            print("COUNTDOWN: executing lambda method...")
            self.method()
            time.sleep(self.duration)
            self.event.wait(1)

    def runLonger(self, duration):
        print("COUTNDOWN: Starting countdown threading method")
        self.event.clear()
        while not self.event.is_set():
            print("COUNTDOWN: executing lambda method...")
            self.method()
            time.sleep(duration)
            self.event.wait(1)

    def stop(self):
        self.event.set()
