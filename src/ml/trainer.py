import pandas as pd 
import numpy as np
import glob
import re

class trainer:
    def __init__(self, pathPattern):
        self.lastScore = 0
        self.turnsWithoutFood = 0
        self.version = self.getVersion(pathPattern)
        self.trainData = list()
        self.faultedState = False

    def trackedMove(self, length, score, left, right, top, bottom, headCoordinates, foodCoordinates, direction):
        if(direction == None): # get data to predict it.
            return (self.turnsWithoutFood, length, score, left, right, top, bottom, headCoordinates[0], headCoordinates[1], foodCoordinates[0], foodCoordinates[1], direction)

        if(score > self.lastScore and score > 10):
            self.turnsWithoutFood = 0
            self.lastScore = score
            self.flush()
        else:
            self.turnsWithoutFood += 1

        self.trainData.append((self.turnsWithoutFood, length, score, left, right, top, bottom, headCoordinates[0], headCoordinates[1], foodCoordinates[0], foodCoordinates[1], direction))
        return self.trainData[-1]
    
    def flush(self):
        df = pd.DataFrame(data = self.trainData)
        df.to_json('properData/snake_data_raw_v1_{0}_autogen.json'.format(self.version))
        print("Last stored value - ", self.trainData[-1])


    def getVersion(self, pathPattern):
        files = glob.iglob(pathPattern, recursive=False)
        return (max([int(re.search(r'_(\d+)[_autogen]*.json', file).group(1)) for file in files]) + 1)

