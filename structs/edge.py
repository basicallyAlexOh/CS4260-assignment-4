"""
edge.py
Classes: Edge
Purpose: Defines a directed edge in the graph.
"""

from structs.node import Node

class Edge:
    def __init__(self, label: str, start: Node, end: Node, weight: int, pref: float, speed: float = 0.0):
        self.start = start
        self.end = end
        self.weight = weight
        self.label = label
        self.pref = pref
        self.speed = speed


    def __str__(self):
        ret = str(self.start) + " " + str(self.end) + " " + self.label + " " + str(self.pref) + " " + str(self.weight / self.speed) + " " + str(self.end.pref) + " " + str(self.end.time_at_location())
        return ret

    def __eq__(self, other):
        if not isinstance(other, Edge):
            return NotImplemented
        return self.label == other.label

    def time_on_edge(self):
        # Simply return the preference value as the time spent on edge
        # f(x) = x
        return self.pref