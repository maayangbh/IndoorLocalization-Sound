#!/usr/bin/python3 
import numpy as np
from scipy import signal
from tdoa import TimeDifferenceOfArrival
from triangulation import Triangulation
from calibration import CalibrationSpeedOfSound
from Code.Experiments.plot import plottingSignal
from envelope import create_envelope
import time

SAMPLE_FREQUENCY = 2e6  # 2 MHz
SAMPLE_DURATION = 0.1 # 1 sec
CHIRP_DURATION = 5e-3  # 5 ms
CHIRP_FREQUENCY1 = 100e3  # 100 kHz
CHIRP_FREQUENCY2 = 110e3  # 110 kHz

TIME_SHIFT = 1e-3  # 1 ms
SAMPLE_SHIFT = int(TIME_SHIFT * SAMPLE_FREQUENCY)

HEIGHT = 200 # cm

def Get_envelope(interpolated_data):
    """
    Calculates the envelope of the interpolated data.
    """
    peaks, _ = find_peaks(interpolated_data.squeeze(), height=0) # find the peaks (above 0) in the interpolated data
    troughs, _ = find_peaks(-interpolated_data.squeeze())        # find the troughts in the interpolated data

    #Fit suitable models to the data. Here I am using cubic splines.
    u_p = interp1d(peaks, interpolated_data.squeeze()[peaks], kind='cubic', bounds_error=False, fill_value=0.0)
    l_p = interp1d(troughs, interpolated_data.squeeze()[troughs], kind='cubic', bounds_error=False, fill_value=0.0)
    Upper_envelope = [u_p(i) for i in range(interpolated_data.shape[0])]
    Lower_envelope = [l_p(i) for i in range(interpolated_data.shape[0])]

    return peaks, troughs, Upper_envelope, Lower_envelope

def main():
    t1 = np.zeros(int(SAMPLE_DURATION * SAMPLE_FREQUENCY))
    t2 = np.zeros(int(SAMPLE_DURATION * SAMPLE_FREQUENCY))
    t3 = np.zeros(int(SAMPLE_DURATION * SAMPLE_FREQUENCY))
    
    # Create the chirp signal
    t = np.linspace(0, CHIRP_DURATION, int(CHIRP_DURATION * SAMPLE_FREQUENCY), endpoint=False)
    chirp_signal = signal.chirp(t, f0=CHIRP_FREQUENCY1, f1=CHIRP_FREQUENCY2, t1=CHIRP_DURATION)
    
    # Put chirp_signal in the middle of t1
    middle_index = len(t1) // 2
    t1[middle_index - len(chirp_signal)//2 : middle_index + len(chirp_signal)//2] = chirp_signal
    
    # Put chirp_signal 1 ms shifted from the middle of t2
    t2[middle_index - len(chirp_signal)//2 + SAMPLE_SHIFT : middle_index + len(chirp_signal)//2 + SAMPLE_SHIFT] = chirp_signal
    
    t3 = t1.copy()
    
    # add a little noise to t1 and t2
    t1 += np.random.normal(0, 1, len(t1))
    t2 += np.random.normal(0, 1, len(t2))
    t3 += np.random.normal(0, 1, len(t3))

    plotting = plottingSignal(SAMPLE_FREQUENCY)
    plotting.plot_three_signals(t1, t2, t3)


    t1 = t1.astype(np.float32)
    t2 = t2.astype(np.float32)
    t3 = t3.astype(np.float32)

    # *************************
    # Caliberate Speed Of Light
    # *************************

    calibration = CalibrationSpeedOfSound(chirp_signal, SAMPLE_FREQUENCY, 1e3)
    speed_of_sound = calibration.calc_speed_of_sound(t1, t2, t3)
    print("speed of light: {} cm/ms".format(speed_of_sound))


    # ************************
    # Calculate the time delta
    # ************************
    start = time.time()
    tdoa = TimeDifferenceOfArrival(chirp_signal, SAMPLE_FREQUENCY, 1e3)
    time_delta1, time_delta2 = tdoa.time_delta_2d(t1, t2, t3)
    mid = time.time()
    
    # ****************************
    # Calculate Location of signal
    # ****************************
    triang = Triangulation(height=HEIGHT, bounds=[200, 200])
    x, y = triang.location_2d(time_delta1, time_delta2)
    end = time.time()
    
    print("Time delta calculation time: {} s".format(mid - start))
    print("Location calculation time: {} s".format(end - mid))
    print("Total time: {} s".format(end - start))
    
    print("Time deltas: {} ms, {} ms".format(time_delta1, time_delta2))
    print("Coordinates: ({}, {})".format(x, y))
    
if __name__ == "__main__":
    main()