
import numpy as np

from Analytics.LimitOrderBookSeries import LimitOrderBookSeries

class HawkesProcess:

    def __init__(self, intensity_rate):
        self.intensity_rate = intensity_rate

    def generate_events(self, number_of_events):
        """
        :param number_of_events: number of events
        :return: a list of events
        """
        time = 0
        events = np.random.exponential(1.0/self.intensity_rate, number_of_events)
        output = list()
        for event in events:
            time += event
            output.append(np.round(time, 2))

        return output

    def simulate_process(self, events, alpha=0.6, beta=0.8, l=1.2):
        import matplotlib.pyplot as plt
        # return a limit order book series
        max_value = np.ceil(events[-1])
        # I want to increase in increments of 0.01
        x = np.linspace(0, max_value, 100*max_value)

        y = list()
        event = 0
        event_time = 0
        for time in x:
            if np.round(time, 2) in events:
                event = y[-1] + alpha
                event_time = np.round(time, 2)
                y.append(event)
            else:
                y.append(l+np.exp(-beta*(time - event_time)))

        plt.plot()
        plt.plot(x, y)

        plt.show()
        return None

if __name__ == '__main__':
    hawkes = HawkesProcess(1.2)
    events = hawkes.generate_events(100)
    hawkes.simulate_process(events)
