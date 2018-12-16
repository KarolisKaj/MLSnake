import pandas as pd 
import tensorflow as tf
import numpy as np
import glob as glob

class learner:
    def __init__(self, trainingSetPath):
        self.neighbour = { 'Food': 4, 'Empty': 3,'Wall': 2, 'Body': 1 }
        self.df = self.loadAllData(trainingSetPath)
        self.model = self.createModel()

    def fixData(self):
        # Transform
        self.df[3] = self.transformNeighbour(self.df[3])
        self.df[4] = self.transformNeighbour(self.df[4])
        self.df[5] = self.transformNeighbour(self.df[5])
        self.df[6] = self.transformNeighbour(self.df[6])

        move = {'Right': 0, 'Left': 1,'Top': 2, 'Bottom': 3 }
        self.df[11] = [move[item] for item in self.df[11]]

        # Normalize
        df = self.df
        self.dif = [1] * 11
        self.mean = [1] * 11
        for i in range(11): 
            self.dif[i] = self.df[i].max() - self.df[i].min()
            self.mean[i] = self.df[i].mean()
            df[i] = ((self.df[i] - self.mean[i]) / self.dif[i])
        return df

    def transformNeighbour(self, dataSet):
        return [self.neighbour[item] for item in dataSet]

    def createModel(self):
        df = self.fixData()

        model = tf.keras.models.Sequential()
        model.add(tf.keras.layers.Flatten())
        model.add(tf.keras.layers.Dense(11, activation = tf.nn.relu))
        model.add(tf.keras.layers.Dense(11, activation = tf.nn.relu))
        model.add(tf.keras.layers.Dense(4, activation = tf.nn.softmax))

        model.compile(optimizer = 'adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
        print(df.values)
        x_train = np.asarray([row[:11] for row in df.values])
        y_train = np.asarray([row[11] for row in df.values])
        model.fit(x_train, y_train, epochs = 13)
        return model

    def predict(self, dataRaw):
        data = [1] * 11
        data[3] = self.transformNeighbour([dataRaw[3]])[0]
        data[4] = self.transformNeighbour([dataRaw[4]])[0]
        data[5] = self.transformNeighbour([dataRaw[5]])[0]
        data[6] = self.transformNeighbour([dataRaw[6]])[0]
        
        for i in range(11):
            data[i] = (((data[i] if isinstance(dataRaw[i], str) else dataRaw[i]) - self.mean[i]) / self.dif[i])
        
        predictedMove = self.model.predict([[data]])
        print(predictedMove)
        print(np.argmax(predictedMove[0]))
        return np.argmax(predictedMove[0])
    
    def loadAllData(self, path):
        files = glob.iglob(path, recursive=False)
        dataFrames = [pd.read_json(file) for file in files]
        return pd.concat(dataFrames)

