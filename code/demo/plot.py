import sys
sys.path.insert(0, 'C:\\Users\\maaya\\OneDrive\\Desktop\\study\\finalProject\\Final Project\\code')

import process
import matplotlib.pyplot as plt
import pandas as pd

def plot_signals(path):
    data_frame = pd.read_csv(path, header=None)
    signal1, signal2 = process.initial_process(data_frame, process.SAMPLES_PER_PERIOD)

    _, axis = plt.subplots(1, 1, figsize=(20, 40))
    axis.plot(signal1, label='filtered Channel 1')
    axis.plot(signal2, label='filtered Channel 2')
    axis.set_xlabel('Time [micro sec]')
    axis.set_ylabel('Amplitude [mV]')
    axis.set_title('Filtered Signals - Channel 1 & 2')
    axis.grid(True)
    plt.legend() 
    plt.show()

if __name__ == "__main__":
    path = '.\\Raw Data\\recordings\\tryDemoUnderMic1.csv'
    plot_signals(path)