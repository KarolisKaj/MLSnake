import pandas as pd 

class trainer:
    def __init__(self):
        self.lastScore = 0
        self.turnsWithoutFood = 0
        self.trainData = list()

    def trackedMove(self, length, score, left, right, top, bottom, headCoordinates, foodCoordinates, direction):
        if(score > self.lastScore):
            self.turnsWithoutFood = 0
            self.lastScore = score
            self.trainData.append((self.turnsWithoutFood, length, score, left, right, top, bottom, headCoordinates[0], headCoordinates[1], foodCoordinates[0], foodCoordinates[1], direction))
            self.flush()
        else:
            self.turnsWithoutFood += 1

        self.trainData.append((self.turnsWithoutFood, length, score, left, right, top, bottom, headCoordinates[0], headCoordinates[1], foodCoordinates[0], foodCoordinates[1], direction))
        print(self.trainData[-1])
    
    def flush(self):
        df = pd.DataFrame(data = self.trainData)
        df.to_json('snake_data_raw_v1.json')

    #def storeData(self, starvation, length, scoreDif, left, right, top, bottom, headCoordinates, foodCoordinates):



