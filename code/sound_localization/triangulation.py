from sympy import Symbol, nsolve

SPEED_OF_SOUND = 34.3 # cm/ms

class Triangulation:
    def __init__(self, height, bounds=[], speed_of_sound = SPEED_OF_SOUND):
        self.height = height
        self.bounds = bounds
        self.speed_of_sound = speed_of_sound     
        self.initial_guess = [i / 2 for i in bounds]   
    
    def location_1d(self, time_delta):
        if len(self.bounds) < 1:
            raise Exception("Bounds dimensions must be greater than 0")
        delta_d = time_delta * self.speed_of_sound
        x = Symbol('x')
        z_0 = self.height
        x_0 = self.bounds[0]
        eq = ((z_0) ** 2 + (x_0 - x) ** 2) ** 0.5 - ((z_0) ** 2 + (x) ** 2) ** 0.5 - delta_d
        res = nsolve(eq, x, self.initial_guess[0])
        self.initial_guess[0] = res
        return res

    def location_2d(self, time_delta_1, time_delta_2):
        if len(self.bounds) < 2:
            raise Exception("Bounds dimensions must be greater than 1")
        x, y = Symbol('x'), Symbol('y')
        z_0 = self.height
        x_0 = self.bounds[0]
        y_0 = self.bounds[1]
        delta_d_1 = time_delta_1 * self.speed_of_sound
        delta_d_2 = time_delta_2 * self.speed_of_sound
        eq1 = ((z_0) ** 2 + (x_0 - x) ** 2 + y ** 2) ** 0.5 - ((z_0) ** 2 + (x) ** 2 + (y) ** 2) ** 0.5 - delta_d_1
        eq2 = ((z_0) ** 2 + x ** 2 + (y_0 - y) ** 2) ** 0.5 - ((z_0) ** 2 + (x) ** 2 + (y) ** 2) ** 0.5 - delta_d_2
        res = nsolve((eq1, eq2), (x, y), (self.initial_guess[0], self.initial_guess[1]))
        self.initial_guess[0], self.initial_guess[1] = res
        return res
