from time import sleep, time

from src.actuator.motors import set_wheel_speeds

sleep(3)
set_wheel_speeds(0.5, 0.5)

