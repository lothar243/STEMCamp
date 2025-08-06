from gpiozero import LED
from time import sleep

digit_pins = [26, 19, 13, 6]
segment_pins = [5, 22, 27, 17, 4, 21, 20, 16]

digits = [LED(digit) for digit in digit_pins]
segments = [LED(segment, active_high=False) for segment in segment_pins]

digits[0].on()
segments[0].on()
segments[1].on()

number_encodings = {
        "1": 0b00000110,
        "2": 0b01011011,
        "3": 0b01001111,
        "4": 0b01100110,
        "5": 0b01101101,
        "6": 0b01111101,
        "7": 0b00000111,
        "8": 0b01111111,
        "9": 0b01101111,
        "0": 0b00111111
        }

def display_value(value):
    for index, character in enumerate(value):
        digits[index].on()
        for segment_num in range(8):
            if 2**segment_num & number_encodings[character] > 0:
                segments[segment_num].on()
            else:
                segments[segment_num].off()
        sleep(.002)
        digits[index].off()


if __name__ == "__main__":
    while True:
        display_value("5609")