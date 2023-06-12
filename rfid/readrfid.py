from myMFRC522 import SimpleMFRC522
import gpiod

reader = SimpleMFRC522()
try:
    reader.__init__()
    print("Tap the a card to the reader to read it (or press CTRL+C to quit)")
    id, text = reader.read()
    print("Card id: " + str(id))
    print("Text: " + text)
except KeyboardInterrupt:
    print("\nExiting due to keyboard interrupt")
finally:
    pass
#    chip = gpiod.Chip("1")
#    chip.reset()

