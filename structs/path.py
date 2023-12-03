"""
path.py
Classes: Path
Purpose: Defines a path of nodes and edges.
"""

from structs.node import Node
from structs.edge import Edge

class Path:

    # __init__
    # Constructor: creates a path with a single starting node
    # Param: startNode (Node)
    def __init__(self, startNode: Node, themes: list[str] = []):
        self.path = [startNode]
        self.edges = []
        self.weight = 0
        self.pref = startNode.pref
        self.themes = themes
        self.themeCount = [0] * len(themes)

        # Total time of trip so far
        self.time = startNode.time_at_location()
        # Time added to set of solutions
        self.solveTime = None

    # __len__
    # Implements len(). Gives the length of the path.
    # Returns: int
    def __len__(self):
        return len(self.path)

    # __iter__
    # Defines a starting iterator for the path.
    def __iter__(self):
        self.x = 0
        return self

    # __next__
    # Increments an iterator to make the Path class iterable
    def __next__(self):
        x = self.x
        if x >= len(self.path):
            raise StopIteration
        self.x = x + 1
        return self.path[x]

    # __lt__
    # Allows comparisons of paths
    # Can be called when priority queue has 2 of the same weights and paths must be compared.
    # A path is less than another path if it is HIGHER in preference.
    # Note: This allows for the priority queue to be in the correct order.
    # Returns: bool
    def __lt__(self, other):
        if not isinstance(other, Path):
            raise Exception("Trying to compare Path with another type")
        return self.pref > other.pref

    # __str__
    # Gives a string with node IDs separated by a character of whitespace
    # Returns: string
    def __str__(self):
        ret = ""
        for node in self.path:
            ret += str(node) + " "
        return ret


    # getLastNode (Public)
    # Retrieves the last node in the path.
    # Returns: Node
    def getLastNode(self):
        return self.path[-1]

    # addEdge (Public)
    # Adds an edge to the path and updates the list of nodes and list of edges.
    # Params: e (Edge)
    def addEdge(self, e: Edge):

        self.weight += e.weight
        self.time += e.weight/e.speed

        newEdgePref = e.pref
        if e not in self.edges:
            factor = self.calculate_multiplier(e)
            newEdgePref *= factor
            self.pref += newEdgePref
            self.time += e.time_on_edge()
        else:
            newEdgePref = 0

        newNodePref = e.end.pref
        if e.end not in self.path or e.end == self.path[0]:
            factor = self.calculate_multiplier(e.end)
            newNodePref *= factor
            self.pref += e.end.pref * factor
            self.time += e.end.time_at_location()
        else:
            newNodePref = 0

        newNode = Node(e.end.id, e.end.longitude, e.end.latitude, newNodePref, e.end.attractions)
        newEdge = Edge(e.label, e.start, newNode, e.weight, newEdgePref, e.attractions, e.speed)

        self.track_themes(e)
        self.track_themes(e.end)
        self.path.append(newNode)
        self.edges.append(newEdge)


    # time_estimate (Public)
    # Amount of time spent on the path
    # Returns; float
    def time_estimate(self):
        return self.time


    def track_themes(self, loc):
        for attraction in loc.attractions:
            listOfThemes = attraction[1]
            for theme in listOfThemes:
                if theme in self.themes:
                    self.themeCount[self.themes.index(theme)] += 1

    def calculate_multiplier(self, loc):
        multiplier = 1
        for attraction in loc.attractions:
            listOfThemes = attraction[1]
            for theme in listOfThemes:
                if theme in self.themes:
                    # Penalize for
                    multiplier *= (0.9)**(self.themeCount[self.themes.index(theme)])
        return multiplier