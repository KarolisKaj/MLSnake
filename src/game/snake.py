from turtle import *
from random import randrange
from freegames import square, vector
from ml.initial import trackedMove

food = vector(0, 0)
snake = [vector(10, 0)]
aim = vector(0, -10)

def change(x, y):
    aim.x = x
    aim.y = y

def inside(coordinates):
    return -200 < coordinates.x < 190 and -200 < coordinates.y < 190

def moveDirection(head, aim):
    if(head.x > aim.x):
        return "Right"
    elif(head.x < aim.x):
        return "Left"
    elif(head.y > aim.y):
        return "Bottom"
    else:
        return "Top"


def move():
    head = snake[-1].copy()
    direction = moveDirection(head, aim)
    head.move(aim)

    if not inside(head) or head in snake:
        square(head.x, head.y, 9, 'red')
        update()
        return

    snake.append(head)

    if head == food:
        print('Snake:', len(snake))
        food.x = randrange(-19, 19) * 10
        food.y = randrange(-19, 19) * 10
    else:
        snake.pop(0)

    clear()

    for body in snake:
        square(body.x, body.y, 9, 'black')

    square(food.x, food.y, 9, 'green')
    update()
    ontimer(move, 100)
    trackedMove(len(snake), len(snake) * 10, (head.x - 10, head.y), (head.x + 10, head.y),(head.x, head.y + 10), (head.x, head.y - 10), (head.x, head.y), (food.x, food.y), direction)
    # Tracking snake actions.

def whereIsCoordinate(coordinates):
    if(not inside(coordinates)):
        return "Wall"
    elif (coordinates in snake):
        return "Body"
    elif (coordinates == food):  
        return "Food"
    else:
        return "Empty"

def start():
    setup(420, 420, 370, 0)
    hideturtle()
    tracer(False)
    listen()
    onkey(lambda: change(10, 0), 'Right')
    onkey(lambda: change(-10, 0), 'Left')
    onkey(lambda: change(0, 10), 'Up')
    onkey(lambda: change(0, -10), 'Down')
    move()
    done()