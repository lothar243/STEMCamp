import lcd_i2c
from myMFRC522 import SimpleMFRC522
import gpiod

reader = SimpleMFRC522()
try:
    reader.__init__()
    lcd_i2c.lcd_init()
    while True:
        id, text = reader.read()
        print("Card read, see LCD")
        #print("id=",id)
        #print("text=",text)
        lcd_i2c.lcd_string(str(id), lcd_i2c.LCD_LINE_1)
        lcd_i2c.lcd_string(str(text), lcd_i2c.LCD_LINE_2)
except KeyboardInterrupt:
    print("\nExiting due to keyboard interrupt")
finally:
    print("Cleaning up...")
    lcd_i2c.lcd_byte(0x01, lcd_i2c.LCD_CMD)

