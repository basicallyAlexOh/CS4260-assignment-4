"""
graph.py
Classes: Graph
Purpose: Denotes the structure of the graph and builds the adjacency list.
"""


from collections import defaultdict
from math import sin, cos, asin, sqrt, radians
from structs.node import Node
from structs.edge import Edge

from utils.dataloader import Dataloader


class Graph:


    # __init__
    # Constructor - instantiates an object of Graph
    # Params: dataloader (Dataloader), goal (string)
    def __init__(self, dataloader: Dataloader, goal=None):
        self.__nodes = []
        self.__adj = defaultdict(list)
        self.__buildGraph(dataloader)
        self.__goal = None
        self.__setGoal(goal)


    # buildGraph (Private)
    # Builds the graph with the given dataloader
    # Params: dataloader (Dataloader)
    def __buildGraph(self, dataloader: Dataloader):
        self.__nodes = dataloader.nodeList
        for e in dataloader.edgeList:
            label, u,v,w, pref, speed = e.label, e.start, e.end, e.weight, e.pref, e.speed
            self.__adj[u].append(Edge(label,u,v,w,pref, speed))
            self.__adj[v].append(Edge(label,v,u,w,pref, speed))


    # setGoal (Private)
    # Finds the goal node given the name
    # Params: goalLoc (string)
    # Exceptions: Will raise exception if the location is not found.
    def __setGoal(self, goalLoc: str):
        if goalLoc == None:
            # Goal is not needed
            return

        found = False
        for node in self.__nodes:
            if goalLoc == node.id:
                self.__goal = node
                self.__computeHeuristic()
                found = True
                break

        if not found:
            raise Exception("Invalid goal...")

    # computeHeuristic (Private)
    # Iterates through all nodes defined in the graph and computes their H value
    def __computeHeuristic(self):
        for node in self.__nodes:
            node.h = self.computeDistance(node, self.__goal)
        for key in self.__adj:
            for edge in self.__adj[key]:
                edge.start.h = self.computeDistance(edge.start, self.__goal)
                edge.end.h = self.computeDistance(edge.end, self.__goal)


    # getNodes (Public)
    # Returns: list of nodes
    def getNodes(self):
        return self.__nodes

    # getAdjList (Public)
    # Returns: Dictionary hashed by nodes that points to list of edges
    def getAdjList(self):
        return self.__adj

    # getGoal
    # Returns: the goal node
    def getGoal(self):
        return self.__goal

    # computeDistance (Public, Static)
    # Gives the heuristic distance estimate based on spherical geometry in miles.
    # Returns: int
    @staticmethod
    def computeDistance(node1: Node, node2: Node):
        # Taken from the following post
        # https://www.geeksforgeeks.org/program-distance-two-points-earth/
        lon1, lat1 = radians(node1.longitude), radians(node1.latitude)
        lon2, lat2 = radians(node2.longitude), radians(node2.latitude)

        dlon = lon2 - lon1
        dlat = lat2 - lat1
        a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2

        c = 2 * asin(sqrt(a))

        # Radius of earth in kilometers. Use 3956 for miles
        r = 3956

        # calculate the result
        return (c * r)