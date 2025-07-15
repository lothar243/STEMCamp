from gpiozero import PWMLED
from time import sleep

led = PWMLED(17)

while True:
    led.value = 0.0  # Off
    sleep(1)
    led.value = 0.5  # Half brightness
    sleep(1)
    led.value = 1.0  # Full brightness
    sleep(1)

