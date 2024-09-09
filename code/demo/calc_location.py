import sys
sys.path.insert(0, 'C:\\Users\\maaya\\OneDrive\\Desktop\\study\\finalProject\\Final Project\\code')

import process
import matplotlib.pyplot as plt
import pandas as pd
from sound_localization.tdoa import TimeDifferenceOfArrival
from sound_localization.triangulation import Triangulation
import calibration

def calculate_location():
    data_frame = pd.read_csv('.\\Raw Data\\recordings\\default.csv', header=None)
    signal1, signal2 = process.process(data_frame)
    tdoa = TimeDifferenceOfArrival(sample_frequency=process.SAMPLE_FREQUENCY)
    time_delta = tdoa.time_delta_1d(signal1, signal2)
    #speed_of_sound = calibration.calibrate_speed_of_sound()
    speed_of_sound = 35
    triang = Triangulation(height=process.HEIGHT, bounds=[process.HEIGHT, process.HEIGHT], speed_of_sound=speed_of_sound)
    x = triang.location_1d(time_delta)
    print("Time deltas: {} ms".format(time_delta))
    print("Coordinates: ({})".format(x))

if __name__ == "__main__":
    calculate_location()