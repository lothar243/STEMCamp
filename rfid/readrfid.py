from mfrc522 import SimpleMFRC522
import RPi.GPIO as GPIO
import time

reader = SimpleMFRC522()

try:
    print("Tap a card to the reader...")
    while True:
        try:
            id, text = reader.read()
            if id:
                print("ID:", id)
                print("Text:", text.strip())
                break
        except Exception as e:
            print("Read error:", e)
        time.sleep(0.5)  # Prevent CPU spike
finally:
    GPIO.cleanup()
