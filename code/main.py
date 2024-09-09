#!/usr/bin/python3 
import sys
sys.path.insert(0, 'G:\\My Drive\\Final Project\\code')

import numpy as np
from scipy.signal import butter, filtfilt
from sound_localization.tdoa import TimeDifferenceOfArrival
from sound_localization.triangulation import Triangulation
from sound_localization.calibration import CalibrationSpeedOfSound
import serial

SAMPLE_FREQUENCY = 1e6  # 1 MHz
SAMPLE_DURATION = 1 # 1 s
TOTAL_SAMPLES = int(SAMPLE_FREQUENCY * SAMPLE_DURATION)
NYQUIST_FREQUENCY = SAMPLE_FREQUENCY / 2
CHIRP_HIGH_FREQUENCY = 55e3 # 55kHz
CHIRP_LOW_FREQUENCY = 45e3 # 45kHz
CHIRP_DURATION = 500e-6 # 500 us
CHIRP_PERIOD = 50e-3 # 50 ms
SAMPLES_PER_CHIRP = int(SAMPLE_FREQUENCY * CHIRP_DURATION)
SAMPLES_PER_PERIOD = int(SAMPLE_FREQUENCY * CHIRP_PERIOD)
FILTER_LOW_FREQUENCY = 35e3
FILTER_HIGH_FREQUENCY = 65e3

HEIGHT = 100 # cm

uart = serial.Serial('COM3', 115200, timeout=1)
    
def receive_string_from_uart():   
    while uart.in_waiting == 0:
        pass
    
    # Read the string from UART
    received_string = uart.readline().decode()
        
    return received_string

def crop_and_filter(data_frame, target_size : int = SAMPLES_PER_PERIOD):
    sample_start_index = int(len(data_frame) / 2) - int(target_size / 2)
    sample_end_index = sample_start_index + target_size
    data_frame = data_frame[sample_start_index:sample_end_index].astype(np.float32)
    b, a = butter(6, [FILTER_LOW_FREQUENCY / NYQUIST_FREQUENCY, FILTER_HIGH_FREQUENCY / NYQUIST_FREQUENCY], btype='band')
    return filtfilt(b, a, data_frame).astype(np.float32)
    
def main():
    while (True):
        # ************************
        # Filter and Sample Signal
        # ************************
        uart_buffer = receive_string_from_uart().split(" ")
        # convert every element in the list to uint16
        data_frame = np.array(list(map(np.uint16, uart_buffer)))
        #convert every element in the date_frame to binary
        # data_frame = np.array(list(map(np.binary_repr, data_frame)))
                
        #uzip data_frame to 3 signals
        data_frame_a = data_frame[0::3]
        data_frame_b = data_frame[1::3]
        data_frame_c = data_frame[2::3]
        
        print(data_frame_a)
        print(data_frame_b)
        print(data_frame_c)
        print("*******************")
        
        # filtered_channel1 = crop_and_filter(data_frame_a, SAMPLES_PER_PERIOD * 2)
        # filtered_channel2 = crop_and_filter(data_frame_b, SAMPLES_PER_PERIOD * 2)

        # # ************************
        # # Calculate the time delta
        # # ************************
        # tdoa = TimeDifferenceOfArrival(sample_frequency=SAMPLE_FREQUENCY)
        # time_delta = tdoa.time_delta_1d(filtered_channel1, filtered_channel2)
        
        # # ****************************
        # # Calculate Location of signal
        # # ****************************
        # triang = Triangulation(height=HEIGHT, bounds=[HEIGHT, HEIGHT])
        # x = triang.location_1d(time_delta)
        
        # print("Time deltas: {} ms".format(time_delta))
        # print("Coordinates: ({:.2f})".format(x))
    
if __name__ == "__main__":
    main()