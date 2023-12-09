print("running test_encoder.py")
# Displays encoder counts on the screen and blinks the yellow LED with
# each tick.

from pololu_3pi_2040_robot import robot
from time import sleep

led = robot.YellowLED()
encoders = robot.Encoders()
display = robot.Display()
buttonB = robot.ButtonB()

while True:
    c = encoders.get_counts()

    # change LED on every count
    led((c[0] + c[1]) % 2)

    print("Left: "+str(c[0]))
    print("Right: "+str(c[1]))
    print("\n")
    
    sleep(0.1)

    if buttonB.check():
        encoders.get_counts(reset = True)