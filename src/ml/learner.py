import pandas as pd 

class learner:
    def __init__(self, trainingSetPath):
        self.df = pd.read_json(trainingSetPath)

    def getModel():


