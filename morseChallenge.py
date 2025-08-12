from gpiozero import LED
from time import sleep
from string import ascii_uppercase
import sys
import random
from base64 import b64decode
import os, hashlib

def flash_light(time):
    led.on()
    sleep(time)
    led.off()
    sleep(BETWEEN_LETTER)

def play_letter(letter):
    sequence = MORSE_CODE_DICT[letter.upper()]
    for char in sequence:
        if char == ".":
            flash_light(DIT_LENGTH)
        elif char == "-":
            flash_light(DAH_LENGTH)
        else:
            print("Encountered unknown character: " + char)
    sleep(PAUSE_LENGTH)

def sample():
    for letter in "hello":
        play_letter(letter)

def runRound(roundText, stringLength):
    score = 0
    print(roundText)
    for _ in range(LETTERS_PER_ROUND):
        print("Get ready for the next sequence")
        sleep(2)
        mystring = "".join([random.choice(ascii_uppercase) for _ in range(stringLength)])
        for letter in mystring:
            play_letter(letter)
        guess = input("What letter(s) were just played? ")
        if guess.upper() == mystring:
            score += 1
            print("Correct! You now have " + str(score) + " points")
        else:
            print("Sorry, that is incorrect, it was atually " + mystring)
            print("Quitting")
            exit()
    return score

def evalScore(roundNumber, currentScore):
    if LETTERS_PER_ROUND == currentScore:
        random.seed(generate_seed() + str(roundNumber))
        code = str(random.randint(10000,99999))
        print(str(b64decode(b'WW91IGdvdCBhIHBlcmZlY3Qgc2NvcmUgZm9yIHRoaXMgbGV2ZWwhIFlvdXIgZmxhZyBpcyBjeU1Uew=='))[2:-1] + code + "}")

def generate_seed():
    current_file = os.path.abspath(__file__)
    digest = hashlib.md5()

    with open(current_file, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            digest.update(chunk)

    return digest.hexdigest()

if __name__ == "__main__":
    led = LED(22)
    DIT_LENGTH = .3
    DAH_LENGTH = .9
    BETWEEN_LETTER = .3
    PAUSE_LENGTH = .9
    LETTERS_PER_ROUND = 5

    MORSE_CODE_DICT = { 'A':'.-', 'B':'-...',
                        'C':'-.-.', 'D':'-..', 'E':'.',
                        'F':'..-.', 'G':'--.', 'H':'....',
                        'I':'..', 'J':'.---', 'K':'-.-',
                        'L':'.-..', 'M':'--', 'N':'-.',
                        'O':'---', 'P':'.--.', 'Q':'--.-',
                        'R':'.-.', 'S':'...', 'T':'-',
                        'U':'..-', 'V':'...-', 'W':'.--',
                        'X':'-..-', 'Y':'-.--', 'Z':'--..',
                        '1':'.----', '2':'..---', '3':'...--',
                        '4':'....-', '5':'.....', '6':'-....',
                        '7':'--...', '8':'---..', '9':'----.',
                        '0':'-----', ', ':'--..--', '.':'.-.-.-',
                        '?':'..--..', '/':'-..-.', '-':'-....-',
                        '(':'-.--.', ')':'-.--.-'}


    roundNum = input("Which round would you like to run? (1-3) ")
    score = 0
    if(roundNum == '1'):
        score = runRound("Round 1, single letters", 1)
        evalScore(1, score)
    elif(roundNum == '2'):
        score = runRound("Round 2, two letters", 2)
        evalScore(2, score)
    elif(roundNum == '3'):
        score = runRound("Round 3, three letters", 3)
        evalScore(3, score)
    elif(roundNum == 4):
       score = runRound("Round 4, four letters", 4)
