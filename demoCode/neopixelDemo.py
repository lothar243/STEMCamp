import board
import neopixel
from time import sleep

pixels = neopixel.NeoPixel(board.D18, 30)



colorArray = [
    (200, 0, 130),   # magenta-ish
    (255, 0, 0),     # red
    (255, 64, 0),    # orange-red
    (255, 127, 0),   # orange
    (255, 191, 0),   # gold
    (255, 255, 0),   # yellow
    (191, 255, 0),   # yellow-green
    (127, 255, 0),   # lime green
    (0, 255, 0),     # green
    (0, 191, 127),   # teal
    (0, 127, 255),   # sky blue
    (0, 0, 255),     # blue
    (38, 0, 191),    # indigo
    (75, 0, 130),    # violet
    (120, 0, 192),   # purple
    (143, 0, 255)    # magenta-purple
]
count = 0
numPixels = 10
while True:
  for i in range(numPixels):
    pixels[i] = colorArray[(i + count) % numPixels]
  sleep(.2)
  count += 1
