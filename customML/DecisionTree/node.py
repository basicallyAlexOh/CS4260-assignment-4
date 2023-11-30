from ..Dataloader.datum import Datum
from math import log2

class Node:
    def __init__(self, depth: int):
        self.left = None
        self.right = None
        self.depth = depth
        self.testVar = None
        self.testSplit = None
        self.terminal = False


    def build(self, maxDepth: int, data: list[Datum]):
        (self.testVar, self.testSplit) = self.__selectFN(data)
        leftData = []
        rightData = []
        for datum in data:
            if self.getBranch(datum):
                leftData.append(datum)
            else:
                rightData.append(datum)

        if self.depth == maxDepth or len(leftData) == 0 or len(rightData) == 0:
            self.terminal = True
            if len(leftData) != 0:
                self.left = TerminalNode(self.depth+1)
                self.left.build(maxDepth, leftData)
            if len(rightData) != 0:
                self.right = TerminalNode(self.depth+1)
                self.right.build(maxDepth, rightData)


        else:
            self.left = Node(self.depth+1)
            self.left.build(maxDepth, leftData)
            self.right = Node(self.depth+1)
            self.right.build(maxDepth, rightData)

    def __selectFN(self, data: list[Datum]):
        numThemes = len(data[0].themes)
        minVal = None
        bestTheme = None
        bestSplit = None
        for themeNum in range(0,numThemes):
            for split in range(0,10):
                val = self.computeDiversity(data, themeNum, split)
                if minVal is None or val < minVal:
                    minVal = val
                    bestTheme = themeNum
                    bestSplit = split


        return bestTheme, bestSplit

    def computeDiversity(self, data: list[Datum], theme, split):
        totalCount = len(data)
        leftCount = 0
        rightCount = 0
        leftCategoryCount = [0,0,0,0,0]
        rightCategoryCount = [0,0,0,0,0]

        for datum in data:
            if datum.themes[theme] < split:
                leftCount += 1
                leftCategoryCount[categorize(datum.util)] += 1
            else:
                rightCount += 1
                rightCategoryCount[categorize(datum.util)] += 1



        for i in range(0,5):
            leftCategoryCount[i] = 0 if leftCategoryCount[i] == 0 else leftCategoryCount[i]/leftCount * abs(log2(leftCategoryCount[i]/leftCount))
            rightCategoryCount[i] = 0 if rightCategoryCount[i] == 0 else rightCategoryCount[i]/rightCount * abs(log2(rightCategoryCount[i]/rightCount))


        leftSum = sum(leftCategoryCount)
        rightSum = sum(rightCategoryCount)
        return (leftCount/totalCount) * leftSum + (rightCount/totalCount) * rightSum

    def getBranch(self, datum : Datum):
        # NOTE: Left = True, Right = False
        testVal = datum.themes[self.testVar]
        if testVal < self.testSplit:
            return True
        else:
            return False


    def predict(self, themes):
        testVal = themes[self.testVar]
        if testVal < self.testSplit or self.right is None:
            return self.left.predict(themes)
        else:
            return self.right.predict(themes)

class TerminalNode(Node):
    def __init__(self, depth):
        super().__init__(depth)
        self.classification = None

    def build(self, maxDepth: int, data: list[Datum]):
        categoryCount = [0,0,0,0,0]
        for datum in data:
            categoryCount[categorize(datum.util)] += 1
        self.classification = categoryCount.index(max(categoryCount))

    def predict(self, themes):
        return self.classification


def categorize(util: float):
    if util < 0.2:
        return 0
    elif util < 0.4:
        return 1
    elif util < 0.6:
        return 2
    elif util < 0.8:
        return 3
    else:
        return 4