import RPi.GPIO as GPIO
import time

# GPIO pin setup (modify these based on your actual wiring)
ROW_PINS = [5, 6, 13, 19]    # R1, R2, R3, R4
COL_PINS = [12, 16, 20, 21]  # C1, C2, C3, C4

# Define keypad layout
KEYPAD = [
    ['1', '2', '3', 'A'],
    ['4', '5', '6', 'B'],
    ['7', '8', '9', 'C'],
    ['*', '0', '#', 'D']
]

def setup():
    GPIO.setmode(GPIO.BCM)
    # Set columns as input with pull-up
    for col in COL_PINS:
        GPIO.setup(col, GPIO.IN, pull_up_down=GPIO.PUD_UP)
    # Set rows as output and default them to HIGH
    for row in ROW_PINS:
        GPIO.setup(row, GPIO.OUT)
        GPIO.output(row, GPIO.HIGH)

def scan_keypad():
    for i, row_pin in enumerate(ROW_PINS):
        GPIO.output(row_pin, GPIO.LOW)
        for j, col_pin in enumerate(COL_PINS):
            if GPIO.input(col_pin) == GPIO.LOW:
                # Wait for key release
                while GPIO.input(col_pin) == GPIO.LOW:
                    time.sleep(0.01)
                GPIO.output(row_pin, GPIO.HIGH)
                return KEYPAD[i][j]
        GPIO.output(row_pin, GPIO.HIGH)
    return None

try:
    setup()
    print("Press a key on the keypad:")
    while True:
        key = scan_keypad()
        if key:
            print(f"Key Pressed: {key}")
        time.sleep(0.1)

except KeyboardInterrupt:
    print("\nExiting...")
finally:
    GPIO.cleanup()

