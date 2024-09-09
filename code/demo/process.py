import sys
sys.path.insert(0, 'C:\\Users\\maaya\\OneDrive\\Desktop\\study\\finalProject\\Final Project\\code')

import numpy as np
from scipy.signal import butter, filtfilt
from sound_localization.tdoa import TimeDifferenceOfArrival
from sound_localization.triangulation import Triangulation
from sound_localization.calibration import CalibrationSpeedOfSound
import matplotlib.pyplot as plt
import pandas as pd
from scipy.signal import find_peaks

SAMPLE_FREQUENCY = 1e6  # 1 MHz
SAMPLE_DURATION = 1 # 1 s
TOTAL_SAMPLES = int(SAMPLE_FREQUENCY * SAMPLE_DURATION)
NYQUIST_FREQUENCY = SAMPLE_FREQUENCY / 2
CHIRP_HIGH_FREQUENCY = 65e3 # 55kHz
CHIRP_LOW_FREQUENCY = 40e3 # 45kHz
CHIRP_DURATION = 500e-6 # 500 us
CHIRP_PERIOD = 50e-3 # 50 ms
SAMPLES_PER_CHIRP = int(SAMPLE_FREQUENCY * CHIRP_DURATION)
SAMPLES_PER_PERIOD = int(SAMPLE_FREQUENCY * CHIRP_PERIOD)
HEIGHT = 100 # cm


def crop_and_filter(data_frame, target_size : int = SAMPLES_PER_PERIOD):
    sample_start_index = int(len(data_frame) / 2) - int(target_size / 2)
    sample_end_index = sample_start_index + target_size
    data_frame = data_frame[sample_start_index:sample_end_index]

    # data_frame = savgol_filter(data_frame, 101, 2)
    b, a = butter(6, [CHIRP_LOW_FREQUENCY / NYQUIST_FREQUENCY, CHIRP_HIGH_FREQUENCY / NYQUIST_FREQUENCY], btype='band')
    return filtfilt(b, a, data_frame), data_frame

def find_peaks_and_remove_crosstalk(signal, height=50, prominence=20, distance=500):
    peaks, _ = find_peaks(signal, height=height, prominence=prominence, distance=distance)
    first_peak_index = peaks[0]
    start_of_second_peak = peaks[1]
    end_of_first_peak = np.where(signal[first_peak_index:start_of_second_peak] < 0)[0]
    end_of_first_peak_index = first_peak_index + end_of_first_peak[-1] // 2
    signal_no_crosstalk = signal[end_of_first_peak_index: end_of_first_peak_index + SAMPLES_PER_PERIOD // 2]
    return signal_no_crosstalk, peaks

def initial_process(data_frame, target_size):
    channel1, received_channel1 = crop_and_filter(data_frame[0], target_size)
    channel2, received_channel2 = crop_and_filter(data_frame[1], target_size)
    
    return channel1, channel2

def process(data_frame):
    channel1, channel2 = initial_process(data_frame, TOTAL_SAMPLES - SAMPLES_PER_PERIOD * 2)
    channel1, received_channel1 = crop_and_filter(data_frame[0], SAMPLES_PER_PERIOD)
    channel2, received_channel2 = crop_and_filter(data_frame[1], SAMPLES_PER_PERIOD)
    
    channel1_no_crosstalk, peaks_channel1 = find_peaks_and_remove_crosstalk(channel1, height=50, prominence=20, distance=500)
    channel2_no_crosstalk, peaks_channel2 = find_peaks_and_remove_crosstalk(channel2, height=50, prominence=20, distance=500)

    return channel1_no_crosstalk, channel2_no_crosstalk