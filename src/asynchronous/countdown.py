import threading

class CountDown(threading.Thread):
    def __init__(self, method, name):
        threading.Thread.__init__(self)
        self.method = method
        self.name = name
        self.countdownTimer = None

    def run(self):
        self.countdownTimer = threading.Timer(10, function=self.method, args=(self.name,))
        self.countdownTimer.start()

    def runLonger(self):
        self.countdownTimer = threading.Timer(11, function=self.method, args=(self.name,))
        self.countdownTimer.start()

    # static to stop all threads
    @staticmethod
    def stop():
        allThreads = threading.enumerate()
        main = threading.main_thread()
        for t in allThreads:
            if t is not main:
                t.cancel()