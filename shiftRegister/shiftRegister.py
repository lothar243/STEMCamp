import RPi.GPIO as GPIO
import time

# GPIO pin configuration
SER = 5     # Serial data input
RCLK = 26    # Register (latch) clock
SRCLK = 19   # Shift register clock

# Setup
GPIO.setmode(GPIO.BCM)
GPIO.setup([SER, SRCLK, RCLK], GPIO.OUT)

def shift_out(byte):
    """Send a byte to the 74HC595 shift register"""
    GPIO.output(RCLK, GPIO.LOW)  # Latch low to start
    for i in range(7, -1, -1):   # MSB first
        GPIO.output(SRCLK, GPIO.LOW)
        GPIO.output(SER, (byte >> i) & 0x01)
        GPIO.output(SRCLK, GPIO.HIGH)  # Shift on rising edge
    GPIO.output(RCLK, GPIO.HIGH)       # Latch data

if __name__ == "__main__":
    num = input("Enter a number between 0 and 255 (q to exit): ")
    while num != "q":
        try:
            value = int(num)
            shift_out(value)
        except:
            print("Error reading input")
        num = input("Enter a number between 0 and 255 (q to exit): ")

    shift_out(0)  # Turn off LEDs
    GPIO.cleanup()



