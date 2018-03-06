import random
from builtins import range


class Population:
    def __init__(self, population_size=10):
        """
        Constructor for the population object which has a list of species
        :param population_size: Number of total genomes inclusive of all species
        """
        self.population_size = population_size
        self.generation = 0
        self.max_fitness = 0
        self.species = []  # List of species

        self.stale_species = int(self.population_size * 10 / 3)

    def initialize_population(self):
        """
        Initializes population by creating random genomes and adding them to appropriate species
        """
        from NEAT.Genome import Genome
        for i in range(self.population_size):
            random_genome_connections = Genome.get_random_connection_genes(input_nodes=2, output_nodes=1)
            genome = Genome(random_genome_connections, input_nodes=2, output_nodes=1)
            self.add_to_species(genome)

    def add_to_species(self, genome):
        """
        Adds a genome to the appropriate species
        :param genome: The genome to be added in a species
        """
        from NEAT.Species import Species
        for species in self.species:  # Check for every species
            if Species.is_same_species(genome, species):
                species.genomes.append(genome)  # Append to already existing species
                return
        self.species.append(Species(genome))  # Make a new species and append it to list

    def calculate_total_average_fitness(self):
        """
        Calculates the total average fitness of the whole population
        """
        from functools import reduce
        return float(
            reduce(
                lambda species1, species2: species1.calculate_average_fitness() + species2.calculate_average_fitness(),
                self.species) / len(self.species)
        )

    def create_new_generation(self):
        """
        Creates a new generation of population by using crossover and removing stale and weak species
        """
        import math
        # Remove bottom half of the genomes in each species based on fitness
        self.remove_bottom_half_genomes_in_species()

        # Remove stale species
        # TODO: Don't know how this works. Copied from https://github.com/NeatMonster/NEATFlappyBird
        self.remove_stale_species()

        for species in self.species:
            species.calculate_average_fitness()

        # Remove weak species
        # TODO: Don't know how this works. Copied from https://github.com/NeatMonster/NEATFlappyBird
        self.remove_weak_species()

        # Calculate the total average fitness of this generatipm
        sum = self.total_average_fitness()

        children = list()
        for species in self.species:
            # Don't know why
            # TODO: Don't know how this works. Copied from https://github.com/NeatMonster/NEATFlappyBird
            breed = math.floor(species.average_fitness / sum * self.population_size) - 1.0
            for i in range(0, int(breed)):
                children.append(species.make_child())
        # Remove every genomes in every species except the strongest of each
        self.remove_all_genomes_in_species_except_strongest()

        # Create children
        while len(children) + len(self.species) < self.population_size:
            random_species = self.species[random.choice(list(self.species))]
            children.append(random_species.make_child())

        for child in children:
            self.add_to_species(child)
        self.generation += 1

    def remove_stale_species(self):
        """
        Removes the stale species, which have not created any considerable offsprings in the stale species
        threshold generation
        """
        survived = list()
        for species in self.species:
            species.genomes = list(reversed(sorted(species.genomes, key=lambda genome: genome.fitness)))

            if species.genomes[0].fitness > species.top_fitness:
                species.topFitness = species.genomes[0].fitness
                species.staleness = 0
            else:
                species.staleness += 1
            if species.staleness < self.stale_species or species.top_fitness >= self.max_fitness:
                survived.append(species)

            self.species.clear()
            self.species = survived

    def remove_weak_species(self):
        """
        Removes the weak species which have an average fitness less than the threshold below
        TODO: DON'T KNOW HOW THIS WORKS !
        """
        import math
        survived = list()
        sum = self.total_average_fitness()
        for species in self.species:
            breed = math.floor(species.average_fitness / sum * self.population_size)
            if breed >= 1.0:
                survived.append(species)
        self.species.clear()
        self.species = survived

    def total_average_fitness(self):
        """
        Calculates the average fitness of all species
        """
        from functools import reduce
        return reduce(lambda species_1, species_2: species_1.average_fitness + species_2.average_fitness, self.species)

    def remove_bottom_half_genomes_in_species(self):
        """
        Removes the bottom half genomes in each species depending of the genome fitness
        """
        for species in self.species:
            species.genomes = list(reversed(sorted(species.genomes, key=lambda genome: genome.fitness)))
            half_point = int(len(species.genomes) / 2)
            while len(species.genomes) > half_point:
                species.genomes.remove(species.genomes[len(species.genomes) - 1])

    def remove_all_genomes_in_species_except_strongest(self):
        """
        Removes all genomes in each species except the strongest ones
        """
        for species in self.species:
            species.genomes = list(reversed(sorted(species.genomes, key=lambda genome: genome.fitness)))
            while len(species.genomes) > 1:
                species.genomes.remove(species.genomes[len(species.genomes) - 1])
