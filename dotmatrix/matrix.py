import RPi.GPIO as GPIO
from time import sleep
from threading import Thread, Event, Lock


# GPIO pin numbers, using BCM numbering.
#
# Columns: C1, C2, C3, C4, C5, C6, C7, C8
DEFAULT_COLUMN_PINS = [5, 17, 25, 10, 23, 16, 6, 4]

# Rows: R1, R2, R3, R4, R5, R6, R7, R8
DEFAULT_ROW_PINS = [22, 18, 19, 12, 20, 26, 27, 13]


class LedMatrix:
    """
    Controls an 8x8 LED matrix.

    The display is represented as an 8x8 list:

        bitmap[row][col]

    where True means the LED should be on.

    Example:

        bitmap = blank_bitmap()
        bitmap[0][0] = True      # top-left LED
        bitmap[7][7] = True      # bottom-right LED
        matrix.set_bitmap(bitmap)
    """

    def __init__(
        self,
        row_pins=None,
        column_pins=None,
        display_delay=0.001,
        gpio_mode=GPIO.BCM,
    ):
        self.row_pins = row_pins or DEFAULT_ROW_PINS
        self.column_pins = column_pins or DEFAULT_COLUMN_PINS
        self.display_delay = display_delay

        self.current_bitmap = blank_bitmap()

        self.stop_event = Event()
        self.bitmap_lock = Lock()
        self.thread = None

        GPIO.setmode(gpio_mode)
        self.setup_gpio()

    def setup_gpio(self):
        for pin in self.row_pins + self.column_pins:
            GPIO.setup(pin, GPIO.OUT)

        self.clear_pins()

    def clear_pins(self):
        """
        Turn the display off.

        Rows are active-high.
        Columns are active-low.
        """

        for row_pin in self.row_pins:
            GPIO.output(row_pin, GPIO.LOW)

        for column_pin in self.column_pins:
            GPIO.output(column_pin, GPIO.HIGH)

    def display_once(self, bitmap):
        """
        Scan through the display one row at a time.

        This must run repeatedly because an LED matrix is multiplexed.
        """

        for row in range(8):
            # Turn on this row.
            GPIO.output(self.row_pins[row], GPIO.HIGH)

            # Set each column for this row.
            for col in range(8):
                if bitmap[row][col]:
                    GPIO.output(self.column_pins[col], GPIO.LOW)
                else:
                    GPIO.output(self.column_pins[col], GPIO.HIGH)

            sleep(self.display_delay)

            # Turn everything off before moving to the next row.
            self.clear_pins()

    def refresh_loop(self):
        """
        Keeps refreshing the display until stop() is called.
        """

        while not self.stop_event.is_set():
            with self.bitmap_lock:
                bitmap_copy = copy_bitmap(self.current_bitmap)

            self.display_once(bitmap_copy)

    def start(self):
        """
        Starts the background display-refresh thread.
        """

        if self.thread is None:
            self.thread = Thread(target=self.refresh_loop)
            self.thread.start()

    def stop(self):
        """
        Stops the display-refresh thread and turns off the GPIO pins.
        """

        self.stop_event.set()

        if self.thread is not None:
            self.thread.join()

        self.clear_pins()
        GPIO.cleanup()

    def set_bitmap(self, bitmap):
        """
        Replaces the image currently shown on the LED matrix.
        """

        with self.bitmap_lock:
            self.current_bitmap = copy_bitmap(bitmap)

    def clear(self):
        """
        Clears the displayed image.
        """

        self.set_bitmap(blank_bitmap())

    def set_led(self, row, col, value=True):
        """
        Turn one LED on or off.

        row and col should each be from 0 to 7.
        """

        with self.bitmap_lock:
            self.current_bitmap[row][col] = value


def blank_bitmap():
    """
    Create a blank 8x8 bitmap.

    Do not use [[False] * 8] * 8 because that reuses the same row 8 times.
    """

    return [[False for col in range(8)] for row in range(8)]


def copy_bitmap(bitmap):
    """
    Makes a real copy of an 8x8 bitmap.
    """

    return [row[:] for row in bitmap]


def single_led(row, col):
    """
    Create a bitmap with one LED turned on.
    """

    bitmap = blank_bitmap()
    bitmap[row][col] = True
    return bitmap


def full_row(row):
    """
    Create a bitmap with one full row turned on.
    """

    bitmap = blank_bitmap()
    bitmap[row] = [True for col in range(8)]
    return bitmap


def full_column(col):
    """
    Create a bitmap with one full column turned on.
    """

    bitmap = blank_bitmap()

    for row in range(8):
        bitmap[row][col] = True

    return bitmap