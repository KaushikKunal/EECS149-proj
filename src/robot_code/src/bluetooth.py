import machine
import time

# Configure UART  
uart = machine.UART(0, 9600)
uart.write("Starting BLE UART connection")


"""UP: 516 507
DOWN: 615 606
LEFT:714 705
RIGHT:813 804
1: 11: 10;
2: 219 20:
3: 318 309
4: 417 408"""

commands = {"up": False, "down": False, "left": False, "right": False, "1": False, "2": False, "3": False, "4": False}
down_blueooth_messages = {"516": "up", "615": "down", "714": "left", "813": "right", "11": "1", "219": "2", "318": "3", "417": "4"}
up_blueooth_messages =   {"507": "up", "606": "down", "705": "left", "804": "right", "10": "1",  "20": "2", "309": "3", "408": "4"}

def get_bluetooth_commands():
    if uart.any():
        data = uart.read()  
        uart.write("Received: " + str(data))

        # check for down presses
        for down_msg in down_blueooth_messages:
            if down_msg in data:
                down_cmd = down_blueooth_messages[down_msg]
                commands[down_cmd] = True
        
        # check for up presses
        for up_msg in up_blueooth_messages:
            if up_msg in data:
                up_cmd = up_blueooth_messages[up_msg]
                commands[up_cmd] = False
        
    return commands