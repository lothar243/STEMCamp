import board
import neopixel
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

