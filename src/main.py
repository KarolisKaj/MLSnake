from game.snake import start
from ml.trainer import trainer
from ml.learner import learner

trainer = trainer()
learner = learner("C:/Users/WarHorse/SourceControl/MLSnake/properData/snake_data_raw_v1.json")
learner.getModel()
start(trainer.trackedMove)