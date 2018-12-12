from turtle import *
from random import randrange
from freegames import square, vector

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

def whereIsCoordinate(coordinates):
    if(not inside(coordinates)):
        return "Wall"
    elif (coordinates in snake):
        return "Body"
    elif (coordinates == food):  
        return "Food"
    else:
        return "Empty"

def move(track, predict):
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
    ontimer(lambda: move(track, predict), 100)
    stepData = track(len(snake), len(snake) * 10, whereIsCoordinate(vector(head.x - 10, head.y)), whereIsCoordinate(vector(head.x + 10, head.y)), whereIsCoordinate(vector(head.x, head.y + 10)), whereIsCoordinate(vector(head.x, head.y - 10)), (head.x, head.y), (food.x, food.y), direction)
    predictedDirection = predict(stepData)
    #{'Right': 0, 'Left': 1,'Top': 2, 'Bottom': 3 }
    if(predictedDirection == 0):
        right()
    elif(predictedDirection == 1):
        left()
    elif(predictedDirection == 2):
        bottom()
    elif(predictedDirection == 3):
        top()

def start(track, predict):
    setup(420, 420, 370, 0)
    hideturtle()
    tracer(False)
    listen()
    # onkey(lambda: change(10, 0), 'Right')
    # onkey(lambda: change(-10, 0), 'Left')
    # onkey(lambda: change(0, 10), 'Up')
    # onkey(lambda: change(0, -10), 'Down')
    move(track, predict)
    done()

def right():
    change(10, 0)
def left():
    change(-10, 0)
def top():
    change(0, 10)
def bottom():
    change(0, -10)