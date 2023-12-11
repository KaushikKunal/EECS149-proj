import machine
import time

# Configure UART  
uart = machine.UART(0, 9600)
# uart.init(9600, bits=8, parity=None, stop=1)  
# uart = machine.UART(0, baudrate=9600)
# tx_pin = machine.Pin(0, machine.Pin.IN)  # Assuming TX is on GP0 (pin 0)
uart.write("Hello from the other side")

print("LISTENING FOR BLUETOOTH")

while True:
    # Check if data is available
    
    if uart.any():
        # Read all available data 
        data = uart.read()  
        
        # Print message  
        print(data)
    time.sleep_ms(50)

# while True:
#     data = uart.read()
#     if data:
#         print("Received:", data)

#     # Small delay
#     time.sleep_ms(50)