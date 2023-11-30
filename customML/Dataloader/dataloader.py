
import csv
from .datum import Datum
import random
class Dataloader:

    def __init__(self, path: str):
        self.path = path
        self.utilList = []
        self.__build()

    def __len__(self):
        return len(self.utilList)

    def splitSet(self, iter: int, numFolds: int):
        if iter >= numFolds:
            raise IndexError("Iteration number greater than number of folds")

        start = len(self.utilList) // numFolds * iter
        if iter == numFolds -1:
            end = len(self.utilList)
        else:
            end = start + len(self.utilList) // numFolds

        trainSet = self.utilList[0:start] + self.utilList[end:len(self.utilList)]
        testSet = self.utilList[start:end]
        return (trainSet, testSet)


    def randomize(self):
        random.shuffle(self.utilList)

    def __build(self):
        # with open(self.path, 'r', encoding='utf-16') as csv_file:
        with open(self.path, 'r') as csv_file:
            csv_reader = csv.reader(csv_file, delimiter='\t')
            for row in csv_reader:
                try:
                    util = float(row[0])
                    themes = [int(a) for a in row[1:]]
                    self.utilList.append(Datum(util, themes))
                except:
                    print("invalid row")
