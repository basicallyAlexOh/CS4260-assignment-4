from .decisiontree import DecisionTree
from ..Dataloader.dataloader import Dataloader
class DTRunner:

    def __init__(self, numFolds: int, maxDepth: int):
        self.numFolds = numFolds
        self.maxDepth = maxDepth
        self.dt = None

    def run(self, trainSet, testSet):
            dt = DecisionTree(self.maxDepth)
            dt.build(trainSet)
            accuracy = dt.evaluate(testSet)
            return accuracy

    def getDecisionTree(self):
        return self.dt
