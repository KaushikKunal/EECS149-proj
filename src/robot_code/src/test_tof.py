from machine import SoftI2C, Pin
from src.sensor.vl53l1x import VL53L1X
import time
i2c = SoftI2C(scl=Pin(5), sda=Pin(4), freq=100_000)
distance = VL53L1X(i2c)
while True:
    print("range: mm ", distance.read())
    time.sleep_ms(50)