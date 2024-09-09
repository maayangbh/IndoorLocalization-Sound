import sys
sys.path.insert(0, 'C:\\Users\\maaya\\OneDrive\\Desktop\\study\\finalProject\\Final Project\\code')

import process
import pandas as pd
from sound_localization.calibration import CalibrationSpeedOfSound


def calibrate_speed_of_sound():
    calibration_data_frame = pd.read_csv('.\\Raw Data\\recordings\\demoside.csv', header=None)    
    calibration_channel1, calibration_channel2 = process.initial_process(calibration_data_frame, int(process.SAMPLES_PER_PERIOD * 2))
    calibration = CalibrationSpeedOfSound(process.SAMPLE_FREQUENCY, 1e3)
    speed_of_sound = calibration.calc_speed_of_sound(calibration_channel1, calibration_channel2)
    print("speed of sound: {} cm/ms".format(speed_of_sound))
    return speed_of_sound

if __name__ == "__main__":
    calibrate_speed_of_sound()