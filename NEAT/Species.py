import random
from functools import reduce

import numpy as np


class Species:
    def __init__(self, genomes):
        """
        Constructor for species which has a list of genomes
        :param genomes: List of genomes in this species
        """
        self.genomes = genomes
        self.top_fitness = self.get_max_fitness()
        self.average_fitness = self.calculate_average_fitness()
        self.staleness = 0.0

    def get_max_fitness(self):
        """
        Retrieves the fitness of the strongest genome
        :return: Fitness of the strongest genome
        """
        return max(self.genomes, key=lambda genome: genome.fitness).fitness

    def calculate_average_fitness(self):
        """
        Retrieves the average fitness of all the genomes
        :return: Average fitness of all the genomes
        """
        return float(
            reduce(lambda genome_1, genome_2: genome_1.fitness + genome_2.fitness, self.genomes) / len(self.genomes)
        )

    def make_child(self):
        """
        Creates an offspring of two random genomes from the list of genomes
        :return: Child genome
        """
        parent_1 = self.genomes[random.choice(list(self.genomes.keys()))]
        parent_2 = self.genomes[random.choice(list(self.genomes.keys()))]
        child = Species.crossover(parent_1, parent_2)
        return child

    @staticmethod
    def crossover(parent_1_genome, parent_2_genome):
        from NEAT.Genome import Genome
        """
        Abstract for crossover between two genomes.
        Actual crossover at get_child_connections(parent_1_genome, parent_2_genome)

        Mutation rates: Refer paper section 4.1
            Node Mutation = 0.03
            Connection Mutation = 0.05
            Weight Mutation = 0.8
                Weight Perturb Rate = 0.9
                Weight Reassign Rate = 0.1
            Connection Enable/Disable Rate = 0.75
            Inter-species Crossover = 0.001 
        :param parent_1_genome: The genome for 1st parent
        :param parent_2_genome: The genome for 2nd parent
        :return: Child genome with mutation applied
        """

        inter_species_crossover_rate = 0.001
        node_mutation_rate = 0.03
        connection_mutation_rate = 0.05
        connection_enable_disable_rate = 0.75
        weight_mutation = 0.8
        weight_perturb_rate = 0.9
        weight_reassign_rate = 0.1

        if Species.is_same_species(parent_1_genome, parent_2_genome):
            perform_crossover = True
        else:
            perform_crossover = True if np.random.uniform() < inter_species_crossover_rate else False

        if perform_crossover:
            child_connections = Species.get_child_connections(parent_1_genome, parent_2_genome)
            child_genome = Genome(child_connections)
            if np.random.uniform() < node_mutation_rate:
                child_genome.add_node_mutation()
            if np.random.uniform() < connection_mutation_rate:
                child_genome.add_connection_mutation()
            if np.random.uniform() < weight_mutation:
                child_genome.perturb_weights(weight_perturb_rate)
                child_genome.reassign_weights(weight_reassign_rate)
            if np.random.uniform() < connection_enable_disable_rate:
                child_genome.enable_disable_gene(connection_enable_disable_rate)
            return child_genome
        else:
            return max([parent_1_genome, parent_2_genome], key=lambda genome: genome.fitness)

    @staticmethod
    def is_same_species(parent_1_genome, species):
        from NEAT.Genome import Genome
        """
        Returns True if the genomes is in same species else False
        Threshold value = 3.0   Refer paper section 4.1
    
        :param parent_1_genome: The genome of anyone to be added in this species
        :param species: Species object
        :return: Boolean representing whether genome belong in the provided species
        """
        threshold = 3.0
        return True if Genome.get_compatibility_distance(parent_1_genome, species.genomes[0]) < threshold else False

    @staticmethod
    def get_child_connections(parent_1_genome, parent_2_genome):
        """
        Performs actual crossover between the two genomes
        :param parent_1_genome: The genome for 1st parent
        :param parent_2_genome: The genome for 2nd parent
        :return: Child genome connections dictionary
        """
        child_connections = dict()

        if parent_1_genome.fitness > parent_2_genome.fitness:
            parent_1_genome, parent_2_genome = parent_1_genome, parent_2_genome
        elif parent_1_genome.fitness < parent_2_genome.fitness:
            parent_1_genome, parent_2_genome = parent_2_genome, parent_1_genome
        else:
            parent_1_genome, parent_2_genome = parent_1_genome, parent_2_genome

        parent_1_connections = parent_1_genome.connection_genes
        parent_2_connections = parent_2_genome.connection_genes

        if parent_1_genome.fitness != parent_2_genome.fitness:
            for k, v in parent_1_connections.items():
                if parent_2_connections.get(k) is None:
                    child_connections[k] = parent_1_connections[k]
                else:
                    child_connections[k] = v if np.random.uniform() < 0.5 else parent_2_connections[k]
        else:
            for k, v in parent_1_connections.items():
                if parent_2_connections.get(k) is None:
                    child_connections[k] = parent_1_connections[k]
            for k, v in parent_2_connections.items():
                if parent_1_connections.get(k) is None:
                    child_connections[k] = parent_2_connections[k]
            for k, v in parent_1_connections.items():
                if parent_1_connections.get(k) is not None and parent_2_connections.get(k) is not None:
                    child_connections[k] = v if np.random.uniform() < 0.5 else parent_2_connections[k]
        return child_connections
