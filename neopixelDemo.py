import board
import neopixel
from time import sleep

pixels = neopixel.NeoPixel(board.D18, 30)



colorArray = [(200,0,130), (255,0,0), (255,127,0), (255,255,0), (127,255,0), (0,255,0), (0,127,255), (0,0,255), (75,0,130), (143,0,255)]
count = 0
numPixels = 10
while True:
  for i in range(numPixels):
    pixels[i] = colorArray[(i + count) % numPixels]
  sleep(.2)
  count += 1
