heart = [
    0b00000,
    0b01010,
    0b11111,
    0b11111,
    0b11111,
    0b01110,
    0b00100,
    0b00000
]

from lcd_i2c import *

lcd_init()
lcd_create_char(0, heart)
lcd_string("Custom: " + chr(0), LCD_LINE_1)


