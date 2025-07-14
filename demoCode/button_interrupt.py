from gpiozero import Button
from time import sleep

numberPresses = 0

def handleButtonPress():
    global numberPresses
    numberPresses += 1
    print(f"The button has been pressed {numberPresses} times")

testButton = Button(16, bounce_time=.05)
testButton.when_pressed = handleButtonPress

input("Press enter to exit\n")
    
exit()
    
    
    