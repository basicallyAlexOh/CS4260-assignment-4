from .node import Node, categorize
from ..Dataloader.datum import Datum
class DecisionTree:

    def __init__(self, maxDepth):
        self.root = None
        # Default Max Depth is 5
        self.maxDepth = maxDepth

    def build(self, data: list[Datum]):
        self.root = Node(0)
        self.root.build(maxDepth=self.maxDepth, data=data)


    def predict(self, themes: Datum):
        return self.root.predict(themes)

    def evaluate(self, data: list[Datum]):
        numCorrect = 0
        for datum in data:
            predicted = self.predict(datum.themes)
            actual = categorize(datum.util)
            # print("Predicted: " + str(predicted) + "  Actual: " + str(actual))
            if predicted == actual:
                numCorrect += 1

        accuracy = numCorrect / len(data)
        return accuracy



