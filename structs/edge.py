"""
edge.py
Classes: Edge
Purpose: Defines a directed edge in the graph.
"""

from structs.node import Node

class Edge:
    def __init__(self, label: str, start: Node, end: Node, weight: int, pref: float, attractions: list, speed: float = 0.0):
        self.start = start
        self.end = end
        self.weight = weight
        self.label = label
        self.pref = pref
        self.attractions = attractions
        self.speed = speed


    def __str__(self):
        ret = str(self.start) + " to " + str(self.end) + "  Edge Pref: " + str(self.pref) + "\n "
        ret += "\t Time on Edge: " + str(self.time_on_edge()) + "\n "
        ret += "\t Destination Pref: " + str(self.end.pref) + "  Time at Destination: " + str(self.end.time_at_location()) + "\n"
        ret += "\t Attractions on Edge: " + str(self.attractions) + "\n"
        ret += "\t Attractions at Destination: " + str(self.end.attractions) + "\n"
        return ret

    def __eq__(self, other):
        if not isinstance(other, Edge):
            return NotImplemented
        return self.label == other.label

    def time_on_edge(self):
        # Simply return the preference value as the time spent on edge
        # f(x) = x
        return self.pref + self.weight / self.speed