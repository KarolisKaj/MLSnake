import pandas as pd 
import tensorflow as tf

class learner:
    def __init__(self, trainingSetPath):
        self.df = pd.read_json(trainingSetPath)

    def getModel(self):
        enumIndexes = [3, 4, 5, 6, 11]
        # Normalize
        for value in self.df:
            if(not value in enumIndexes):
                print([self.df[value]])
                self.df[value] = tf.keras.utils.normalize([self.df[value]])

        # Transform
        neighbour = {'Food': 4, 'Empty': 3,'Wall': 2, 'Body':1 }
        self.df[3] = [neighbour[item] for item in self.df[3]] 
        self.df[4] = [neighbour[item] for item in self.df[4]] 
        self.df[5] = [neighbour[item] for item in self.df[5]] 
        self.df[6] = [neighbour[item] for item in self.df[6]]

        move = {'Right': 1, 'Left': 2,'Top': 3, 'Bottom':4 }
        self.df[11] = [move[item] for item in self.df[11]]

        print(self.df)

