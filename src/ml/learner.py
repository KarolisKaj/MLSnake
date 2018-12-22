import pandas as pd 
import tensorflow as tf
import numpy as np
import glob as glob

class learner:
    def __init__(self, trainingSetPath):
        self.neighbour = { 'Food': 10, 'Empty': 7,'Wall': 2, 'Body': 1 }
        self.df = self.loadAllData(trainingSetPath)
        self.model = self.createModel()

    def fixData(self, df):
        print("Fixing data...")
        # Transform
        df[3] = self.transformNeighbour(df[3])
        df[4] = self.transformNeighbour(df[4])
        df[5] = self.transformNeighbour(df[5])
        df[6] = self.transformNeighbour(df[6])

        # Make all positive
        df[7] = [value + 1000 for value in df[7]]
        df[8] = [value + 1000 for value in df[8]]
        df[9] = [value + 1000 for value in df[9]]
        df[10] = [value + 1000 for value in df[10]]

        df[7] = [hx - fx for hx, fx in zip(df[7], df[9])]
        df[9] = [hx - fx for hx, fx in zip(df[8], df[10])]
        df.drop(columns=[8,10], inplace=True)
        df.rename(index=int, columns={df.columns[8]: 8, df.columns[9]: 9})

        dfLastIndex = len(df.values[0]) - 1
        move = {'Right': 0, 'Left': 2,'Top': 1, 'Bottom': 3 }
        df[dfLastIndex] = [move[item] for item in df[dfLastIndex]]

        # Normalize
        self.dif = [1] * dfLastIndex
        self.mean = [1] * dfLastIndex
        for i in range(dfLastIndex): 
            self.dif[i] = df[i].max() - df[i].min()
            self.mean[i] = df[i].mean()
            df[i] = ((df[i] - self.mean[i]) / self.dif[i])
        return df

    def transformNeighbour(self, dataSet):
        return [self.neighbour[item] for item in dataSet]

    def createModel(self):
        self.df = self.fixData(self.df)
        dfLastIndex = len(self.df.values[0]) - 1
        print("Creating network...")
        model = tf.keras.models.Sequential()
        model.add(tf.keras.layers.Flatten())
        model.add(tf.keras.layers.Dense(36, input_shape=(11,), activation = tf.nn.relu))
        model.add(tf.keras.layers.Dense(24, activation = tf.nn.relu))
        model.add(tf.keras.layers.Dense(12, activation = tf.nn.relu))
        model.add(tf.keras.layers.Dense(4, activation = tf.nn.softmax))

        model.compile(optimizer = 'adam', loss='sparse_categorical_crossentropy', metrics=['accuracy'])
        print(self.df.values)
        x_train = np.asarray([row[:dfLastIndex] for row in self.df.values])
        y_train = np.asarray([row[dfLastIndex] for row in self.df.values])

        # Reduce data intake
        # x_train = x_train[:,[7,8,9,10]]
        model.fit(x_train, y_train, epochs = 1)
        return model

    def predict(self, dataRaw):
        dfLastIndex = len(self.df.values[0]) - 1
        data = np.zeros(dfLastIndex)
        data[3] = self.transformNeighbour([dataRaw[3]])[0]
        data[4] = self.transformNeighbour([dataRaw[4]])[0]
        data[5] = self.transformNeighbour([dataRaw[5]])[0]
        data[6] = self.transformNeighbour([dataRaw[6]])[0]

        data[7] = dataRaw[7] + 1000 - dataRaw[9] + 1000
        data[8] = dataRaw[8] + 1000 - dataRaw[10] + 1000
        # data[9] = 
        # data[10] = 
        
        for i in range(dfLastIndex):
            data[i] = (((data[i] if isinstance(dataRaw[i], str) else dataRaw[i]) - self.mean[i]) / self.dif[i])
        
        # Reduce data intake
        # data = data[7:11]
        predictedMove = self.model.predict([[data]])
        return np.argmax(predictedMove[0])
    
    def loadAllData(self, path):
        print("Reading training data...")
        files = glob.iglob(path, recursive=False)
        dataFrames = [pd.read_json(file) for file in files]
        return pd.concat(dataFrames)

