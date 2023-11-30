"""
node.py
Classes: Node
Purpose: Defines a node in the graph.
"""
class Node:

    # __init__
    # Constructor: creates a node
    # Params: name (str), long (float), lat (float)
    def __init__(self, name: str, long: float, lat: float, pref: float):
        self.id = name
        self.longitude = long
        self.latitude = lat
        self.h = 0
        self.pref = pref



    # __str__
    # Gives the ID of the node
    # Returns: string
    def __str__(self):
        return self.id


    # __eq__
    # Checks equality of two nodes.
    # Equality is defined if the ID is the same.
    # Returns: bool
    def __eq__(self, other):
        if not isinstance(other, Node):
            return NotImplemented
        return self.id == other.id


    # __hash__
    # Makes our nodes hashable to be used in dictionaries.
    # Hashing is on the ID of the node.
    def __hash__(self):
        return hash(self.id)

    # time_at_location
    # Time spent on node
    # Returns: float
    def time_at_location(self):
        # Simply return the preference value as the time spent on edge
        # f(x) = x
        return self.pref