import turtle
from random import randrange
from freegames import square, vector

class snakeGame:
    def __init__(self):
        self.food = vector(0, 0)
        self.snake = [vector(10, 0)]
        self.aim = vector(0, -10)

    def setFoodCoordinates(self):
        self.food.x = randrange(-19, 19) * 10
        self.food.y = randrange(-19, 19) * 10
        if(self.food in self.snake):
            self.setFoodCoordinates()

    def change(self, x, y):
        self.aim.x = x
        self.aim.y = y

    def inside(self, coordinates):
        return -200 < coordinates.x < 200 and -200 < coordinates.y < 200

    def move(self, track, predict):
        head = self.snake[-1].copy()
        # Play
        stepData = track(len(self.snake), len(self.snake) * 10, self.whereIsCoordinate(vector(head.x - 10, head.y)), self.whereIsCoordinate(vector(head.x + 10, head.y)), self.whereIsCoordinate(vector(head.x, head.y + 10)), self.whereIsCoordinate(vector(head.x, head.y - 10)), (head.x, head.y), (self.food.x, self.food.y), None)
        self.performPredictedMove(predict(stepData))
        # Learn
        direction = self.moveDirection(head, self.aim)
        track(len(self.snake), len(self.snake) * 10, self.whereIsCoordinate(vector(head.x - 10, head.y)), self.whereIsCoordinate(vector(head.x + 10, head.y)), self.whereIsCoordinate(vector(head.x, head.y + 10)), self.whereIsCoordinate(vector(head.x, head.y - 10)), (head.x, head.y), (self.food.x, self.food.y), direction)
        head.move(self.aim)

        if not self.inside(head) or head in self.snake:
            square(head.x, head.y, 9, 'red')
            turtle.update()
            return

        self.snake.append(head)

        if head == self.food:
            print('Snake size :', len(self.snake))
            self.setFoodCoordinates()
        else:
            self.snake.pop(0)

        turtle.clear()

        for body in self.snake:
            square(body.x, body.y, 9, 'black')

        square(self.food.x, self.food.y, 9, 'green')
        turtle.update()
        turtle.ontimer(lambda: self.move(track, predict), 100)


    def start(self, track, predict):
        turtle.setup(420, 420, 370, 0)
        turtle.hideturtle()
        turtle.tracer(False)
        turtle.listen()
        # turtle.onkey(lambda: self.change(10, 0), 'Right')
        # turtle.onkey(lambda: self.change(-10, 0), 'Left')
        # turtle.onkey(lambda: self.change(0, 10), 'Up')
        # turtle.onkey(lambda: self.change(0, -10), 'Down')
        self.move(track, predict)
        turtle.done()


    #{'Right': 0, 'Left': 1,'Top': 2, 'Bottom': 3 }
    def performPredictedMove(self, predictedDirection):
        if(predictedDirection == 0):
            self.right()
        elif(predictedDirection == 1):
            self.left()
        elif(predictedDirection == 2):
            self.top()
        elif(predictedDirection == 3):
            self.bottom()

    def right(self):
        self.change(10, 0)
    def left(self):
        self.change(-10, 0)
    def top(self):
        self.change(0, 10)
    def bottom(self):
        self.change(0, -10)

    def moveDirection(self, head, aim):
        if(aim.x > 0):
            return "Right"
        elif(aim.x < 0):
            return "Left"
        elif(aim.y < 0):
            return "Bottom"
        else:
            return "Top"

    def whereIsCoordinate(self, coordinates):
        if(not self.inside(coordinates)):
            return "Wall"
        elif (coordinates in self.snake):
            return "Body"
        elif (coordinates == self.food):  
            return "Food"
        else:
            return "Empty"