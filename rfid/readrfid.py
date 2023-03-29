from myMFRC522 import SimpleMFRC522

reader = SimpleMFRC522()
try:
    print("Tap the a card to the reader to read it...")
    id, text = reader.read()
    print(id)
    print(text)
finally:
    pass
    # GPIO.cleanup()

