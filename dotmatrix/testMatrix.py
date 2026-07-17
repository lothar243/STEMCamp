from time import sleep
from pprint import pprint
from matrix import LedMatrix, single_led, full_row, full_column


matrix = LedMatrix()
matrix.start()

try:
    while True:

        # Move a full row downward
        for row in range(8):
            bitmap = full_row(row)
            matrix.set_bitmap(bitmap)

            print(f"full row {row}")
            pprint(bitmap)

            sleep(0.4)

        # Move a full column sideways
        for col in range(8):
            bitmap = full_column(col)
            matrix.set_bitmap(bitmap)

            print(f"full column {col}")
            pprint(bitmap)

            sleep(0.4)

except KeyboardInterrupt:
    print("Stopping...")

finally:
    matrix.stop()