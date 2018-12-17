from game.snake import snakeGame
from ml.trainer import trainer
from ml.learner import learner
import threading

def startRunner():
    game = snakeGame(rerun)
    dataStoredPathPattern = "C:/Users/WarHorse/SourceControl/MLSnake/properData/snake_data_raw_v1*.json"
    t = trainer(dataStoredPathPattern)
    l = learner(dataStoredPathPattern)
    game.start(t.trackedMove, l.predict)

def rerun():
    threading.Thread(target=startRunner).start()
