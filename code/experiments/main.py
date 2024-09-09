#!/usr/bin/python3 
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

# from scipy.signal import savgol_filter

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
    
def main():
    # *************************
    # Calibrate Speed Of Sound
    # *************************
    original_sweep = pd.read_csv('.\\Raw Data\\recordings\\original_signal_sweep.csv', header=None)

    calibration_data_frame = pd.read_csv('.\\Raw Data\\recordings\\tryDemoUnderMic1.csv', header=None)    
     
    calibration_channel1, received_channel1 = crop_and_filter(calibration_data_frame[0], int(SAMPLES_PER_PERIOD * 2))
    calibration_channel2, received_channel2 = crop_and_filter(calibration_data_frame[1], int(SAMPLES_PER_PERIOD * 2))
    
    calibration_channel1_no_crosstalk, peaks_channel1 = find_peaks_and_remove_crosstalk(calibration_channel1, height=50, prominence=20, distance=500)
    calibration_channel2_no_crosstalk, peaks_channel2 = find_peaks_and_remove_crosstalk(calibration_channel2, height=50, prominence=20, distance=500)

    received_channel1 = received_channel1[:len(calibration_channel1_no_crosstalk)]
    received_channel2 = received_channel2[:len(calibration_channel2_no_crosstalk)]
   
    
    # Plotting

    # original sweep wave
    original_sweep.columns = ['Time', 'Amplitude']
    original_sweep['Time'] = original_sweep['Time'] * 1e6
    plt.figure(figsize=(10, 6))
    plt.plot(original_sweep['Time'], original_sweep['Amplitude'])
    plt.xlabel('Time [micro sec]')
    plt.ylabel('Amplitude [V]')
    plt.title('Original Sweep Plot')
    plt.grid(True)
    plt.show()

    plt.figure(figsize=(10, 6))
    plt.plot(received_channel1)
    plt.title('received Signal')
    plt.xlabel('Sample Number')
    plt.ylabel('Amplitude [mV]')
    plt.title('One Cycle of The Received Signal - Channel 1')
    plt.grid(True)
    plt.show()

    plt.figure(figsize=(10, 6))
    plt.plot(calibration_channel1)
    plt.title('Filtered Signal - Channel 1')
    plt.xlabel('Sample Number')
    plt.ylabel('Amplitude [mV]')
    plt.grid(True)
    plt.show()

    # plot filtered signals with found peaks 
    plt.figure(figsize=(14, 6))
    plt.subplot(2, 1, 1)
    plt.plot(calibration_channel1, label='Channel 1')
    plt.plot(peaks_channel1, calibration_channel1[peaks_channel1], "x", label='Peaks Channel 1')
    plt.title('Channel 1 with Peaks')
    plt.xlabel('Sample Number')
    plt.ylabel('Amplitude [mV]')
    plt.grid(True)
    plt.legend()
    plt.subplot(2, 1, 2)
    plt.plot(calibration_channel2, label='Channel 2')
    plt.plot(peaks_channel2, calibration_channel2[peaks_channel2], "x", label='Peaks Channel 2')
    plt.title('Channel 2 with Peaks')
    plt.xlabel('Sample Number')
    plt.ylabel('Amplitude [mV]')
    plt.legend()
    plt.tight_layout()
    plt.grid(True)
    plt.show()

    plt.figure(figsize=(10, 6))
    plt.plot(calibration_channel1_no_crosstalk)
    plt.title('Filtered Signal without crosstalk')
    plt.xlabel('Sample Number')
    plt.ylabel('Amplitude [mV]')
    plt.grid(True)
    plt.show()


    plt.figure(figsize=(12, 6))
    
    # Original cropped received signal
    plt.subplot(3, 1, 1)  # 2 rows, 1 column, 1st subplot
    plt.plot(received_channel1)
    plt.title('Original Cropped Signal')
    plt.xlabel('Sample Number')
    plt.ylabel('Amplitude [mV]')
    plt.grid(True)

    
    # Filtered signal with crosstalk
    plt.subplot(3, 1, 2)
    plt.plot(calibration_channel1)
    plt.title('Filtered Signal with crosstalk')
    plt.xlabel('Sample Number')
    plt.ylabel('Amplitude [mV]')
    plt.grid(True)

    plt.subplot(3, 1, 3)
    plt.plot(calibration_channel1_no_crosstalk, color='orange')
    plt.title('Filtered Signal without crosstalk')
    plt.xlabel('Sample Number')
    plt.ylabel('Amplitude [mV]')
    
    plt.tight_layout()
    plt.grid(True)

    plt.show()
    
    _, axis = plt.subplots(1, 1, figsize=(20, 40))
    axis.plot(calibration_channel1_no_crosstalk, label='Channel 1')
    axis.plot(calibration_channel2_no_crosstalk, label='Channel 2')
    axis.set_xlabel('Time [micro sec]')
    axis.set_ylabel('Amplitude [mV]')
    axis.set_title('Calibration Signals')
    axis.grid(True)
    plt.legend() 
    plt.show()


    calibration = CalibrationSpeedOfSound(SAMPLE_FREQUENCY, 1e3) 
    speed_of_sound = calibration.calc_speed_of_sound(calibration_channel1, calibration_channel2)
    print("speed of sound: {} cm/ms".format(speed_of_sound))
    
    # ************************
    # Filter and Sample Signal
    # ************************
    data_frame = pd.read_csv('.\\Raw Data\\recordings\\tryDemoUnderMic1.csv', header=None)
    filtered_channel1, _ = crop_and_filter(data_frame[0], TOTAL_SAMPLES - SAMPLES_PER_PERIOD * 2)
    filtered_channel2, _ = crop_and_filter(data_frame[1], TOTAL_SAMPLES - SAMPLES_PER_PERIOD * 2)


    _, axis = plt.subplots(1, 1, figsize=(20, 40))
    axis.plot(filtered_channel1, label='filtered Channel 1')
    axis.plot(filtered_channel2, label='filtered Channel 2')
    axis.set_xlabel('Time [micro sec]')
    axis.set_ylabel('Amplitude [mV]')
    axis.set_title('Filtered Signals - Channel 1 & 2')
    axis.grid(True)
    plt.legend() 
    plt.show()
    
    filtered_channel1, _ = crop_and_filter(filtered_channel1, SAMPLES_PER_PERIOD)
    filtered_channel2, _ = crop_and_filter(filtered_channel2, SAMPLES_PER_PERIOD)
    
    _, axis = plt.subplots(2, 1, figsize=(20, 40))
    axis[0].plot(filtered_channel1)
    axis[0].set_xlabel('Time [micro sec]')
    axis[0].set_ylabel('Amplitude [mV]')
    axis[0].set_title('Sampled Signal - Channel 1 - Single Period')
    axis[0].grid(True)
    axis[1].plot(filtered_channel2)
    axis[1].set_xlabel('Time [micro sec]')
    axis[1].set_ylabel('Amplitude [mV]')
    axis[1].set_title('Sampled Signal - Channel 2 - Single Period')
    axis[1].grid(True)
    plt.show()


    

    filtered_channel1_no_crosstalk, peaks_channel1 = find_peaks_and_remove_crosstalk(filtered_channel1, height=50, prominence=20, distance=500)
    filtered_channel2_no_crosstalk, peaks_channel2 = find_peaks_and_remove_crosstalk(filtered_channel2, height=50, prominence=20, distance=500)

            
    peak_index_channel1 = peaks_channel1[1]
    peak_index_channel2 = peaks_channel2[2]

    # Extracting the second peak values for each channel
    peak_value_channel1 = filtered_channel1[peak_index_channel1]
    peak_value_channel2 = filtered_channel2[peak_index_channel2]

    # Calculate the delta for the second peak
    delta_second_peak = peak_index_channel2 - peak_index_channel1
    print("print!!!")
    print("delta second peak = ",delta_second_peak)
    # Plotting the filtered channels

    plt.figure(figsize=(15,7))
    plt.plot(filtered_channel1, label='Filtered Channel 1')
    plt.plot(filtered_channel2, label='Filtered Channel 2')

    # Plotting the second peak for both channels
    plt.plot(peak_index_channel1, peak_value_channel1, 'go', label='Second Peak Channel 1')  # green dot on channel 1
    plt.plot(peak_index_channel2, peak_value_channel2, 'ro', label='Second Peak Channel 2')  # red dot on channel 2
        
    arrow_start = (peak_index_channel2, peak_value_channel2)
    # End of the arrow (at second peak of channel 1)
    arrow_end = (peak_index_channel1, peak_value_channel2)

    # Adding an arrow annotation with the calculated delta
    plt.annotate(f'Delta: {delta_second_peak:.0f} micro Sec',
                xy=arrow_end,
                xytext=arrow_start,
                arrowprops=dict(arrowstyle="<->", color='red', lw=2),
                fontsize=14)

    plt.legend()
    plt.title('Filtered Signals with Delta Annotation for Second Peak')
    plt.xlabel('Time [micro sec]')
    plt.ylabel('Amplitude [mV]')
    plt.grid(True)
    plt.show()



    
    _, axis = plt.subplots(1, 1, figsize=(20, 40))
    axis.plot(filtered_channel1, label='Channel 1')
    axis.plot(filtered_channel1_no_crosstalk, label='Channel 1 no crosstalk')
    axis.set_xlabel('Time [micro sec]')
    axis.set_ylabel('Amplitude [mV]')
    axis.set_title('Channel 1 no crosstalk')
    axis.grid(True)
    plt.legend() 
    plt.show()

    _, axis = plt.subplots(1, 1, figsize=(20, 40))
    axis.plot(filtered_channel2, label='Channel 2')
    axis.plot(filtered_channel2_no_crosstalk, label='Channel 2 no crosstalk')
    axis.set_xlabel('Time [micro sec]')
    axis.set_ylabel('Amplitude [mV]')
    axis.set_title('Channel 2 no crosstalk')
    axis.grid(True)
    plt.legend() 
    plt.show()
    


     # plot filtered signals with found peaks 
    plt.figure(figsize=(14, 6))
    plt.subplot(2, 1, 1)
    plt.plot(filtered_channel1, label='Channel 1')
    plt.plot(peaks_channel1, filtered_channel1[peaks_channel1], "x", label='Peaks Channel 1')
    plt.title('Channel 1 with Peaks')
    plt.legend()
    plt.subplot(2, 1, 2)
    plt.plot(filtered_channel2, label='Channel 2')
    plt.plot(peaks_channel2, filtered_channel2[peaks_channel2], "x", label='Peaks Channel 2')
    plt.title('Channel 2 with Peaks')
    plt.legend()
    plt.tight_layout()
    plt.show()

    
    # ************************
    # Calculate the time delta
    # ************************
    tdoa = TimeDifferenceOfArrival(sample_frequency=SAMPLE_FREQUENCY)
    time_delta = tdoa.time_delta_1d(filtered_channel1_no_crosstalk, filtered_channel2_no_crosstalk)
    print(time_delta)
    
    # ****************************
    # Calculate Location of signal
    # ****************************
    triang = Triangulation(height=HEIGHT, bounds=[HEIGHT, HEIGHT], speed_of_sound=speed_of_sound)
    x = triang.location_1d(time_delta)

 
    
    print("Time deltas: {} ms".format(time_delta))
    print("Coordinates: ({})".format(x))
    
if __name__ == "__main__":
    main()