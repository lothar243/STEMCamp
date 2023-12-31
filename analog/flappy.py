"""Flappy, game inspired by Flappy Bird.

Exercises

1. Keep score.
2. Vary the speed.
3. Vary the size of the balls.
4. Allow the bird to move forward and back.
"""

from random import *
from turtle import *

from freegames import vector
from smbus import SMBus
bus = SMBus(1)
ads7830_commands = (0x84, 0xc4, 0x94, 0xd4, 0xa4, 0xe4, 0xb4, 0xf4)

def covered():
    bus.write_byte(0x4b, ads7830_commands[7])
    reading = bus.read_byte(0x4b)
    print(reading)
    return (reading > 200)


bird = vector(0, 0)
balls = []


def tap(x, y):
    """Move bird up in response to screen tap."""
    up = vector(0, 30)
    bird.move(up)


def inside(point):
    """Return True if point on screen."""
    return -200 < point.x < 200 and -200 < point.y < 200


def draw(alive):
    """Draw screen objects."""
    clear()

    if covered():
        bird.y += 4
    else:
        bird.y -= 4
    goto(bird.x, bird.y)

    if alive:
        dot(10, 'green')
    else:
        dot(10, 'red')

    for ball in balls:
        goto(ball.x, ball.y)
        dot(20, 'black')

    update()


def move():
    """Update object positions."""
    #bird.y -= 5

    for ball in balls:
        ball.x -= 3

    if randrange(10) == 0:
        y = randrange(-199, 199)
        ball = vector(199, y)
        balls.append(ball)

    while len(balls) > 0 and not inside(balls[0]):
        balls.pop(0)

    if not inside(bird):
        draw(False)
        return

    for ball in balls:
        if abs(ball - bird) < 15:
            draw(False)
            return

    draw(True)
    ontimer(move, 30)


setup(420, 420, 370, 0)
hideturtle()
up()
tracer(False)
#onscreenclick(tap)
move()
done()
