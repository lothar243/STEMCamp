#!/usr/bin/python3

from signal import signal, SIGTERM, SIGHUP, pause
from smbus import SMBus
from time import sleep

bus = SMBus(1)
ads7830_commands = (0x84, 0xc4, 0x94, 0xd4, 0xa4, 0xe4, 0xb4, 0xf4)


def safe_exit(signum, frame):
    exit(1)

def read_ads7830(input):
    bus.write_byte(0x4b, ads7830_commands[input])
    return bus.read_byte(0x4b)

def no_drift(input):
        value = read_ads7830(input)

        return value if value < 110 or value > 140 else 127 

def read_min(input):
    while True:
        value = read_ads7830(input)

        yield (127-value)/127 if value < 110 else 0

def read_max(input):
    while True:
        value = read_ads7830(input)

        yield (value-128)/127 if value > 140 else 0

try:
    signal(SIGTERM, safe_exit)
    signal(SIGHUP, safe_exit)

    while True:
        print(f"x: {read_ads7830(7)}, Y: {read_ads7830(6)}")
        sleep(.1)
    pause()

except KeyboardInterrupt:
    pass

finally:
    pass

