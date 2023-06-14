#!/usr/bin/python3

from smbus import SMBus
from time import sleep
import math

bus = SMBus(1)
ads7830_commands = (0x84, 0xc4, 0x94, 0xd4, 0xa4, 0xe4, 0xb4, 0xf4)

x1, y1 = (69, 90.0)
x2, y2 = (113, 71.0)
m = (y2 - y1) / (x2 - x1)

def reading_to_temp(reading):
    """Takes a value from 0-255 and tries to determine the temperature, based on two temperatures and readings"""
#    return (m * (reading - x1) + y1)
    voltage = float(reading) * 5 / 256
    resistance = 10.0 * voltage / (5 - voltage)
    tempK = 1 / (math.log(resistance / 10) / 3950 + 1 / (273.15 + 25))
    return convert_to_farenheit(tempK - 273.15)

def convert_to_farenheit(celcius):
    return float(celcius) * 9/5 + 32


def safe_exit(signum, frame):
    exit(1)

def read_ads7830(input):
    bus.write_byte(0x4b, ads7830_commands[input])
    return bus.read_byte(0x4b)

def read_min(input):
    while True:
        value = read_ads7830(input)

        yield (127-value)/127 if value < 110 else 0

def read_max(input):
    while True:
        value = read_ads7830(input)

        yield (value-128)/127 if value > 140 else 0

try:

    while True:
        reading = read_ads7830(7)
        print(f"reading: {reading}, temp={reading_to_temp(reading)}")
        sleep(.5)
    pause()

except KeyboardInterrupt:
    pass

finally:
    pass

