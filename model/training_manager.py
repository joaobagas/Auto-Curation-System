import time
from threading import Thread


class TrainingManager:
    def __init__(self):
        print("Initialized")

    def train(self, progressBar):
        t = Thread(target=self.load, args=(progressBar, ))
        t.start()

    def load(self, progressBar):
        for i in range(101):
            time.sleep(0.05)
            progressBar.setValue(i)
