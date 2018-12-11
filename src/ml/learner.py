import pandas as pd 
import tensorflow as tf
import numpy as np

class learner:
    def __init__(self, trainingSetPath):
        self.df = pd.read_json(trainingSetPath)


    def fixData(self):
        # Transform
        neighbour = { 'Food': 4, 'Empty': 3,'Wall': 2, 'Body': 1 }
        self.df[3] = [neighbour[item] for item in self.df[3]] 
        self.df[4] = [neighbour[item] for item in self.df[4]] 
        self.df[5] = [neighbour[item] for item in self.df[5]] 
        self.df[6] = [neighbour[item] for item in self.df[6]]

        move = {'Right': 1, 'Left': 2,'Top': 3, 'Bottom':4 }
        self.df[11] = [move[item] for item in self.df[11]]

        # Normalize
        
        df = ((self.df - self.df.mean()) / (self.df.max() - self.df.min()))
        df[11] = self.df[11]
        return df

    def getModel(self):
        df = self.fixData()

        model = tf.keras.models.Sequential()
        model.add(tf.keras.layers.Flatten())
        model.add(tf.keras.layers.Dense(10, activation = tf.nn.relu))
        model.add(tf.keras.layers.Dense(20, activation = tf.nn.relu))
        model.add(tf.keras.layers.Dense(5, activation = tf.nn.softmax))

        model.compile(optimizer = 'adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
        print(df.values)
        x_train = np.asarray([row[:11] for row in df.values])
        y_train = np.asarray([row[11] for row in df.values])
        model.fit(x_train, y_train, epochs=4)
        return model

