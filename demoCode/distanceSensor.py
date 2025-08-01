import RPi.GPIO as GPIO
import time

TRIG = 23
ECHO = 24 # use a voltage divider here (1kOhm resistor to GPIO, 2kOhm resitor to ground to get voltage down to 3.3V)

GPIO.setmode(GPIO.BCM)
GPIO.setup(TRIG, GPIO.OUT)
GPIO.setup(ECHO, GPIO.IN)

def measure_distance(timeout=0.02):
    """Trigger pulse and measure echo duration with timeout."""
    GPIO.output(TRIG, True)
    time.sleep(0.00001)
    GPIO.output(TRIG, False)

    # Wait for echo to go HIGH (start time)
    start_time = time.time()
    timeout_start = start_time
    while GPIO.input(ECHO) == 0:
        if time.time() - timeout_start > timeout:
            return None  # No echo received
    pulse_start = time.time()

    # Wait for echo to go LOW (end time)
    timeout_start = time.time()
    while GPIO.input(ECHO) == 1:
        if time.time() - timeout_start > timeout:
            return None  # Echo took too long
    pulse_end = time.time()

    duration = pulse_end - pulse_start
    distance = (duration * 34300) / 2  # cm
    return round(distance, 2)

def is_consistent(readings, tolerance=0.10):
    """Check if all readings are within ±10% of the average."""
    if None in readings:
        return False
    avg = sum(readings) / len(readings)
    return all(abs(r - avg) / avg <= tolerance for r in readings)

if __name__ == "__main__":
    try:
        print("Measuring distance every 0.5 seconds...")
        while True:
            readings = [measure_distance() for _ in range(3)]
            if is_consistent(readings):
                avg = round(sum(readings) / 3, 2)
                print(f"Distance: {avg} cm")
            else:
                print("Inconsistent readings, skipping")
            time.sleep(0.5)

    except KeyboardInterrupt:
        print("\nStopped by user.")
    finally:
        GPIO.cleanup()
