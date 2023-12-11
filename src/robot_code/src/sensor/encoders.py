from pololu_3pi_2040_robot import robot
from math import pi

CPR = 12 * 29.86  # counts per revolution, accounting for gear ratio
WHEEL_DIAMETER = 0.032  # meters

encoders = robot.Encoders()

# returns tuple of (left wheel dist, right wheel dist) in meters
def get_wheel_dists():
    c = encoders.get_counts()
    # using datasheet values, WHICH SUX
    # left_dist =  c[0]/CPR * WHEEL_DIAMETER * pi
    # right_dist = c[1]/CPR * WHEEL_DIAMETER * pi

    # using calibration values (done using a 30cm ruler)
    left_dist =  (c[0]/1000)*0.3
    right_dist = (c[1]/1000)*0.3

    return left_dist, right_dist