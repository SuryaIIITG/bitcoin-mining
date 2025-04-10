import mraa
import time

# Manually initialize GPIO by specifying the pin number
data_pin = mraa.Gpio(73)  # GPIO4_C2 (check your board's GPIO mapping)
clock_pin = mraa.Gpio(74)  # GPIO4_C6

# Set pin direction
data_pin.dir(mraa.DIR_OUT)
clock_pin.dir(mraa.DIR_OUT)

# Function to send a single bit
def send_bit(bit):
    data_pin.write(bit)  # Write bit to data pin
    clock_pin.write(1)  # Clock high
    time.sleep(0.001)  # Small delay
    clock_pin.write(0)  # Clock low

# 255-bit data to send (example pattern: 255 '1's)
data_to_send = [1] * 255  # Replace with your desired bit pattern

# Sending the data
for bit in data_to_send:
    send_bit(bit)

print("255-bit data sent successfully!")

# Function to read back the sent data
def read_data():
    received_data = []
    for _ in range(255):
        clock_pin.write(1)  # Clock high
        time.sleep(0.001)  # Small delay
        bit = data_pin.read()  # Read data bit
        received_data.append(bit)
        clock_pin.write(0)  # Clock low
    return received_data

# Reading the sent data
received_data = read_data()
print("Received Data:", received_data)

