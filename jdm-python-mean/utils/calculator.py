import statistics

class Calculator:
    def __init__(self, data):
        self.data = data

    def mean(self):
        # Calculate the mean of the data
        mean = statistics.mean(self.data)

        return mean
