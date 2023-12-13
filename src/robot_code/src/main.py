from pololu_3pi_2040_robot import robot
from time import sleep, time, time_ns


from src.sensor.encoders import get_wheel_dists
from src.sensor.potentiometers import get_pot_angles, calibrate_pot
# from src.sensor.imu import get_imu_data
from src.bluetooth import get_bluetooth_commands, send_bluetooth_message
from src.actuator.motors import set_wheel_speeds
from src.actuator.buzzer import play_fatal_sound
# from src.controller.reversing_controller import 

MAIN_LOOP_FREQ = 50  # Hz
PRINT_FREQ = 1  # Hz
ASSISTED_MODE = True
DRIVING_MODE = "forwards"  # or "reversing"


yellow_led = robot.YellowLED()

buttonA = robot.ButtonA()
buttonB = robot.ButtonB()
buttonC = robot.ButtonC()

# TODO
def change_driving_mode():
    global DRIVING_MODE
    if (DRIVING_MODE == "forwards"):
        DRIVING_MODE = "reversing"
    elif (DRIVING_MODE == "reversing"):
        DRIVING_MODE = "forwards"
    else:
        error("invalid driving mode", fatal=True)

def error(msg, fatal=False):
    print("ERROR: " + msg)
    yellow_led.on()
    if (fatal):
        # play_fatal_sound()
        exit()


def main():
    # calibrate_pot()
    prev_left_wheel_dist, prev_right_wheel_dist = get_wheel_dists()
    i = 0
    while True:
        start_time = time_ns()

        # read sensors
        left_wheel_dist, right_wheel_dist = get_wheel_dists()
        # print("L/R dists (m): {}, {}".format(left_wheel_dist, right_wheel_dist))
        left_wheel_vel = (left_wheel_dist - prev_left_wheel_dist) * MAIN_LOOP_FREQ
        right_wheel_vel = (right_wheel_dist - prev_right_wheel_dist) * MAIN_LOOP_FREQ
        prev_left_wheel_dist, prev_right_wheel_dist = left_wheel_dist, right_wheel_dist
        pololu_pot_angle, hitch_pot_angle = get_pot_angles(radians=True)
        # pololu_pot_angle, hitch_pot_angle = get_pot_angles(radians=False)
        # pololu_pot_angle, hitch_pot_angle = 0, 0
        
        global ASSISTED_MODE, DRIVING_MODE
        # read bluetooth commands
        commands = get_bluetooth_commands()
        if (commands["up"]):
            DRIVING_MODE = "forwards"
        elif (commands["down"]):
            DRIVING_MODE = "reversing"
        else:
            DRIVING_MODE = "halt"

        if (commands["1"] and not ASSISTED_MODE):
            ASSISTED_MODE = True
            send_bluetooth_message("ASSISTED MODE ON\n")
        elif (commands["2"] and ASSISTED_MODE):
            ASSISTED_MODE = False
            send_bluetooth_message("ASSISTED MODE OFF\n")
        
        if(i % int(MAIN_LOOP_FREQ/PRINT_FREQ) == 0):
            print("L/R vels (m/s): {}, {}".format(left_wheel_vel, right_wheel_vel))
            print("Pololu/hitch angles (rad): {}, {}".format(pololu_pot_angle, hitch_pot_angle))
            print("commands:", commands)
        
        if ASSISTED_MODE:
            if DRIVING_MODE == "forwards":

                left_motor_speed =  0.3
                right_motor_speed = 0.3

                radius = 0.085396 # meters
                desired_angle = 0
                ang_error = desired_angle - abs(pololu_pot_angle)
                
                if (commands["left"]):
                    left_motor_speed = left_motor_speed + radius * ang_error
                    right_motor_speed = right_motor_speed - radius * ang_error
                if (commands["right"]):
                    left_motor_speed = left_motor_speed + radius * -ang_error
                    right_motor_speed = right_motor_speed - radius * -ang_error

            elif DRIVING_MODE == "reversing":

                radius = 0.085396 # meters
                desired_angle = 0
                ang_error = desired_angle - abs(pololu_pot_angle)

                left_motor_speed =  -0.3
                right_motor_speed = -0.3
                if (commands["left"]):
                    left_motor_speed = left_motor_speed + radius * ang_error
                    right_motor_speed = right_motor_speed - radius * ang_error
                if (commands["right"]):
                    left_motor_speed = left_motor_speed + radius * -ang_error  
                    right_motor_speed = right_motor_speed - radius * -ang_error

            elif DRIVING_MODE == "halt":
                left_motor_speed =  0
                right_motor_speed = 0
            # actuate motors with feedback
            set_wheel_speeds(left_motor_speed, right_motor_speed, left_wheel_vel, right_wheel_vel)
        else:
            # unasisted mode
            if DRIVING_MODE == "forwards":
                left_motor_speed =  0.3
                right_motor_speed = 0.3
            elif DRIVING_MODE == "reversing":
                left_motor_speed =  -0.3
                right_motor_speed = -0.3
            elif DRIVING_MODE == "halt":
                left_motor_speed =  0
                right_motor_speed = 0
            if (commands["left"]):
                right_motor_speed *= 1.5
            if (commands["right"]):
                left_motor_speed *= 1.5
            
            set_wheel_speeds(left_motor_speed, right_motor_speed)  # without feedback

        # fix loop frequency
        end_time = time_ns()
        loop_time = (end_time - start_time)/1000000000  # in seconds
        if(i % int(MAIN_LOOP_FREQ/PRINT_FREQ) == 0):
            print("loop time: {} ms".format(loop_time * 1000))
        if (loop_time < 1/MAIN_LOOP_FREQ):
            sleep(1/MAIN_LOOP_FREQ - loop_time)
        else:
            print("throttling loop frequency by {} ms".format((loop_time - 1/MAIN_LOOP_FREQ)*1000))
        i += 1
main()