from gpiozero import DigitalOutputDevice as dod, Button
from time import sleep

col_pins = [Button(26), Button(19), Button(13), Button(6)]
row_pins = [dod(21), dod(20), dod(16), dod(12)]

def decode_key(col, row):
    if col == 0:
        if row == 0:
            return "1"
        if row == 1:
            return "4"
        if row == 2:
            return "7"
        if row == 3:
            return "*"
    if col == 1:
        if row == 0:
            return "2"
        if row == 1:
            return "5"
        if row == 2:
            return "8"
        if row == 3:
            return "0"
    if col == 2:
        if row == 0:
            return "3"
        if row == 1:
            return "6"
        if row == 2:
            return "9"
        if row == 3:
            return "#"
    if col == 3:
        if row == 0:
            return "A"
        if row == 1:
            return "B"
        if row == 2:
            return "C"
        if row == 3:
            return "D"

def get_keypad_button(col_pins, row_pins):
    for row_num, row_pin in enumerate(row_pins):
        row_pin.off()
        for col_num, col_pin in enumerate(col_pins):
            if(col_pin.is_pressed):
                print(decode_key(col_num, row_num))
        row_pin.on()

while True:
    get_keypad_button(col_pins, row_pins)
    sleep(.2)