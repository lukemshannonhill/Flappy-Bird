import numpy as np

from Bird import Bird


class Genetic_Algorithm:
    def __init__(self, population_size):
        self.population_size = population_size
        self.population = list()
        self.elites = list()
        for i in range(population_size):
            self.population.append(Bird(100, np.random.randint(20, 500), show_bird=True))
        self.mutation_rate = 10

    def reset_population(self):
        self.population = list()
        for bird in self.elites:
            self.population.append(bird)
            print("Added from elites")
        if len(self.population) < self.population_size:
            for i in range(len(self.population), self.population_size):
                self.population.append(Bird(100, np.random.randint(20, 500), show_bird=True))

        for bird in self.population:
            print(bird.score)

    def get_best_unit(self):
        return sorted(self.population, key=lambda bird: bird.alive_time)[-1]

    def add_to_elites(self):
        if len(self.elites) == 0:
            if self.get_best_unit().score != 0:
                self.elites.append(self.get_best_unit())
                print("added to elites, now elites are", len(self.elites))

        else:
            if self.get_best_unit().alive_time > self.elites[- 1].alive_time:
                print("added to elites, now elites are", len(self.elites))
                self.elites.append(self.get_best_unit())

            if len(self.elites) > self.population_size:
                self.elites = self.elites[len(self.elites) - self.population_size:]

    def selection(self, best_count):
        sorted_population = sorted(self.population, key=lambda bird: bird.alive_time + bird.score)
        self.add_to_elites()
        return sorted_population[len(sorted_population):len(sorted_population) - best_count - 1:-1]

    def next_generation(self):
        best3 = self.selection(3)

        if self.get_best_unit().score == 0:
            print("Population reset")
            self.reset_population()

        new_population = list()
        first_3 = self.crossover(best3[0], best3[1])
        second_3 = self.crossover(best3[1], best3[2])
        for i in range(len(best3)):
            new_population.append(first_3[i])
            new_population.append(second_3[i])
        self.population = new_population

    def crossover(self, father_bird, mother_bird):
        hidden_weights_father, hidden_bias_father = father_bird.neural_network.get_hidden_weights_and_bias()
        output_weights_father, output_bias_father = father_bird.neural_network.get_output_weights_and_bias()

        hidden_weights_mother, hidden_bias_mother = mother_bird.neural_network.get_hidden_weights_and_bias()
        output_weights_mother, output_bias_mother = mother_bird.neural_network.get_output_weights_and_bias()

        child_1_hidden = np.random.random(hidden_weights_father.shape)
        for i in range(child_1_hidden.shape[0]):
            for j in range(int(child_1_hidden.shape[1] / 2)):
                child_1_hidden[i][j] = hidden_weights_father[i][j]
        for i in range(child_1_hidden.shape[0]):
            for j in range(int(child_1_hidden.shape[1] / 2), child_1_hidden.shape[1]):
                child_1_hidden[i][j] = hidden_weights_mother[i][j]
        child_1_output = np.random.random(output_weights_father.shape)
        for i in range(child_1_output.shape[0]):
            for j in range(int(child_1_output.shape[1] / 2)):
                child_1_output[i][j] = output_weights_father[i][j]
        for i in range(child_1_output.shape[0]):
            for j in range(int(child_1_output.shape[1] / 2), child_1_output.shape[1]):
                child_1_output[i][j] = output_weights_mother[i][j]

        child_2_hidden = np.random.random(hidden_weights_father.shape)
        for i in range(int(child_2_hidden.shape[0] / 2)):
            for j in range(child_2_hidden.shape[1]):
                child_2_hidden[i][j] = hidden_weights_father[i][j]
        for i in range(int(child_2_hidden.shape[0] / 2), child_2_hidden.shape[0]):
            for j in range(child_2_hidden.shape[1]):
                child_2_hidden[i][j] = hidden_weights_mother[i][j]
        child_2_output = np.random.random(output_weights_father.shape)
        for i in range(int(child_2_output.shape[0] / 2)):
            for j in range(child_2_output.shape[1]):
                child_2_output[i][j] = output_weights_father[i][j]
        for i in range(int(child_2_output.shape[0] / 2), child_2_output.shape[0]):
            for j in range(child_2_output.shape[1]):
                child_2_output[i][j] = output_weights_mother[i][j]

        child_3_hidden = np.random.random(hidden_weights_father.shape)
        for i in range(child_3_hidden.shape[0]):
            for j in range(child_3_hidden.shape[1]):
                child_3_hidden[i][j] = hidden_weights_father[i][j] if np.random.randint(0, 100) > 50 else \
                    hidden_weights_mother[i][j]
        child_3_output = np.random.random(output_weights_father.shape)
        for i in range(child_3_output.shape[0]):
            for j in range(child_3_output.shape[1]):
                child_3_output[i][j] = output_weights_father[i][j] if np.random.randint(0, 100) > 50 else \
                    output_weights_mother[i][j]

        child_1_hidden = self.mutate(child_1_hidden)
        child_2_hidden = self.mutate(child_2_hidden)
        child_3_hidden = self.mutate(child_3_hidden)
        child_1_output = self.mutate(child_1_output)
        child_2_output = self.mutate(child_2_output)
        child_3_output = self.mutate(child_3_output)

        child_1 = Bird(100, np.random.randint(20, 500), show_bird=True)
        child_2 = Bird(100, np.random.randint(20, 500), show_bird=True)
        child_3 = Bird(100, np.random.randint(20, 500), show_bird=True)

        child_1.neural_network.set_hidden_weights_and_bias(child_1_hidden,
                                                           father_bird.neural_network.get_hidden_weights_and_bias()[1])
        child_1.neural_network.set_output_weights_and_bias(child_1_output,
                                                           father_bird.neural_network.get_output_weights_and_bias()[1])

        child_2.neural_network.set_hidden_weights_and_bias(child_2_hidden,
                                                           father_bird.neural_network.get_hidden_weights_and_bias()[1])
        child_2.neural_network.set_output_weights_and_bias(child_2_output,
                                                           father_bird.neural_network.get_output_weights_and_bias()[1])

        child_3.neural_network.set_hidden_weights_and_bias(child_3_hidden,
                                                           father_bird.neural_network.get_hidden_weights_and_bias()[1])
        child_3.neural_network.set_output_weights_and_bias(child_3_output,
                                                           father_bird.neural_network.get_output_weights_and_bias()[1])
        # print(child_1)
        # print(child_2)
        # print(child_3)

        return child_1, child_2, child_3

    def mutate(self, child):
        for i in range(child.shape[0]):
            for j in range(child.shape[1]):
                child[i][j] = np.random.random() if np.random.randint(0, 100) < self.mutation_rate else child[i][j]
        return child

    def get_population(self):
        return self.population.copy()
