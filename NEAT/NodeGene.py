from enum import Enum


class NodeGene:
    def __init__(self, id, type):
        """
        Node gene constructor that takes an ID and node type as input
        :param id: ID of the node to be created
        :param type: Type of the node to be created
        """
        self.id = id
        self.type = type
        self.output = None

    def fire_neuron(self):
        pass

    def __repr__(self):
        return "Node ID: {}\tType: {}\tOutput: {}\n".format(self.id, self.type, self.output)


class Type(Enum):
    """
    Input Node, Hidden Node, Output Node
    """
    INPUT = 1
    HIDDEN = 2
    OUTPUT = 3
