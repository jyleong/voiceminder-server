import threading
import time

class EventLoop(threading.Thread):

    def __init__(self, method, duration=5):
        threading.Thread.__init__(self)
        self.event = threading.Event()
        # lambda method we must provide method arguements to it
        self.method = method
        self.duration = duration

    # this method doesn work if you call it
    def run(self):
        print("EVENTLOOP: Starting eventloop threading method")
        while not self.event.is_set():
            print("EVENTLOOP: executing lambda method...")
            self.method()
            time.sleep(self.duration)
            self.event.wait(1)

    def stop(self):
        self.event.set()

class Countdown(threading.Thread):

    def __init__(self, method, duration=5):
        threading.Thread.__init__(self)
        self.event = threading.Event()
        # lambda method we must provide method arguements to it
        self.method = method
        self.duration = duration

    def run(self):
        print("COUNTDOWN: Starting countdown threading method")
        time.sleep(self.duration)
        self.method()
