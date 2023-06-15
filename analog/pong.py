"""Pong, classic arcade game.

Exercises

1. Change the colors.
2. What is the frame rate? Make it faster or slower.
3. Change the speed of the ball.
4. Change the size of the paddles.
5. Change how the ball bounces off walls.
6. How would you add a computer player?
6. Add a second ball.
"""

from random import choice, random, seed, randint
from turtle import *
import hashlib
from base64 import b64decode
from freegames import vector
import sys
from datetime import datetime


#ADC stuff
from smbus import SMBus
bus = SMBus(1)
ads7830_commands = (0x84, 0xc4, 0x94, 0xd4, 0xa4, 0xe4, 0xb4, 0xf4)

with open(sys.argv[0], 'r') as thisfile:
    myhash = hashlib.md5(thisfile.read().encode()).hexdigest()
    inthash = int(myhash, 16)

def scale_to_screen(initialVal):
    """Takes a values between 0 and 255 and scales it from -200 to 200"""
    return (initialVal * 400 / 256) - 200

def read_positions():

    bus.write_byte(0x4b, ads7830_commands[6])
    player1 = bus.read_byte(0x4b)
    bus.write_byte(0x4b, ads7830_commands[7])
    player2 = bus.read_byte(0x4b)
    if(not(isinstance(player1, int) and isinstance(player2, int))):
        print("Error, got values: {}, {}".format(player1, player2))
    return scale_to_screen(player1), scale_to_screen(player2)


def value():
    """Randomly generate value between (-5, -3) or (3, 5)."""
    return (3 + random() * 2) * choice([1, -1])


ball = vector(0, 0)
aim = vector(value(), value())
state = {1: 0, 2: 0, 'hitcount': 0}

def restart():
    ball.x = 0
    ball.y = 0
    aim.x = value()
    aim.y = value()
    state['hitcount'] = 0
    
def checkScore():
    if state['hitcount'] in (10, 15, 20):
        seed(inthash * state['hitcount'])
        code = str(randint(10000,99999))
        print("hitcount " + str(state['hitcount']) + ", cymt{" + code + "}")

def move(player, change):
    """Move player position by change."""
    state[player] += change


def rectangle(x, y, width, height):
    """Draw rectangle at (x, y) with given width and height."""
    up()
    goto(x, y)
    down()
    begin_fill()
    for count in range(2):
        forward(width)
        left(90)
        forward(height)
        left(90)
    end_fill()


def draw():
    """Draw game and move pong ball."""
    clear()
    player_positions = read_positions()
    state[1] = player_positions[0]
    state[2] = player_positions[1]

    rectangle(-200, state[1], 10, 50)
    rectangle(190, state[2], 10, 50)

    ball.move(aim)
    x = ball.x
    y = ball.y

    up()
    goto(x, y)
    dot(10)
    update()

    if y < -200 or y > 200:
        aim.y = -aim.y

    if x < -185:
        low = state[1]
        high = state[1] + 50

        if low <= y <= high:
            # bounce
            aim.x = -aim.x
            # small random height change
            seed = datetime.now().strftime('%s') * state['hitcount']
            aim.y += randint(-1, 1)
            # speed up
            if(state['hitcount'] %2 == 0):
                    aim.x += 1
            state['hitcount'] += 1
            checkScore()
        else:
            restart()

    if x > 185:
        low = state[2]
        high = state[2] + 50

        if low <= y <= high:
            # bounce
            aim.x = -aim.x
            # small random height change
            seed = datetime.now().strftime('%s') * state['hitcount']
            aim.y += randint(-1, 1)
            # speed up
            if(state['hitcount'] %2 == 0):
                    aim.x -= 1
            state['hitcount'] += 1
            checkScore()
        else:
            restart()

    ontimer(draw, 10)


setup(420, 420, 370, 0)
hideturtle()
tracer(False)
listen()
#onkey(lambda: move(1, 20), 'w')
#onkey(lambda: move(1, -20), 's')
#onkey(lambda: move(2, 20), 'i')
#onkey(lambda: move(2, -20), 'k')
draw()
done()
