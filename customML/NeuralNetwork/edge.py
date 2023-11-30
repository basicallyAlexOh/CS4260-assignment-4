from .node import Node
import random
class Edge:
    def __init__(self, source: Node, to: Node, weight: float = random.random()):
        self.source = source
        self.to = to
        self.weight = weight


