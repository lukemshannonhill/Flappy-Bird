from enum import Enum


class NodeGene:
    def __init__(self, id, type):
        self.id = id
        self.type = type

    def __repr__(self):
        return "Node ID: {}\tType: {}\n".format(self.id, self.type)


class Type(Enum):
    INPUT = 1
    HIDDEN = 2
    OUTPUT = 3
