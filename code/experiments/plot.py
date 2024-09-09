import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

class plottingSignal(object):
    def __init__(self, sample_frequency):
        self.sample_frequency = sample_frequency

    def plot_three_signals(self, signal1, signal2, signal3):
        plt.figure(figsize=(10, 6))

        plt.subplot(3, 1, 1)
        plt.plot(np.arange(len(signal1)) / self.sample_frequency, signal1)
        plt.title('signal1')
        plt.xlabel('Time (s)')
        plt.ylabel('Amplitude')

        plt.subplot(3, 1, 2)
        plt.plot(np.arange(len(signal2)) / self.sample_frequency, signal2)
        plt.title('signal2')
        plt.xlabel('Time (s)')
        plt.ylabel('Amplitude')

        plt.subplot(3, 1, 3)
        plt.plot(np.arange(len(signal3)) / self.sample_frequency, signal3)
        plt.title('Signal3')
        plt.xlabel('Time (s)')
        plt.ylabel('Amplitude')

        plt.tight_layout()
        plt.show()

    def plot_single_signal(self, signal, signal_name="first signal"):
        
        plt.plot(np.arange(len(signal)) / self.sample_frequency, signal)
        plt.title(signal_name)
        #plt.xlim(0.07175, 0.073)
        plt.xlabel('Time (s)')
        plt.ylabel('Amplitude')
        plt.show()

    def plot_CSV(file_path):
        try:
            data_frame = pd.read_csv(self, file_path)
        except FileNotFoundError:
            print("File not found. Please make sure the file path is correct.")
            exit()

        # Plotting the graph
        plt.plot(data_frame['x'], data_frame['y'], color='blue', marker='o', linestyle='-')
        plt.title('Graph')
        plt.xlabel('X-axis')
        plt.ylabel('Y-axis')
        plt.grid(True)
        plt.show()

    
    def plot_twoCSV_together(self, file_path1, file_path2):
        try:
            data_frame1 = pd.read_csv(file_path1)
            data_frame2 = pd.read_csv(file_path2)
        except FileNotFoundError:
            print("One or both files not found. Please make sure the file paths are correct.")
            exit()

        # Plotting the graphs
        # Plot the first graph
        plt.plot(data_frame1['Frequency (Hz)'], data_frame1['Channel 1 Magnitude (dB)'], label='CVS')

        # Plot the second graph on top of the first one
        plt.plot(data_frame2['Frequency (Hz)'], data_frame2['Channel 1 Magnitude (dB)'], label='Mems')

        # Add labels and title
        plt.xlabel('Frequency (Hz)')
        plt.ylabel('Magnitude (dB)')
        plt.title('Comparison between CVS and Mems mics')

        # Add legend
        plt.legend()

        # Show the plot
        plt.show()