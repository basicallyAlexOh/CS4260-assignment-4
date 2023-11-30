from .node import SigmoidNode, RELUNode, InputNode, Node


class Layer:
    def __init__(self):
        self.nodes = []

    def forward(self):
        for node in self.nodes:
            node.forward()

    def backward(self):
        for node in self.nodes:
            node.backward()

    def adjustWeight(self, lr):
        for node in self.nodes:
            node.adjustWeight(lr)



class HiddenLayer(Layer):
    def __init__(self, size, type='sigmoid'):
        super().__init__()
        if type == 'sigmoid':
            for i in range(0,size):
                self.nodes.append(SigmoidNode())
        elif type == 'RELU':
            for i in range(0,size):
                self.nodes.append(RELUNode())



class InputLayer(Layer):
    def __init__(self, numInputs):
        super().__init__()
        for i in range(0, numInputs):
            self.nodes.append(InputNode())

    def forward(self, input):
        if len(input) != len(self.nodes):
            raise AttributeError("Mismatched size of input to input nodes")

        for i in range(0,len(self.nodes)):
            self.nodes[i].activation = input[i]


class OutputLayer(Layer):

    def __init__(self, numOutputs, type='sigmoid'):
        super().__init__()
        if type == 'sigmoid':
            for i in range(0, numOutputs):
                self.nodes.append(SigmoidNode())
        elif type == 'RELU':
            for i in range(0, numOutputs):
                self.nodes.append(RELUNode())


    def backward(self, target):
        for i in range(0, len(self.nodes)):
            self.nodes[i].delta = self.nodes[i].derivative(self.nodes[i].activation) * (target[i] - self.nodes[i].activation)



    def getOutputs(self):
        return self.nodes