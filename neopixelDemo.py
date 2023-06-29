import board
import neopixel
from time import sleep

pixels = neopixel.NeoPixel(board.D18, 30)

pixels.fill((100,0,100))
pixels[0] = (255,0,0)
pixels[1] = (255,0,0)
pixels[2] = (255,127,0)
pixels[3] = (255,255,0)
pixels[4] = (127,255,0)
pixels[5] = (0,255,0)
pixels[6] = (0,127,255)
pixels[7] = (0,0,255)
pixels[8] = (75,0,130)
pixels[9] = (143,0,255)

colorArray = [(200,0,130), (255,0,0), (255,127,0), (255,255,0), (127,255,0), (0,255,0), (0,127,255), (0,0,255), (75,0,130), (143,0,255)]
count = 0
numPixels = 10
while True:
  for i in numPixels:
    pixels[i] = colorArray[(i + count) % numPixels]
  sleep(.2)
  count += 1
