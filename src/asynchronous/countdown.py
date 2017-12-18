import threading
import time

class CountDown(threading.Thread):
    def __init__(self, method, duration=5):
        threading.Thread.__init__(self)
        self.event = threading.Event()
        # lambda method we must provide method arguements to it
        self.method = method
        self.duration = duration

    # this method doesn work if you call it
    def run(self):
        print("COUNTDOWN: Starting countdown threading method")
        while not self.event.is_set():
            print("COUNTDOWN: executing lambda method...")
            self.method()
            time.sleep(self.duration)
            self.event.wait(1)

    def stop(self):
        self.event.set()

class CountDowntoStop(threading.Thread):
    def __init__(self, method, state):
        threading.Thread.__init__(self)
        self.method = method
        self.state = state
        self.countdownTimer = None

    def run(self):
        self.countdownTimer = threading.Timer(15, function=self.method, args=(self.state,))
        self.countdownTimer.start()

    @staticmethod
    def stop():
        self.countdownTimer.cancel()
