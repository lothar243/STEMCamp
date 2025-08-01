import lcd_i2c

lcd_i2c.lcd_init()
lcd_i2c.lcd_string("Hello world!", lcd_i2c.LCD_LINE_1)

input("Press enter to end")

lcd_i2c.lcd_byte(0x01, lcd_i2c.LCD_CMD) # clear the screen when done


