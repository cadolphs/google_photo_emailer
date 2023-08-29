class OutputListener:
    def __init__(self):
        self.trackers = []

    def track(self, data):
        for tracker in self.trackers:
            tracker.add(data)

    def create_tracker(self):
        tracker = OutputTracker(self)
        self.trackers.append(tracker)
        return tracker

    def remove(self, tracker):
        self.trackers.remove(tracker)


class OutputTracker:
    def __init__(self, listener):
        self.listener = listener
        self._data = []

    def add(self, data):
        self._data.append(data)

    @property
    def data(self):
        return self._data.copy()

    def clear(self):
        data = self.data
        self._data = []
        return data

    def stop(self):
        self.listener.remove(self)
