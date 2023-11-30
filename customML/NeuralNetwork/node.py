from math import exp

class Node:
    def __init__(self):
        self.inputSum = 0
        self.activation = 0
        self.inputEdges = []
        self.outputEdges = []
        self.delta = 0

    def activate(self):
        raise NotImplemented("Base Node class has no activation")

    def derivative(self, x):
        raise NotImplemented("Base Node class has no derivative")

    def forward(self):
        curSum = 0
        for edge in self.inputEdges:
            curSum += edge.source.activation * edge.weight
        self.inputSum = curSum
        self.activate()

    def backward(self):
        deriv = self.derivative(self.activation)
        sum = 0
        for edge in self.outputEdges:
            sum += edge.to.delta * edge.weight
        self.delta = sum * deriv

    def adjustWeight(self, lr):
        for edge in self.inputEdges:
            change = lr * self.delta * edge.source.activation
            edge.weight += change



class SigmoidNode(Node):
    def __init__(self):
        super().__init__()

    def activate(self):
        self.activation = self.sigmoid(self.inputSum)

    def derivative(self, x):
        return self.sigmoid(x) * (1-self.sigmoid(x))

    @staticmethod
    def sigmoid(x):
        return 1 / (1+exp(-x))


class InputNode(Node):
    def __init__(self):
        super().__init__()



class RELUNode(Node):
    def __init__(self):
        super().__init__()

    def derivative(self, x):
        return 1 if x >= 0 else 0

