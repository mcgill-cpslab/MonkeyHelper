from Replayer import ReplayEvent
from Pipeline import PipelineParcel


class EventGenerator:

    def __init__(self, interval=3000, number=100):
        '''interval is in ms'''
        self.number = number
        self.interval = interval
        self.list = self.generate()

    def generate(self):
        list = []
        timestamp = 0
        for i in range(self.number):
            timestamp += self.interval
            list.append(ReplayEvent(timestamp))
        return list[::-1]

    def next(self, dummy):
        parcel = PipelineParcel()
        if self.list:
            parcel.enqueue(self.list.pop())
        return parcel
