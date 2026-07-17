from time import sleep
import sys

from matrix import LedMatrix, blank_bitmap


FRAME_DELAY = 0.5


def line_to_bitmap_row(line):
    """
    Convert one line of text into one LED matrix row.

    '1' means the LED is on.
    Anything else means the LED is off.

    Example:
        "10100000" becomes:
        [True, False, True, False, False, False, False, False]
    """

    row = []

    for char in line.strip():
        row.append(char == "1")

    # Make sure the row is exactly 8 columns wide.
    while len(row) < 8:
        row.append(False)

    return row[:8]


def load_bitmaps(filename):
    """
    Load a list of 8x8 bitmaps from a text file.

    Each frame should contain 8 rows.
    Blank lines are ignored.

    Example frame:

        00111100
        01000010
        10100101
        10000001
        10100101
        10011001
        01000010
        00111100
    """

    bitmaps = []
    current_frame = blank_bitmap()
    current_row = 0

    with open(filename, "r") as filedata:
        for line in filedata:
            line = line.strip()

            # Skip blank lines between frames.
            if line == "":
                continue

            current_frame[current_row] = line_to_bitmap_row(line)
            current_row += 1

            # Once we have 8 rows, save the frame.
            if current_row == 8:
                bitmaps.append(current_frame)
                current_frame = blank_bitmap()
                current_row = 0

    if current_row != 0:
        print("Warning: the last frame was incomplete and was ignored.")

    return bitmaps


def main():
    if len(sys.argv) < 2:
        print("Usage: python3 customAnimation.py dots.txt")
        sys.exit(1)

    filename = sys.argv[1]
    bitmaps = load_bitmaps(filename)

    if len(bitmaps) == 0:
        print("No complete 8x8 frames were found.")
        sys.exit(1)

    matrix = LedMatrix()
    matrix.start()

    try:
        frame_number = 0

        while True:
            bitmap = bitmaps[frame_number % len(bitmaps)]
            matrix.set_bitmap(bitmap)

            sleep(FRAME_DELAY)
            frame_number += 1

    except KeyboardInterrupt:
        print("Stopping...")

    finally:
        matrix.stop()


main()