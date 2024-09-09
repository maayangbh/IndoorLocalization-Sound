from sound_localization.tdoa import TimeDifferenceOfArrival
import math

class CalibrationSpeedOfSound(object):
    def __init__(self, sample_frequency=2e6, time_scale=1e3):
        self.tdoa = TimeDifferenceOfArrival(sample_frequency, time_scale)
        self.distance_delta = math.sqrt(2*(100**2)) - 100
    
    def calc_speed_of_sound(self, t1, t2):
        time_delta1 = self.tdoa.time_delta_1d(t1, t2)
        return self.distance_delta / time_delta1

