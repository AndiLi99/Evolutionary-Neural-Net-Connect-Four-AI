import time

class Timer:
    total = 0
    measurements = 0
    def __init__(self):
        self.currentTime = time.clock()

    def lap(self):
        t = time.clock()-self.currentTime
        self.currentTime = time.clock()
        Timer.total += t
        Timer.measurements += 1
        print "average: " + str(Timer.total/Timer.measurements)
        return t

    def start(self):
        self.currentTime = time.clock()
