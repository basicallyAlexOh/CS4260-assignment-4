from .layer import Layer, InputLayer, HiddenLayer, OutputLayer
from ..Dataloader.dataloader import Dataloader
from ..Dataloader.datum import Datum
from .node import Node
from .edge import Edge

class NeuralNetwork:
    def __init__(self, numInputs, hiddenLayers, numOutputs):
        self.inputLayer = InputLayer(numInputs)
        self.hiddenLayers = []
        for layerSizes in hiddenLayers:
            self.hiddenLayers.append(HiddenLayer(layerSizes))
        self.outputLayer = OutputLayer(numOutputs)

        if len(hiddenLayers) == 0:
            self.__connectLayers(self.inputLayer, self.outputLayer)

        else:
            self.__connectLayers(self.inputLayer, self.hiddenLayers[0])
            for i in range(0, len(self.hiddenLayers)-1):
                self.__connectLayers(self.hiddenLayers[i], self.hiddenLayers[i+1])
            self.__connectLayers(self.hiddenLayers[-1], self.outputLayer)

    def __connectLayers(self, fromLayer: Layer, toLayer: Layer):
        for source in fromLayer.nodes:
            for to in toLayer.nodes:
                self.__addEdge(source, to)
    def __addEdge(self, source: Node, to: Node):
        e = Edge(source, to)
        source.outputEdges.append(e)
        to.inputEdges.append(e)


    def train(self, trainData: list[Datum], lr=0.05):
        for datum in trainData:
            inputs = datum.themes
            target = [datum.util]
            self.forward(inputs)
            self.backward(target, lr)


    def predict(self, input: list[int]):
        self.forward(input)
        outputs = [node.activation for node in self.outputLayer.nodes]
        return outputs

    def evaluate(self, data):
        MSE = 0
        for datum in data:
            predicted = self.predict(datum.themes)
            target = [datum.util]
            for i in range(0, len(self.outputLayer.nodes)):
                MSE += (target[i] - predicted[i])**2
        MSE /= len(data)
        return MSE





    def forward(self, inputs):
        self.inputLayer.forward(inputs)
        for layer in self.hiddenLayers:
            layer.forward()
        self.outputLayer.forward()

    def backward(self, target, lr):
        self.outputLayer.backward(target)
        for layer in self.hiddenLayers:
            layer.backward()

        self.outputLayer.adjustWeight(lr)
        for layer in self.hiddenLayers:
            layer.adjustWeight(lr)


