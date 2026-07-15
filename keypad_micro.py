# keypad.py
# MicroPython version
#
# Feel free to use this as a library by calling get_keypad_buttons()
# to get a list of buttons that are currently pressed.

from machine import Pin
from time import sleep


def decode_key(col, row):
    """Given a column and row, return the character that is pressed."""
    keys = [
        ["1", "2", "3", "A"],
        ["4", "5", "6", "B"],
        ["7", "8", "9", "C"],
        ["*", "0", "#", "D"],
    ]
    return keys[row][col]


def get_keypad_buttons(col_gpio, row_gpio):
    """
    Read through each row/column to determine which buttons are currently pressed.

    col_gpio and row_gpio should be lists of GPIO pin numbers.

    Returns a list of pressed button characters.
    """
    pressed_buttons = []

    # Set all rows to inputs first so only one row is driven at a time
    rows = [Pin(pin, Pin.IN) for pin in row_gpio]

    # Columns use internal pull-ups
    cols = [Pin(pin, Pin.IN, Pin.PULL_UP) for pin in col_gpio]

    for row_num, row_pin_num in enumerate(row_gpio):
        # Drive this row low
        row = Pin(row_pin_num, Pin.OUT)
        row.value(0)

        # Check each column
        for col_num, col in enumerate(cols):
            if col.value() == 0:
                pressed_buttons.append(decode_key(col_num, row_num))

        # Return row to high-impedance input mode
        rows[row_num] = Pin(row_pin_num, Pin.IN)

    return pressed_buttons


if __name__ == "__main__":
    # Example execution - this just prints what is pressed.
    #
    # These are GPIO numbers, not physical pin numbers.
    # Adjust them for your MicroPython board.
    col_gpio = [0, 1, 2, 3]
    row_gpio = [4, 5, 6, 7]

    while True:
        pressed_buttons = get_keypad_buttons(col_gpio, row_gpio)

        if len(pressed_buttons) != 0:
            print(pressed_buttons)

        sleep(0.2)