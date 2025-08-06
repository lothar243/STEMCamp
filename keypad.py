# Feel free to use this as a library (calling get_keypad_buttons)
# to get a list of buttons that are currently pressed.

import RPi.GPIO as GPIO
from time import sleep

GPIO.setmode(GPIO.BCM) # Use the GPIO pin numbers (instead of physical pin numbers)


def decode_key(col, row):
    """Given a column and row, return the character that is pressed"""
    keys = [
            ["1", "2", "3", "A"],
            ["4", "5", "6", "B"],
            ["7", "8", "9", "C"],
            ["*", "0", "#", "D"]
            ]
    return keys[row][col]

def get_keypad_buttons(col_pins, row_pins):
    """Read through each row/column to determine which buttons are currently pressed
    Returns a list of their characters"""
    pressed_buttons = []
    for row_num, row_pin in enumerate(row_pins):
        GPIO.setup(row_pin, GPIO.OUT)
        GPIO.output(row_pin, 0) # pull to ground
        for col_num, col_pin in enumerate(col_pins):
            GPIO.setup(col_pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
            if(GPIO.input(col_pin) == 0):
                pressed_buttons.append(decode_key(col_num, row_num))
        GPIO.setup(row_pin, GPIO.IN)
    return pressed_buttons

if __name__ == "__main__":
    # Example execution - this just prints what is pressed
    col_pins = [26, 19, 13, 6]
    row_pins = [21, 20, 16, 12]
    while True:
        pressed_buttons = get_keypad_buttons(col_pins, row_pins)
        if len(pressed_buttons) != 0:
            print(pressed_buttons)
        sleep(.2)