from pololu_3pi_2040_robot import robot
from time import sleep, time

FEEDBACK_GAIN = 0.3  # change this
motors = robot.Motors()

# sets L/R wheel speeds in m/s
def set_wheel_speeds(left_wheel_speed, right_wheel_speed, cur_left_wheel_speed=None, cur_right_wheel_speed=None):
    
    # feedback if previous speed is given
    if (cur_left_wheel_speed is not None and cur_right_wheel_speed is not None):
        left_wheel_speed += FEEDBACK_GAIN * (left_wheel_speed - cur_left_wheel_speed)
        right_wheel_speed += FEEDBACK_GAIN * (right_wheel_speed - cur_right_wheel_speed)

    # convert wheel speeds to motor speeds
    left_motor_speed = left_wheel_speed * motors.MAX_SPEED/1.5
    right_motor_speed = right_wheel_speed * motors.MAX_SPEED/1.5

    # cap speeds
    if (abs(left_motor_speed) > motors.MAX_SPEED):
        # error("left motor speed too high", fatal=False)
        print("left motor speed too high")
        left_motor_speed = motors.MAX_SPEED * left_motor_speed/abs(left_motor_speed)

    if (abs(right_motor_speed) > motors.MAX_SPEED):
        # error("right motor speed too high", fatal=False)
        print("right motor speed too high")
        right_motor_speed = motors.MAX_SPEED * right_motor_speed/abs(right_motor_speed)
    motors.set_speeds(left_motor_speed, right_motor_speed)
        