import numpy as np
import concurrent.futures
import matplotlib.pyplot as plt


FLAG = True

class TimeDifferenceOfArrival(object):
    def __init__(self, sample_frequency=2e6, time_scale=1e3):
        self.sample_frequency = sample_frequency
        self.time_scale = time_scale

    def __correlate_and_find_max(signal1, signal2):
        correlation = np.correlate(signal1, signal2, mode='full')
        lags = np.arange(-len(signal1) + 1, len(signal2))
        '''
        plt.figure(figsize=(10, 5))
        plt.plot(lags, correlation)
        plt.title('Cross-correlation between Signal 1 and Signal 2')
        plt.xlabel('Lags')
        plt.ylabel('Cross-correlation')
        plt.grid(True)
        plt.show()
        '''
        sample_delta = np.argmax(correlation)
        return sample_delta
    
    def time_delta_1d(self, signal1, signal2):
        m = TimeDifferenceOfArrival.__correlate_and_find_max(signal1, signal2)
        return (m - len(signal1)) / self.sample_frequency * self.time_scale
    
    def time_delta_2d(self, signal1, signal2, signal3):
        with concurrent.futures.ThreadPoolExecutor() as executor:
            future1 = executor.submit(TimeDifferenceOfArrival.__correlate_and_find_max, signal1, signal2)
            future2 = executor.submit(TimeDifferenceOfArrival.__correlate_and_find_max, signal1, signal3)
            
            m1 = future1.result() / self.sample_frequency * self.time_scale
            m2 = future2.result() / self.sample_frequency * self.time_scale
            return m1, m2
