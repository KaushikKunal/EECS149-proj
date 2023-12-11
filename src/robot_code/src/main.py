from pololu_3pi_2040_robot import robot
from time import sleep, time


from src.sensor.encoders import get_wheel_dists
from src.sensor.potentiometers import get_pot_angles, calibrate_pot
from src.actuator.motors import set_wheel_speeds
from src.actuator.buzzer import play_fatal_sound
# from controller.

MAIN_LOOP_FREQ = 5  # Hz  TODO CHANGE TO HIGHER VALUE
DRIVING_MODE = "forwards"  # or "reversing"


yellow_led = robot.YellowLED()
imu = robot.IMU()

buttonA = robot.ButtonA()
buttonB = robot.ButtonB()
buttonC = robot.ButtonC()

def error(msg, fatal=False):
    print("ERROR: " + msg)
    yellow_led.on()
    if (fatal):
        play_fatal_sound()
        exit()


def main():
    prev_left_wheel_dist, prev_right_wheel_dist = get_wheel_dists()
    while True:
        start_time = time()

        # read sensors
        left_wheel_dist, right_wheel_dist = get_wheel_dists()
        print("L/R dists (m): {}, {}".format(left_wheel_dist, right_wheel_dist))
        left_wheel_vel = (left_wheel_dist - prev_left_wheel_dist) * MAIN_LOOP_FREQ
        right_wheel_vel = (right_wheel_dist - prev_right_wheel_dist) * MAIN_LOOP_FREQ
        prev_left_wheel_dist, prev_right_wheel_dist = left_wheel_dist, right_wheel_dist
        pololu_pot_angle, hitch_pot_angle = get_pot_angles(radians=True)

        print("L/R vels (m/s): {}, {}".format(left_wheel_vel, right_wheel_vel))
        # print("Pololu/hitch angles (rad): {}, {}".format(pololu_pot_angle, hitch_pot_angle))

        # pass sensor values to controller
        # TODO

        # INPUT TO CONTROLLER
        # pololu_pot_angle
        # hitch_pot_angle
        # 

        # OUTPUT FROM CONTROLLER
        left_motor_speed =  0.1
        right_motor_speed = 0.1

        
        # actuate motors with feedback
        set_wheel_speeds(left_motor_speed, right_motor_speed, left_wheel_vel, right_wheel_vel)

            

        # fix loop frequency
        end_time = time()
        loop_time = end_time - start_time
        if (loop_time < 1/MAIN_LOOP_FREQ):
            sleep(1/MAIN_LOOP_FREQ - loop_time)
            
main()