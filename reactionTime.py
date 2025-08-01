"""
reactionTime.py
Connect an LED and Button to the specified GPIO ports
When the light turns off, push the button as quickly as you can
"""

from gpiozero import LED, Button
from time import sleep, time
import random
import os

led = LED(26)
button = Button(16)

FILENAME = "reaction_times.txt"
MAX_RECORDS = 5

def load_best_times():
    if not os.path.exists(FILENAME):
        return []
    with open(FILENAME, 'r') as f:
        return [float(line.strip()) for line in f.readlines()]

def save_best_times(times):
    with open(FILENAME, 'w') as f:
        for t in times:
            f.write(f"{t:.4f}\n")

def play_round():
    led.on()
    print("Wait for it...")
    sleep(random.uniform(3, 5))  # Wait before signal

    led.off()
    print("GO! Press the button!")

    start_time = time()
    button.wait_for_press()
    reaction_time = time() - start_time

    print(f"Your reaction time: {reaction_time:.4f} seconds")
    return reaction_time

def main():
    print("Welcome to the Reaction Timer Game!")
    best_times = load_best_times()

    while True:
        rt = play_round()
        best_times.append(rt)
        best_times.sort()
        best_times = best_times[:MAX_RECORDS]
        save_best_times(best_times)

        print("\nTop 10 Fastest Times:")
        for i, t in enumerate(best_times, 1):
            print(f"{i}. {t:.4f} sec")

        play_again = input("\nPlay again? (y/n): ").strip().lower()
        if play_again != 'y':
            print("Thanks for playing!")
            break

if __name__ == "__main__":
    main()

