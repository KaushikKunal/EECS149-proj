from machine import ADC
from time import sleep



def convert_signal_to_degrees(u16_signal):
    conversion_factor = 3.3 / (65535)
    voltage =  u16_signal * conversion_factor
    degrees = voltage/3.3 * 210  # 210 degrees is the range of the potentiometer
    degrees -= 105  # 105 degrees is the center of the potentiometer
    return degrees
    

# create a PIN object to read the potentiometer from GPIO 27
print("reading potentiometer...")
while True:
    pot = ADC(27)
    print("{} degrees".format(convert_signal_to_degrees(pot.read_u16())))
    sleep(0.1) 