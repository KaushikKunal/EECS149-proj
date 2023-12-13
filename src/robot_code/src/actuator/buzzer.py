from pololu_3pi_2040_robot import robot
from time import sleep

buzzer = robot.Buzzer()

def play_fatal_sound():
    buzzer.play_in_background('<g-8r8<g-8r8<g-8')  # error sound
    # sleep(1)