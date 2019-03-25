class StreamingMovingAverage:
    def __init__(self, window_size):
        self.window_size = window_size
        self.values = []
        self.sum = 0

    async def update(self, value):
        """
        Store a given value for calculation
        :param int value:
        """
        self.values.append(value)
        self.sum += value
        if len(self.values) > self.window_size:
            self.sum -= self.values.pop(0)

    def calculate(self):
        """
        Return the average
        :rtype: int
        """
        return int(float(self.sum) / len(self.values))
