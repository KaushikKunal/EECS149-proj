from pololu_3pi_2040_robot import robot

battery = robot.Battery()
led = robot.YellowLED()
buttonB = robot.ButtonB()

"""
 TODO:
    Run motors
    import other files
    workflow between mictrocontroller and local files
    test classes/oop?
    importing packages from online
    test encoders/potentiometer
    
"""
print("battery: {} mV".format(battery.get_level_millivolts()))
print("press B to run :D")

# wait until B pressed
while not buttonB.check():
    pass
print("RUNNING...")
import src.test_encoder  # replace this with the file to run