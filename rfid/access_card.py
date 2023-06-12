from myMFRC522 import SimpleMFRC522
from lepotatoGPIO import LED
import lcd_i2c
import csv
import time


redPin = 21
yellowPin = 20
greenPin = 16
redLight = LED(redPin)
yellowLight = LED(yellowPin)
greenLight = LED(greenPin)
redLight.off()
yellowLight.off()
greenLight.off()

USE_LCD = True

def logAccess(id, status):
    with open ("log.txt", 'a') as logfile:
        logfile.write("{} id={}, {}\n".format(time.strftime("%Y-%m-%d %H:%m:%S", time.gmtime()), id, status))

with open ("validcards.txt", 'r')  as cardfile:
    filelines = cardfile.readlines()
    validcards = []
    for line in filelines:
        try:
            validcards.append(int(line))
        except:
            print("Error in validcards.txt, couldn't convert '{}'".format(line[:-1]))

print(validcards)
    

reader = SimpleMFRC522()
try:
    if USE_LCD:
        lcd_i2c.lcd_init()
    while True:
        reader.__init__()
        redLight.off()
        yellowLight.on()
        greenLight.off()
        if USE_LCD:
            lcd_i2c.lcd_string(" Please present", lcd_i2c.LCD_LINE_1)
            lcd_i2c.lcd_string('    RFID card', lcd_i2c.LCD_LINE_2)
        else:
            print("Please present your RFID card")
        id, text = reader.read()
        print("card swiped, id=", type(id) ,id)
        if id in validcards:
            yellowLight.off()
            greenLight.on()
            logAccess(id, "Access Granted")
            if USE_LCD:
                lcd_i2c.lcd_string("Access Granted", lcd_i2c.LCD_LINE_1)
                lcd_i2c.lcd_string(str(id), lcd_i2c.LCD_LINE_2)
            else:
                print("Access Granted")
            time.sleep(5)
        else:
            yellowLight.off()
            redLight.on()
            logAccess(id, "Access Denied")
            if(USE_LCD):
                lcd_i2c.lcd_string("Access Denied", lcd_i2c.LCD_LINE_1)
                lcd_i2c.lcd_string(str(id), lcd_i2c.LCD_LINE_2)
            else:
                print("Access Denied")
            time.sleep(5)


except KeyboardInterrupt:
    print("\nExiting due to keyboard interrupt")
            
finally:
    print("Cleaning up...")
    lcd_i2c.lcd_byte(0x01, lcd_i2c.LCD_CMD)
