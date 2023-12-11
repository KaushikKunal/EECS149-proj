from machine import ADC, Pin
from math import sqrt, pi
from pololu_3pi_2040_robot import robot
from time import sleep

# --------------- #
# ---MAIN CODE--- #
# --------------- #

HITCH_POT_PIN = 28  # GPIO pin of hitch potentiometer
POLOLU_POT_PIN = 27  # GPIO pin of pololu potentiometer

HITCH_ADC = ADC(HITCH_POT_PIN)
POLOLU_ADC = ADC(POLOLU_POT_PIN)

# returns angle of pololu potentiometer in degrees
def get_pololu_pot_angle():
    # # tunable params
    # max_pololu_pot_angle = 210
    # straight_voltage = 1.65  # volts when pololu is straight

    # u16_val = POLOLU_ADC.read_u16()
    # voltage = u16_val/65535 * 3.3 - straight_voltage
    # angle = voltage/3.3 * max_pololu_pot_angle

    # tunable params
    min_u16_val = 0
    max_u16_val = 65535
    min_angle = -105
    max_angle = 105

    u16_val = HITCH_ADC.read_u16()
    angle = (u16_val - min_u16_val)/(max_u16_val - min_u16_val) * (max_angle - min_angle) + min_angle
    return angle

# returns angle of hitch potentiometer in degrees
def get_hitch_pot_angle():
    # tunable params
    min_u16_val = 0
    max_u16_val = 65535
    min_angle = -105
    max_angle = 105

    u16_val = HITCH_ADC.read_u16()
    angle = (u16_val - min_u16_val)/(max_u16_val - min_u16_val) * (max_angle - min_angle) + min_angle
    return angle

# returns tuple of (pololu angle, hitch angle)
def get_pot_angles(radians=False):
    pololu_angle = get_pololu_pot_angle()
    hitch_angle = get_hitch_pot_angle()

    if (radians):# convert degrees to radians
        pololu_angle = pololu_angle * pi/180
        hitch_angle = hitch_angle * pi/180
    
    return pololu_angle, hitch_angle

# ---------------------- #
# ---CALIBRATION CODE--- #
# ---------------------- #

CAL_POT_PIN = 27  # GPIO pin of potentiometer to calibrate
NUM_READINGS = 1000
READING_FREQ = 100  # Hz

buttonB = robot.ButtonB()

def get_average_reading(adc):
    total = 0
    squared_diff_sum = 0
    for _ in range(NUM_READINGS):
        reading = adc.read_u16()
        total += reading
        squared_diff_sum += reading ** 2
        sleep(1 / READING_FREQ)

    mean = total / NUM_READINGS
    std = sqrt((squared_diff_sum / NUM_READINGS) - (mean ** 2))

    return mean, std

# prints raw readings from potentiometer
def calibrate_pot():
    adc = ADC(CAL_POT_PIN)
    while True:
        # wait until B pressed
        print("set potentiometer to desired angle, then press B")
        while not buttonB.check():
            pass

        # take readings and print
        average, std_dev = get_average_reading(adc)
        print("average: {}, std: {}".format(average, std_dev))