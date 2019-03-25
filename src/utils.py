import threading


class StreamingMovingAverage:
    """
    TODO: add description
    """
    def __init__(self, window_size):
        self.moving_average_lock = threading.Lock()
        self.window_size = window_size
        self.values = []
        self.sum = 0

    def process(self, value):
        with self.moving_average_lock:
            self.values.append(value)
            self.sum += value
            if len(self.values) > self.window_size:
                self.sum -= self.values.pop(0)
            return int(float(self.sum) / len(self.values))
