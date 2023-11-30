import copy
import matplotlib.pyplot as plt
import numpy as np

from .neuralnetwork import NeuralNetwork

class NNRunner:
    def __init__(self, numFolds: int, numInputs: int, hiddenLayers: list[int], numOutputs: int, epochs : int = 200, lr: float = 0.05):
        self.numFolds = numFolds
        self.numInputs = numInputs
        self.hiddenLayers = hiddenLayers
        self.numOutputs = numOutputs
        self.epochs = epochs
        self.lr = lr

        self.bestModel = None
        self.bestNSE = None
        self.bestEpoch = None
        self.errorList = []

    def getBestNN(self):
        return self.bestModel

    def plotTrainingCurve(self):
        plt.plot(np.arange(0,self.epochs), self.errorList)
        plt.show()

    def run(self, trainSet, testSet):

        nn = NeuralNetwork(self.numInputs, self.hiddenLayers, self.numOutputs)
        for i in range(0, self.epochs):
            nn.train(trainSet, self.lr)
            MSE = nn.evaluate(testSet)
            self.errorList.append(MSE)
            if self.bestModel is None or self.bestMSE is None or MSE < self.bestMSE:
                # Save the model
                self.bestModel = copy.deepcopy(nn)
                self.bestMSE = MSE
                self.bestEpoch = i
