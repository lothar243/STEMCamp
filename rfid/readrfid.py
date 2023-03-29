from myMFRC522 import SimpleMFRC522
import gpiod

reader = SimpleMFRC522()
try:
    print("Tap the a card to the reader to read it...")
    id, text = reader.read()
    print(id)
    print(text)
except KeyboardInterrupt:
    print("\nExiting due to keyboard interrupt")
finally:
    chip = gpiod.chip(1)
    chip.reset()

