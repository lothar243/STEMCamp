from gpiozero import Button
from time import sleep

testButton = Button(16)
while True:
    if(testButton.is_pressed):
        print("The button is pressed")
    else:
        print("The button is not pressed")
    sleep(.25)
