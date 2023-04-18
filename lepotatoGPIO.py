import os
import gpiod
import time
import threading

piPinTranslation = {
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

class OutputDevice():
    def __init__(self, piPin):
        if piPin not in piPinTranslation.keys():
            raise Exception(f"Pi GPIO pin {piPin} not defined")

        self.gpiochip = piPinTranslation[piPin][0]
        self.gpionum = piPinTranslation[piPin][1]
        self.chip = gpiod.Chip('gpiochip{}'.format(self.gpiochip))
        self.line = self.chip.get_line(self.gpionum)
        self.line.request(consumer='LED', type=gpiod.LINE_REQ_DIR_OUT)
        print("Initialized") 

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

        super(LED, self).__init__(piPin)
        #if piPin not in piPinTranslation.keys():
        #    raise Exception(f"Pi GPIO pin {piPin} not defined")
#
#        self.gpiochip = piPinTranslation[piPin][0]
#        self.gpionum = piPinTranslation[piPin][1]
#        self.chip = gpiod.Chip('gpiochip{}'.format(self.gpiochip))
#        self.line = self.chip.get_line(self.gpionum)
#        self.line.request(consumer='LED', type=gpiod.LINE_REQ_DIR_OUT)
        self.blink_thread = None
        self.pulse_thread = None

        if(active_high):
            self.active=1
            self.inactive=0
        else:
            self.active=0
            self.inactive=1

        if(initial_value == False):
            self.off()
        elif(initial_value == True):
            self.on()

    def on(self):
        self.line.set_value(self.active)
        self.currentState = 1

    def off(self):
        self.line.set_value(self.inactive)
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
        pass


