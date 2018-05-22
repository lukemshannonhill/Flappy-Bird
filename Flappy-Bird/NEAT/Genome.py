import random

import numpy as np

from NEAT.ConnectionGene import ConnectionGene
from NEAT.InnovationNumberGenerator import InnovationNumberGenerator
from NEAT.NodeGene import Type, NodeGene

"""
Based on the paper: Evolving Neural Networks through Augmenting Topologies
"""


class Genome:
    def __init__(self, connection_genes, input_nodes=2, output_nodes=1, fitness=0):
        """
        Constructor for the genome object
        :param connection_genes: Dictionary of connection genes
        :param input_nodes: Number of input nodes
        :param output_nodes: Number of output nodes
        :param fitness: Fitness of this genome
        """
        self.connection_genes = connection_genes  # Dictionary of (innovation_number: ConnectionGene)
        self.input_nodes = self.generate_input_nodes(input_nodes)
        self.output_nodes = self.generate_output_nodes(output_nodes)
        self.hidden_nodes = self.generate_hidden_nodes()  # List of Tuple(id)
        self.nodes = {**self.input_nodes, **self.hidden_nodes, **self.output_nodes}  # Dictionary of (node_id: NodeGene)
        self.innovation_number_generator = InnovationNumberGenerator(self.get_last_innovation_number())
        self.fitness = fitness
        self.global_rank = 0

    def total_nodes(self):
        """
        Return sum of input nodes, hidden nodes and output nodes
        :return: The total count of all nodes in this genome
        """
        return len(self.nodes)

    def get_last_innovation_number(self):
        """
        Gets the last used innovation number for this genome
        :return: Innovation number which was last used
        """
        return max(self.connection_genes.keys())

    def generate_hidden_nodes(self):
        """
        Generates hidden node objects using the connection genes
        :return: Dictionary of nodes keyed by node id
        """
        nodes = dict()
        for connection in self.connection_genes:
            connection = self.connection_genes[connection]
            in_node_exists = False
            if connection.in_node in self.input_nodes or connection.in_node in self.output_nodes:
                in_node_exists = True

            out_node_exists = False
            if connection.out_node in self.input_nodes or connection.out_node in self.output_nodes:
                out_node_exists = True

            if not in_node_exists:
                node = NodeGene(connection.in_node, Type.HIDDEN)
                if node.id not in nodes:
                    nodes[node.id] = node
            if not out_node_exists:
                node = NodeGene(connection.out_node, Type.HIDDEN)
                if node.id not in nodes:
                    nodes[node.id] = node
        return nodes

    def add_connection_mutation(self):
        """
        Modifies the existing connection genes by adding a new connection between two unconnected nodes
        or if connection exists, does nothing
        """
        node_1 = self.nodes[random.choice(list(self.nodes.keys()))]
        node_2 = self.nodes[random.choice(list(self.nodes.keys()))]
        while node_1 == node_2:
            node_2 = self.nodes[random.choice(list(self.nodes.keys()))]

        reversed = False
        if node_1.type == Type.OUTPUT and (node_2.type == Type.HIDDEN or node_2.type == Type.INPUT):
            reversed = True

        if node_1.type == Type.HIDDEN and node_2.type == Type.INPUT:
            reversed = True

        if reversed:
            return

        connection_exists = False
        for connection_gene in self.connection_genes:
            connection_gene = self.connection_genes[connection_gene]
            if connection_gene.in_node == node_1.id and connection_gene.out_node == node_2.id:
                connection_exists = True
                break
            if connection_gene.in_node == node_2.id and connection_gene.out_node == node_1.id:
                connection_exists = True
                break

        if connection_exists:
            return

        new_connection = ConnectionGene(in_node=node_2.id if reversed else node_1.id,
                                        out_node=node_1.id if reversed else node_2.id,
                                        weight=np.random.uniform(),
                                        enabled=True,
                                        innovation_number=self.innovation_number_generator.next_int())
        self.connection_genes[new_connection.innovation_number] = new_connection

    def add_node_mutation(self):
        """
        Adds a new node between a existing connection as shown below
        o =========== 0    Old connection
        o ==== o ==== o    New connections
        """
        old_connection = ConnectionGene(1, 4, 1, True,
                                        self.connection_genes[random.choice(list(self.connection_genes.keys()))])

        in_node = old_connection.in_node
        out_node = old_connection.out_node

        new_node = NodeGene(self.total_nodes() + 1, Type.HIDDEN)
        old_connection.enabled = False

        new_connection_1 = ConnectionGene(in_node=in_node,
                                          out_node=new_node.id,
                                          weight=1.0,
                                          enabled=True,
                                          innovation_number=self.innovation_number_generator.next_int())

        new_connection_2 = ConnectionGene(in_node=new_node.id,
                                          out_node=out_node,
                                          weight=old_connection.weight,
                                          enabled=True,
                                          innovation_number=self.innovation_number_generator.next_int())

        self.connection_genes[new_connection_1.innovation_number] = new_connection_1
        self.connection_genes[new_connection_2.innovation_number] = new_connection_2

        self.nodes[new_node.id] = new_node

    @staticmethod
    def get_matching_connections(parent_1_genome, parent_2_genome):
        """
        Finds the connections between the two genomes which have the same innovation number
        Refer Figure 4 in the paper
        :param parent_1_genome: The genome for 1st parent
        :param parent_2_genome: The genome for 2nd parent
        :return: Dictionary of all the matching connections
        """
        matching_connections = dict()
        parent_1_connections = parent_1_genome.connection_genes
        parent_2_connections = parent_2_genome.connection_genes
        for k, v in parent_1_connections.items():
            if k in parent_2_connections:
                matching_connections[k] = v if np.random.uniform() < 0.5 else parent_2_connections[k]
        return matching_connections

    @staticmethod
    def get_disjoint_connections(parent_1_genome, parent_2_genome):
        """
        Finds the connections between the two genomes are unique in both genomes
        Refer Figure 4 in the paper
        :param parent_1_genome: The genome for 1st parent
        :param parent_2_genome: The genome for 2nd parent
        :return: Dictionary of all the disjoint connections
        """
        disjoint_connections = dict()

        #   Make parent 1 the longest of both
        if len(parent_1_genome.connection_genes) > len(parent_2_genome.connection_genes):
            parent_1_genome, parent_2_genome = parent_1_genome, parent_2_genome
        else:
            parent_1_genome, parent_2_genome = parent_2_genome, parent_1_genome

        parent_1_connections = parent_1_genome.connection_genes
        parent_2_connections = parent_2_genome.connection_genes

        for k, v in parent_1_connections.items():
            if parent_2_connections.get(k) is not None:
                continue
            else:
                if k < parent_2_genome.get_last_innovation_number():
                    disjoint_connections[k] = v
        for k, v in parent_2_connections.items():
            if parent_1_connections.get(k) is not None:
                continue
            else:
                disjoint_connections[k] = v
        return disjoint_connections

    @staticmethod
    def get_excess_connections(parent_1_genome, parent_2_genome):
        """
        Finds the connections between the two genomes which are out of bounds in either of the genomes
        Refer Figure 4 in the paper
        :param parent_1_genome: The genome for 1st parent
        :param parent_2_genome: The genome for 2nd parent
        :return: Dictionary of all the excess connections
        """
        excess_connections = dict()

        #   Make parent 1 the longest of both
        if parent_1_genome.get_last_innovation_number() > parent_2_genome.get_last_innovation_number():
            parent_1_genome, parent_2_genome = parent_1_genome, parent_2_genome
        else:
            parent_1_genome, parent_2_genome = parent_2_genome, parent_1_genome

        # Only longest genes will have excess genes
        parent_1_connections = parent_1_genome.connection_genes
        for k, v in parent_1_connections.items():
            if k > parent_2_genome.get_last_innovation_number():
                excess_connections[k] = v

        return excess_connections

    def print_genome(self):
        """
        Prints the genotype of the genome
        """
        return_string = ""
        return_string += "----------------------\n"

        for k, v in self.nodes.items():
            return_string += v.__repr__()
        for k, v in self.connection_genes.items():
            return_string += v.__repr__()
        return_string += "----------------------"
        return return_string

    @staticmethod
    def get_compatibility_distance(parent_1_genome, parent_2_genome):
        """
        Gets the compatibility distance between the two genomes which is a measure of how different the two
        genomes are.

        Formula: d = ((c1 * E) + (c2 * D)) / N + (c3 * W)
        c1, c2, c3 are constants with values 1.0, 1.0, 0.4 (Values from paper. Section 4.1)
        E = Number of matching genes
        D = Number of disjoint genes
        W = Average weight difference of the matching genes
        Refer section 3.3 of paper

        :param parent_1_genome: The genome of 1st parent
        :param parent_2_genome: The genome of 2nd parent
        :return: Compatibility distance
        """

        E = len(Genome.get_excess_connections(parent_1_genome, parent_2_genome))
        D = len(Genome.get_disjoint_connections(parent_1_genome, parent_2_genome))
        W = Genome.get_average_weight_difference_of_matching_genes(parent_1_genome, parent_2_genome)
        N = 1 if len(parent_1_genome.connection_genes) < 20 and len(parent_2_genome.connection_genes) < 20 else len(
            parent_1_genome.connection_genes) if len(parent_1_genome.connection_genes) > len(
            parent_2_genome.connection_genes) else len(parent_1_genome.connection_genes)

        c1 = 1.0
        c2 = 1.0
        c3 = 0.4
        d = ((c1 * E) + (c2 * D)) / N + (c3 * W)
        return d

    @staticmethod
    def get_average_weight_difference_of_matching_genes(parent_1_genome, parent_2_genome):
        """
        Gets the average weight distance between the two genomes
        :param parent_1_genome: The genome of 1st parent
        :param parent_2_genome: The genome of 2nd parent
        :return: Average weight distance
        """
        matching_connections = 0
        weight_difference = 0
        parent_1_connections = parent_1_genome.connection_genes
        parent_2_connections = parent_2_genome.connection_genes
        for k, v in parent_1_connections.items():
            if k in parent_2_connections:
                matching_connections += 1
                weight_difference += abs(v.weight - parent_2_connections[k].weight)
        return float(weight_difference / matching_connections)

    def perturb_weights(self, weight_perturb_rate):
        """
        Changes or perturbs each of the weights according to the rate provided
        :param weight_perturb_rate: The rate at which weights will be perturbed or changed slightly
        """
        for k, v in self.connection_genes.items():
            v.weight = v.weight * (
                np.random.uniform() * 4.0 - 2.0) if np.random.uniform() < weight_perturb_rate else v.weight

    def reassign_weights(self, weight_reassign_rate):
        """
        Reassigns each of the weights according to the rate provided
        :param weight_reassign_rate: The rate at which weights will be reassigned
        """
        for k, v in self.connection_genes.items():
            v.weight = np.random.uniform() if np.random.uniform() < weight_reassign_rate else v.weight

    def __repr__(self):
        return self.print_genome()

    def enable_disable_gene(self, connection_enable_disable_rate):
        """
        Toggles some of the genes depending on the rate provided
        :param connection_enable_disable_rate: The rate at which gene will be toggled
        """
        for k, v in self.connection_genes.items():
            v.enabled = not v.enabled if np.random.uniform() < connection_enable_disable_rate else v.enabled

    @staticmethod
    def get_random_connection_genes(input_nodes, output_nodes, init=False):
        """
        Useful function for generating random connection genes
        :param input_nodes: Number of input nodes
        :param output_nodes: Number of output nodes
        :return: Random connection genes dictionary
        """
        connection_genes = dict()
        innovation_number = 1
        for i in range(1, input_nodes + 1):
            for j in range(1, output_nodes + 1):
                connection_genes[innovation_number] = ConnectionGene(
                    in_node=i,
                    out_node=input_nodes + j,
                    weight=np.random.random(),
                    enabled=np.random.random() < 0.5 if not init else True,
                    innovation_number=innovation_number
                )
                innovation_number += 1
        return connection_genes

    def generate_input_nodes(self, input_nodes):
        """
        Generate input_nodes number of node objects
        :param input_nodes: Number of input nodes
        :return: Dictionary of nodes
        """
        input_nodes_dict = dict()
        for i in range(1, input_nodes + 1):
            input_nodes_dict[i] = NodeGene(i, Type.INPUT)
        return input_nodes_dict

    def set_inputs(self, inputs):
        for key, input_node in self.input_nodes.items():
            input_node.output = inputs[key - 1]

    def generate_output_nodes(self, output_nodes):
        """
        Generate output_nodes number of node objects
        :param output_nodes: Number of output nodes
        :return: Dictionary of nodes
        """
        output_nodes_dict = dict()
        for i in range(1, output_nodes + 1):
            output_nodes_dict[len(self.input_nodes) + i] = NodeGene(len(self.input_nodes) + i, Type.OUTPUT)
        return output_nodes_dict

    def evaluate(self, inputs):
        from functools import reduce
        for i, node_id in enumerate(self.input_nodes):
            self.input_nodes[node_id].output = inputs[i]
        while self.output_nodes[3].output is None:
            for node_id, node in self.nodes.items():
                connections_to_this_node = [connection for iv, connection in self.connection_genes.items() if
                                            connection.out_node == node_id and connection.enabled]
                if len(connections_to_this_node) != 0:
                    self.nodes[node_id].output = self.sigmoid(reduce(
                        lambda sum1, next_tuple: sum1 + next_tuple[0] * next_tuple[1]
                        if next_tuple[1] is not None and sum1 is not None else None,
                        [(connection.weight, self.nodes[connection.in_node].output) for connection in
                         connections_to_this_node],
                        0.0))
        print(inputs, self.output_nodes[3].output)
        return self.output_nodes[3].output

    def sigmoid(self, x):
        return 1 / (1 + np.exp(-x))

    def __eq__(self, other):
        return [p1g for p1g in self.connection_genes].__eq__([p2g for p2g in other.connection_genes])


if __name__ == '__main__':
    ccg1 = ConnectionGene(1, 4, 1, True, 1)
    ccg2 = ConnectionGene(1, 5, 2, True, 2)
    ccg3 = ConnectionGene(1, 6, 3, True, 3)
    ccg4 = ConnectionGene(2, 4, 4, True, 4)
    ccg5 = ConnectionGene(2, 5, 5, True, 5)
    ccg6 = ConnectionGene(2, 6, 6, True, 6)
    ccg7 = ConnectionGene(4, 3, 7, True, 7)
    ccg8 = ConnectionGene(5, 3, 8, True, 8)
    ccg9 = ConnectionGene(6, 3, 9, True, 9)
    eg = dict()
    for i in range(1, 10):
        eg[locals()['ccg{}'.format(i)].innovation_number] = locals()['ccg{}'.format(i)]
    eg_genome = Genome(eg)
    eg_genome.set_inputs([1, 2])

    c1 = ConnectionGene(1, 4, 1, True, 1)
    c2 = ConnectionGene(1, 5, 3, True, 2)
    c3 = ConnectionGene(2, 4, 2, True, 3)
    c4 = ConnectionGene(2, 5, 4, True, 4)
    c5 = ConnectionGene(4, 6, 5, True, 5)
    c6 = ConnectionGene(4, 7, 7, True, 6)
    c7 = ConnectionGene(5, 6, 6, True, 7)
    c8 = ConnectionGene(5, 7, 8, True, 8)
    c9 = ConnectionGene(6, 3, 9, True, 9)
    c10 = ConnectionGene(7, 3, 10, True, 10)
    c11 = ConnectionGene(1, 7, 20, True, 11)
    c12 = ConnectionGene(1, 8, 1, True, 12)
    c13 = ConnectionGene(8, 4, 1, True, 13)

    c14 = ConnectionGene(4, 3, 0.7787, True, 14)
    aa = dict()
    for i in range(1, 15):
        aa[locals()['c{}'.format(i)].innovation_number] = locals()['c{}'.format(i)]
    a = Genome(aa)
    # a.add_connection_mutation()
    # a.set_inputs([1, 2])

    # a.add_node_mutation()
    # print(a.nodes)
    # print(a.connection_genes)
    # print(a.evaluate([1, 2]))
