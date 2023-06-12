from myMFRC522 import SimpleMFRC522
import gpiod

mfrc = SimpleMFRC522()
userText = input("Enter a string to store: ")
print("Ok, now tap your RFID card to write the data. Press CTRL+C to quit")
try:
    mfrc.__init__()
    mfrc.write(userText)
    print("The data has been written, tap again to read the data.")
    id, text = mfrc.read()
    print("ID = {}".format(id))
    print("text = {}".format(text))
except KeyboardInterrupt:
    print("Exiting due to CTRL+C sequence")
finally:
    pass

