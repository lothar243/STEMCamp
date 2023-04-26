import os
# import gpiod
import digitalio as dio
import time
import threading
from threading import Thread, Event
from itertools import repeat, cycle, chain
import board

piPinTranslation = {
        # 3.3V    P1
        2:  board.P3, 'SDA1': board.P3,
        3:  board.P5, 'SCL1': board.P5,
        4:  board.P7, 'GPIO4': board.P7,
        # Ground  P9
#        17: board.P11, 'GPIO17': board.P11, # TODO add P11
        27: board.P13, 'GPIO27': board.P13,
        22: board.P15, 'GPIO22': board.P15,
        # 3.3V    P17
        10: board.P19, 'SPIMOSI': board.P19, 'GPIO10': board.P19, 'MOSI': board.P19,
        9:  board.P21, 'SPIMISO': board.P21, 'GPIO9':  board.P21, 'MISO': board.P21,
        11: board.P23, 'SPICLK': board.P23, 'GPIO11': board.P23, 'SCLK': board.P23,
        # Ground  P.25
        0:  board.P27, 'ID_SD': board.P27, 'GPIO0':  board.P27, 'SDA0': board.P27,
        5:  board.P29, 'GPIO5':  board.P29,
        6:  board.P31, 'GPIO6':  board.P31,
        13: board.P33, 'PWM1': board.P33, 'GPIO13': board.P33,
        19: board.P35, 'GPIO19': board.P35,
        26: board.P37, 'GPIO26': board.P37,
        # Ground  P39

        # 5V      P2
        # 5V      P4
        # Ground  P6
        14: board.P8, 'TXD0': board.P8, 'GPIO14': board.P8,
        15: board.P10, 'RXD0': board.P10, 'GPIO15': board.P10,
        18: board.P12, 'PWM0': board.P12, 'GPIO18': board.P12, 
        # Ground  P14
        23: board.P16, 'GPIO23': board.P16,
        24: board.P18, 'GPIO24': board.P18,
        # Ground  P20
        25: board.P22, 'GPIO25': board.P22,
        8:  board.P24, 'SPICE0': board.P24, 'GPIO8':  board.P24, 'CE0': board.P24,
        7:  board.P26, 'SPICE1': board.P26, 'GPIO7':  board.P26, 'CE1': board.P26,
        'ID_SC': board.P28, 'SCL0': board.P28,
        # Ground  P30
        12: board.P32, 'GPIO12': board.P32,
        # Ground  P34
        16: board.P36, 'GPIO16': board.P36,
        20: board.P38, 'GPIO20': board.P38,
        21: board.P40, 'GPIO21': board.P40,

        }

piPinTranslation2 = {
        # 3.3V
        2:  (0, 5), 'SDA1': (0, 5),
        3:  (0, 4), 'SCL1': (0, 4),
        4:  (1, 98), 'GPIO4': (1, 98),
        # Ground
        17: (0, 8), 'GPIO17': (0, 8),
        27: (0, 9), 'GPIO27': (0, 9),
        22: (0, 10), 'GPIO22': (0, 10),
        # 3.3V
        10: (1, 87), 'SPIMOSI': (1, 87), 'GPIO10': (1, 87), 'MOSI': (1, 87),
        9:  (1, 88), 'SPIMISO': (1, 88), 'GPIO9':  (1, 88), 'MISO': (1, 88),
        11: (1, 90), 'SPICLK': (1, 90), 'GPIO11': (1, 90), 'SCLK': (1, 90),
        # Ground
        0:  (1, 75), 'ID_SD': (1, 75), 'GPIO0':  (1, 75), 'SDA0': (1, 75),
        5:  (1, 96), 'GPIO5':  (1, 96),
        6:  (1, 97), 'GPIO6':  (1, 97),
        13: (1, 85), 'PWM1': (1, 85), 'GPIO13': (1, 85),
        19: (1, 86), 'GPIO19': (1, 86),
        26: (1, 84), 'GPIO26': (1, 84),
        # Ground

        # 5V
        # 5V
        # Ground
        14: (1, 91), 'TXD0': (1, 91), 'GPIO14': (1, 91),
        15: (1, 92), 'RXD0': (1, 92), 'GPIO15': (1, 92),
        18: (0, 6), 'PWM0': (0, 6), 'GPIO18': (0, 6), 
        # Ground
        23: (1, 93), 'GPIO23': (1, 93),
        24: (1, 94), 'GPIO24': (1, 94),
        # Ground
        25: (1, 79), 'GPIO25': (1, 79),
        8:  (1, 89), 'SPICE0': (1, 89), 'GPIO8':  (1, 89), 'CE0': (1, 89),
        7:  (1, 80), 'SPICE1': (1, 80), 'GPIO7':  (1, 80), 'CE1': (1, 80),
        'ID_SC': (1, 76), 'SCL0': (1, 76),
        # Ground
        12: (1, 95), 'GPIO12': (1, 95),
        # Ground
        16: (1, 81), 'GPIO16': (1, 81),
        20: (1, 82), 'GPIO20': (1, 82),
        21: (1, 83), 'GPIO21': (1, 83),

        }



_THREADS = set()

class ZombieThread(RuntimeError):
    "Error raised when a thread fails to die within a given timeout"

def _threads_shutdown():
    while _THREADS:
        threads = _THREADS.copy()
        # Optimization: instead of calling stop() which implicitly calls
        # join(), set all the stopping events simultaneously, *then* join
        # threads with a reasonable timeout
        for t in threads:
            t.stopping.set()
        for t in threads:
            t.join(10)


class GPIOThread(Thread):
    def __init__(self, target, args=(), kwargs=None, name=None):
        if kwargs is None:
            kwargs = {}
        self.stopping = Event()
        super().__init__(None, target, name, args, kwargs)
        self.daemon = True

    def start(self):
        self.stopping.clear()
        _THREADS.add(self)
        super().start()

    def stop(self, timeout=10):
        self.stopping.set()
        self.join(timeout)

    def join(self, timeout=None):
        super().join(timeout)
        if self.is_alive():
            assert timeout is not None
            # timeout can't be None here because if it was, then join()
            # wouldn't return until the thread was dead
            raise ZombieThread(
                "Thread failed to die within {timeout} seconds".format(
                    timeout=timeout))
        else:
            _THREADS.discard(self)


class OutputDevice(dio.DigitalInOut):
    def __init__(self, piPin):
        if piPin not in piPinTranslation.keys():
            raise Exception(f"Pi GPIO pin {piPin} not defined")

#        self.gpiochip = piPinTranslation[piPin][0]
#        self.gpionum = piPinTranslation[piPin][1]
        super().__init__(piPinTranslation[piPin],)
        self.direction = dio.Direction.OUTPUT

        """     
                self.chip = gpiod.Chip('gpiochip{}'.format(self.gpiochip))
                self.line = self.chip.get_line(self.gpionum)
                self.line.request(consumer='LED', type=gpiod.LINE_REQ_DIR_OUT)
        """
        
    def _write(self, value):
        #        if value:
        #            write_value = 1
        #        else:
        #            write_value = 0
        try:
            #self.line.set_value(write_value)
            self.value = value
        except AttributeError:
            raise

class LED(OutputDevice):
    """
The following example will light the LED:
from lePotatoGPIO import LED

led1 = LED(22)
led.on()

:type pin: int or str
:param pin:
    The GPIO pin which the LED is connected to.

:param bool active_high:
    If :data:`True` (the default), the LED will operate normally with the
    circuit described above. If :data:`False` you should wire the cathode
    to the GPIO pin, and the anode to a 3V3 pin (via a limiting resistor).

:type initial_value: bool or None
:param initial_value:
    If :data:`False` (the default), the LED will be off initially.  If
    :data:`None`, the LED will be left in whatever state the pin is found
    in when configured for output (warning: this can be on).  If
    :data:`True`, the LED will be switched on initially.

    """

    def __init__(self, piPin, active_high=True, initial_value=False):

        self._blink_thread = None
        self._controller = None
        self._pulse_thread = None
        super().__init__(piPin,)

        self.active_high = active_high

        #if(initial_value == False):
        #    self.off()
        #elif(initial_value == True):
        #    self.on()

    def on(self):
        self._stop_blink()
        self._write(self.active_high)
        self.currentState = 1

    def off(self):
        self._stop_blink()
        self._write(not self.active_high)
        self.currentState = 0

    def toggle(self):
        if self.currentState == 1:
            self.off()
        else:
            self.on()

    def blink(self, on_time=1, off_time=1, n=None, background=True):
        """
Make the device turn on and off repeatedly.

:param float on_time:
    Number of seconds on. Defaults to 1 second.

:param float off_time:
    Number of seconds off. Defaults to 1 second.

:type n: int or None

:param n:
    Number of times to blink; :data:`None` (the default) means forever.

:param bool background:
    If :data:`True` (the default), start a background thread to
    continue blinking and return immediately. If :data:`False`, only
    return when the blink is finished (warning: the default value of
    *n* will result in this method never returning)."""
        self._stop_blink()
        self._blink_thread = GPIOThread(
                self._blink_device, (on_time, off_time, n))
        self._blink_thread.start()
        if not background:
            self._blink_thread.join()
            self._blink_thread = None

    def _stop_blink(self):
        if getattr(self, '_controller', None):
            self._controller._stop_blink(self)
        self._controller = None
        if getattr(self, '_blink_thread', None):
            self._blink_thread.stop()
        self._blink_thread = None

    def _blink_device(self, on_time, off_time, n):
        iterable = repeat(0) if n is None else repeat(0, n)
        for _ in iterable:
            self._write(True)
            if self._blink_thread.stopping.wait(on_time):
                break
            self._write(False)
            if self._blink_thread.stopping.wait(off_time):
                break

class InputDevice(dio.DigitalInOut):
    def __init__(self, piPin):
        if piPin not in piPinTranslation.keys():
            raise Exception(f"Pi GPIO pin {piPin} not defined")
        super().__init__(piPinTranslation[piPin],)

    def __del__(self):
        self.line.release()
        self.chip.close()


class Button(InputDevice):
    def __init__(self, piPin, debounce=100):

        super().__init__(piPin)
        #self.gpiochip = piPinTranslation[piPin][0]
        #self.gpionum = piPinTranslation[piPin][1]
        #self.chip = gpiod.Chip('gpiochip{}'.format(self.gpiochip))
        #self.line = self.chip.get_line(self.gpionum)
        #self.line.request(consumer='BUTTON', type=gpiod.LINE_REQ_DIR_IN)
        # super(Button, self).__init__(piPin)
        #self.debounce = debounce
        # self.line.set_debounce(self.debounce)
        
        self.callbacks = []
        self.thread = None

    def when_pressed(self, callback):
        print("button pressed")
        self.callbacks.append((gpiod.LINE_EVENT_RISING_EDGE, callback))

    def when_release(self, callback):
        print("button released")
        self.callbacks.append((gpiod.LINE_EVENT_FALLING_EDGE, callback))

    def wait_for_press(self):
        print("waiting for press")
        self.line.event_wait(gpiod.LINE_REQUEST_INPUT)

    def is_pressed(self):
        return self.value

    

