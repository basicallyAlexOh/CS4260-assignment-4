"""
solver.py
Classes: AStarSolver
Purpose: Defines how the solver should solve for paths from the start location to the end location.
"""
import copy

from utils.dataloader import *
from structs.graph import Graph
from structs.path import Path
from utils.timer import Timer

from queue import PriorityQueue
import sys


class Solver:

    def __init__(self, locFilePath: str, edgeFilePath: str, prefFilePath: str, startLoc: str, goal: str, resultFilePath: str,
                 speed: float = 0.0):
        dataloader = Dataloader(locFilePath, edgeFilePath, prefFilePath, speed)
        self.graph = Graph(dataloader, goal=goal)
        self.start = None

        for node in self.graph.getNodes():
            if node.id == startLoc:
                self.start = node
                break

        self.discovered = {node: False for node in self.graph.getNodes()}
        self.solutions = []
        self.frontier = PriorityQueue()
        self.timer = Timer()
        self.resultFile = open(resultFilePath, "w+")

    # solutionSummary (Private)
    # Finds the min, max, and average cost of solutions
    # Return: (min, max, avg)
    def solutionSummary(self):
        totalSum = 0
        minCost = self.solutions[0].weight
        maxCost = self.solutions[0].weight
        for path in self.solutions:
            totalSum += path.weight
            minCost = min(minCost, path.weight)
            maxCost = max(maxCost, path.weight)
        avgCost = totalSum / len(self.solutions)
        return minCost, maxCost, avgCost

    # findMinSolution (Private)
    # Finds the ID of the minimum solution
    # Returns: int
    def findMinSolution(self):
        minCost = self.solutions[0].weight
        id = 0
        for i in range(0, len(self.solutions)):
            if self.solutions[i].weight < minCost:
                minCost = self.solutions[i].weight
                id = i
        return id

    # visitedNodes (Private)
    # Lists the nodes that have been visited separated by one character of whitespace
    # Returns: string
    def visitedNodes(self):
        ret = ""
        for node in self.discovered:
            if self.discovered[node]:
                ret += node.id + " "
        return ret

    # printSummary (Private)
    # Prints the summary to output
    # Params: output (default = sys.stdout)
    def printSummary(self, output=sys.stdout):
        print("Size of Frontier: " + str(self.frontier.qsize()), file=output)
        (minCost, maxCost, avgCost) = self.solutionSummary()
        print("Min Cost: " + str(minCost) + "\nAverage Cost: " + str(avgCost) + "\nMax Cost: " + str(maxCost),
              file=output)
        print("Solution ID of Min Cost: " + str(self.findMinSolution()), file=output)
        print("Visited Nodes: " + self.visitedNodes(), file=output)

        for path in self.solutions:
            output.write("\n")
            self.pathSummary(p=path, output=output)
            print(str(path.solveTime), file=output)

    # pathSummary (Private)
    # Outputs the summary of a single path
    # Params: output (default = sys.stdout)
    def pathSummary(self, p: Path, output=sys.stdout):
        print("Solution #%d : %s %d" % (self.solNumber, str(p.path[0]), p.path[0].h), file=output)
        self.solNumber += 1
        curG = 0
        for edge in p.edges:
            curG += edge.weight
            print(str(edge) + " " + str(curG) + " " + str(edge.end.h), file=output)

    # promptContinue (Private)
    # Asks user for a response to continue the search or not
    # Returns: bool
    def promptContinue(self):
        response = input("Would you like to continue? [yes/no]")
        if response.lower() == "yes":
            return True
        elif response.lower() == "no":
            return False
        print("Invalid response... please try again\n")
        return self.promptContinue()

    def solve(self):
        raise Exception("Cannot call Solve() on an abstract class")


class AStarSolver(Solver):
    # static variable to keep track of solution number
    solNumber = 0

    # init
    # Constructor - instantiates an object of AStarSolver
    def __init__(self, locFilePath: str, edgeFilePath: str, startLoc: str, goal: str, resultFilePath: str):
        super().__init__(locFilePath, edgeFilePath, startLoc, goal, resultFilePath)

    # solve (Public)
    # Solves the graph using anytime A* and gives unique paths to the ending location
    # Returns: list of paths
    def solve(self):
        continueSearch = True

        adj = self.graph.getAdjList()

        self.timer.start()

        self.frontier.put((self.start.h, Path(self.start)))
        while not self.frontier.empty():
            (f, curPath) = self.frontier.get()
            curNode = curPath.getLastNode()

            self.discovered[curNode] = True

            if curNode == self.graph.getGoal():
                self.timer.pause()
                curPath.time = self.timer.get()
                self.solutions.append(curPath)
                print("Solution Found!")
                continueSearch = self.promptContinue()
                if not continueSearch:
                    self.printSummary()
                    self.solNumber = 0
                    self.printSummary(output=self.resultFile)
                    break
                self.timer.resume()

            for edge in adj[curNode]:
                (nextNode, w) = (edge.end, edge.weight)
                if nextNode not in curPath:
                    newPath = copy.deepcopy(curPath)
                    newPath.addEdge(edge)
                    newf = curPath.weight + nextNode.h
                    self.frontier.put((newf, newPath))

        print("Search has terminated... ")

        if len(self.solutions) == 0:
            print("no solutions found...")

        if continueSearch:
            print("Printing Results:")
            self.printSummary()
            self.solNumber = 0
            self.printSummary(output=self.resultFile)

        return self.solutions


class UtilityDrivenSolver(Solver):
    # static variable to keep track of solution number
    solNumber = 0

    # init
    def __init__(self, locFilePath: str, edgeFilePath: str, prefFilePath: str, startLoc: str, goal: str, resultFilePath: str,
                 maxTime: float, x_mph: float):
        super().__init__(locFilePath, edgeFilePath, prefFilePath, startLoc, goal, resultFilePath, x_mph)
        self.maxTime = maxTime
        self.themes = list(csv.reader(open(prefFilePath, 'r'), delimiter='\t'))[0][1:]

    def pathSummary(self, p: Path, output=sys.stdout):
        print("Solution #%d : %s" % (self.solNumber, str(p.path[0])), file=output)
        self.solNumber += 1
        for edge in p.edges:
            print(str(edge), file=output)
        print("Total Time of Trip: " + str(p.time) + "\t Total Preference of Trip: " + str(p.pref), file=output)


    def printSummary(self, output=sys.stdout):
        print("Size of Frontier: " + str(self.frontier.qsize()), file=output)
        (minPref, maxPref, avgPref) = self.solutionSummary()
        print("Min Pref: " + str(minPref) + "\nAverage Pref: " + str(avgPref) + "\nMax Pref: " + str(maxPref),
              file=output)
        print("Solution ID of Max Pref: " + str(self.findMaxSolution()), file=output)
        print("Visited Nodes: " + self.visitedNodes(), file=output)
        print("Total Runtime: " + str(self.timer.get()), file=output)

        for path in self.solutions:
            output.write("\n")
            self.pathSummary(p=path, output=output)
            print(str(path.solveTime), file=output)

    def solutionSummary(self):
        totalPref = 0
        minPref = self.solutions[0].pref
        maxPref = self.solutions[0].pref
        for path in self.solutions:
            totalPref += path.pref
            minPref = min(minPref, path.pref)
            maxPref = max(maxPref, path.pref)
        avgPref = totalPref / len(self.solutions)
        return minPref, maxPref, avgPref

    # findMinSolution (Private)
    # Finds the ID of the minimum solution
    # Returns: int
    def findMaxSolution(self):
        maxPref = self.solutions[0].pref
        id = 0
        for i in range(0, len(self.solutions)):
            if self.solutions[i].pref > maxPref:
                maxPref = self.solutions[i].pref
                id = i
        return id

    # solve (Public)
    # Solves the graph using anytime A* and gives unique paths to the ending location
    # Returns: list of paths
    def solve(self):
        continueSearch = True

        adj = self.graph.getAdjList()

        self.timer.start()
        self.frontier.put(Path(self.start, self.themes))
        while not self.frontier.empty():
            curPath = self.frontier.get()
            curNode = curPath.getLastNode()

            self.discovered[curNode] = True

            if curNode == self.graph.getGoal() and len(curPath) != 1:
                self.timer.pause()
                curPath.solveTime = self.timer.get()
                self.solutions.append(curPath)
                print("Solution Found!")
                continueSearch = self.promptContinue()
                if not continueSearch:
                    self.printSummary()
                    self.solNumber = 0
                    self.printSummary(output=self.resultFile)
                    break
                self.timer.resume()
                continue

            for edge in adj[curNode]:
                newPath = copy.deepcopy(curPath)
                newPath.addEdge(edge)
                if newPath.time_estimate() <= self.maxTime:
                    self.frontier.put(newPath)

        print("Search has terminated... ")

        if len(self.solutions) == 0:
            print("no solutions found...")

        if continueSearch:
            print("Printing Results:")
            self.printSummary()
            self.solNumber = 0
            self.printSummary(output=self.resultFile)

        return self.solutions
