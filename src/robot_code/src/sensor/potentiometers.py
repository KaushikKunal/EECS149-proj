from machine import ADC, Pin
from math import sqrt, pi
from pololu_3pi_2040_robot import robot
from time import sleep, time_ns

# --------------- #
# ---MAIN CODE--- #
# --------------- #

HITCH_POT_PIN = 28  # GPIO pin of hitch potentiometer
POLOLU_POT_PIN = 27  # GPIO pin of pololu potentiometer

HITCH_ADC = ADC(HITCH_POT_PIN)
POLOLU_ADC = ADC(POLOLU_POT_PIN)

hitch_ma = 0
pololu_ma = 0

# moving average params
hitch_ma_n = 1
pololu_ma_n = 1

# instantaneous average params
inst_pololu_avg_n = 25
inst_hitch_avg_n = 25

# returns angle of pololu potentiometer in degrees
def get_pololu_pot_angle():
    # tunable params
    min_u16_val = 61610
    max_u16_val = 62374
    min_angle = -45
    max_angle = 45
    reverse = 1
    manual_offset = 0

    global pololu_ma
    # take multiple readings and average
    inst_sum = 0
    for _ in range(inst_pololu_avg_n):
        u16_val = POLOLU_ADC.read_u16()
        angle = (u16_val - min_u16_val)/(max_u16_val - min_u16_val) * (max_angle - min_angle) + min_angle
        inst_sum += angle * reverse
    inst_avg = inst_sum / inst_pololu_avg_n + manual_offset
    pololu_ma = (pololu_ma * (pololu_ma_n - 1) + inst_avg) / pololu_ma_n
    # print("sensor reading time (ms):", (end_time - start_time)/1000000)
    return pololu_ma

# returns angle of hitch potentiometer in degrees
def get_hitch_pot_angle():
    # tunable params
    min_u16_val = 20400
    max_u16_val = 48463
    min_angle = -60
    max_angle = 60
    reverse = 1
    manual_offset = 0

    global hitch_ma
    # take multiple readings and average
    inst_sum = 0
    for _ in range(inst_hitch_avg_n):
        u16_val = HITCH_ADC.read_u16()
        angle = (u16_val - min_u16_val)/(max_u16_val - min_u16_val) * (max_angle - min_angle) + min_angle
        inst_sum += angle * reverse
    inst_avg = inst_sum / inst_hitch_avg_n + manual_offset
    hitch_ma = (hitch_ma * (hitch_ma_n - 1) + inst_avg) / hitch_ma_n
    return hitch_ma

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

CAL_POT_PIN = 28  # GPIO pin of potentiometer to calibrate
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
        print("calculating...")
        average, std_dev = get_average_reading(adc)
        print("average: {}, std: {}".format(average, std_dev))