import numpy as np
from Bird import Bird

class Genetic_Algorithm:
    def __init__(self, population_size):
        self.population_size = population_size
        self.population = list()
        self.elites = list()
        for i in range(population_size):
            self.population.append(Bird(100, np.random.randint(20, 500), show_bird=True))
        self.mutation_rate = 20


    def reset_population(self):
        self.population = list()
        for bird in self.elites:
            self.population.append(bird[1])
            print("Added from elites")
        if len(self.population) < self.population_size:
            for i in range(len(self.population), self.population_size):
                self.population.append(Bird(100, np.random.randint(20, 500), show_bird=True))

        for bird in self.population:
            print(bird.score)


    def get_best_unit(self):
        return sorted(self.population, key=lambda bird: bird.alive_time)[-1]


    def add_to_elites(self):
        best_bird = self.get_best_unit()
        if len(self.elites) < 6:
            if best_bird.alive_time != 0:
                self.elites.append([best_bird.alive_time, best_bird])
                print("added to elites, now elites are", len(self.elites))
        else:
            if best_bird.alive_time > self.elites[0][1].alive_time:
                print("added to elites, now elites are", len(self.elites))
                print("replacing a weak elite")
                self.elites.pop(0)
                self.elites.append([best_bird.alive_time, best_bird])

        self.elites.sort(key=lambda i: i[0])
        print(str(self.elites))


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
        child_population = list()
        child_population.append(self.crossover(best3[0], best3[1]))
        child_population.append(self.crossover(best3[1], best3[2]))
        if len(self.elites) > 1:
            for i in range(len(self.elites)-1,0,-1):
                child_population.append(self.crossover(self.elites[i][1], self.elites[i-1][1]))

        for child in child_population:
            for i in range(len(child)):
                new_population.append(child[i])
        self.population = new_population

        for elite in self.elites:
            if len(self.population) < self.population_size:
                elite[1].score = 0
                elite[1].alive_time = 0
                self.population.append(elite[1])

        if len(self.population) < self.population_size:
            for i in range(len(self.population), self.population_size):
                self.population.append(Bird(100, np.random.randint(20, 500), show_bird=True))


    def crossover(self, father_bird, mother_bird):
        hidden_weights_father, hidden_bias_father = father_bird.neural_network.get_hidden_weights_and_bias()
        output_weights_father, output_bias_father = father_bird.neural_network.get_output_weights_and_bias()

        hidden_weights_mother, hidden_bias_mother = mother_bird.neural_network.get_hidden_weights_and_bias()
        output_weights_mother, output_bias_mother = mother_bird.neural_network.get_output_weights_and_bias()

        child_1_hidden = hidden_weights_father
        child_2_hidden = hidden_weights_mother
        child_1_output = output_weights_mother
        child_2_output = output_weights_father

        hidden_bias_child1 = hidden_bias_father
        hidden_bias_child2 = hidden_bias_mother
        output_bias_child2 = output_bias_father
        output_bias_child1 = output_bias_mother

        child_1_hidden = self.mutate(child_1_hidden)
        child_2_hidden = self.mutate(child_2_hidden)
        child_1_output = self.mutate(child_1_output)
        child_2_output = self.mutate(child_2_output)

        child_1 = Bird(100, np.random.randint(20, 500), show_bird=True)
        child_2 = Bird(100, np.random.randint(20, 500), show_bird=True)

        child_1.neural_network.set_hidden_weights_and_bias(child_1_hidden,
                                                           hidden_bias_child1)
        child_1.neural_network.set_output_weights_and_bias(child_1_output,
                                                           output_bias_child1)

        child_2.neural_network.set_hidden_weights_and_bias(child_2_hidden,
                                                           hidden_bias_child2)
        child_2.neural_network.set_output_weights_and_bias(child_2_output,
                                                           output_bias_child2)

        return child_1, child_2


    def mutate(self, child):
        for i in range(child.shape[0]):
            for j in range(child.shape[1]):
                child[i][j] = np.random.random() if np.random.randint(0, 100) < self.mutation_rate else child[i][j]
        return child

    def get_population(self):
        return self.population.copy()
