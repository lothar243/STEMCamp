import board
import neopixel
import time
import colorsys

# Note: this program must be run with sudo privileges

# CONFIGURE THIS
NUM_LEDS = 16
PIN = board.D18 # necessary (requires hardware PWM)

pixels = neopixel.NeoPixel(PIN, NUM_LEDS, auto_write=False)

def generate_rainbow(n):
    """Generate n RGB colors spread evenly through the HSV rainbow."""
    rainbow = []
    for i in range(n):
        hue = i / n  # Even spacing
        r, g, b = colorsys.hsv_to_rgb(hue, 1.0, 1.0)  # HSV → RGB (0.0–1.0)
        rgb = (int(r * 255), int(g * 255), int(b * 255))
        rainbow.append(rgb)
    return rainbow

def display_colors(rainbow):
    """Display a rainbow color list across the pixels."""
    for i in range(NUM_LEDS):
        pixels[i] = rainbow[i]
    pixels.show()

# Generate the starting colors
rainbow = generate_rainbow(NUM_LEDS)

# Continuously cycle the colors
while True:
    rainbow = rainbow[1:] + [rainbow[0]]  # Rotate left
    display_colors(rainbow)
    time.sleep(0.1)
