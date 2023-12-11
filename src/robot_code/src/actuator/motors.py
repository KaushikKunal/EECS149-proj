from pololu_3pi_2040_robot import robot
from time import sleep, time

motors = robot.Motors()
kp = 0.1  # Adjust proportional gain based on your system
ki = 0.01  # Adjust integral gain based on your system
kd = 0.01  # Adjust derivative gain based on your system
left_integral = 0
right_integral = 0
left_prev_error = 0
right_prev_error = 0

# sets L/R wheel speeds in m/s
def set_wheel_speeds(left_wheel_speed, right_wheel_speed, cur_left_wheel_speed=None, cur_right_wheel_speed=None):
    
    # PID feedback if previous speed is given
    if (cur_left_wheel_speed is not None and cur_right_wheel_speed is not None):
        global left_integral, right_integral, left_prev_error, right_prev_error
        left_error = left_wheel_speed - cur_left_wheel_speed
        right_error = right_wheel_speed - cur_right_wheel_speed

        left_integral = left_integral + left_error
        right_integral = right_integral + right_error

        left_derivative = left_error - left_prev_error
        right_derivative = right_error - right_prev_error

        left_prev_error = left_error
        right_prev_error = right_error

        left_motor_speed = kp*left_error + ki*left_integral + kd*left_derivative
        right_motor_speed = kp*right_error + ki*right_integral + kd*right_derivative

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
        