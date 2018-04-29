import numpy as np

from neural_network import NeuralNetwork


class Bird:
    def __init__(self, x, y, genome=None, show_bird=False):
        from FlappyBird import width, height
        self.x = x
        self.show_bird = show_bird
        self.y = y
        self.radius = 15

        self.gravity = 0.8
        self.velocity = 0
        self.lift = -25

        self.score = 0  # Fitness function

        self.horizontal_distance = 0  # Neural Network input 1
        self.height_difference = 0  # Neural Network input 2
        self.target_point = [width, height]

        self.alive_time = 0

        # ----Simulates neural network output
        self.f = 0
        self.random_no = np.random.randint(30, 50)
        # ----Done

        self.neural_network = NeuralNetwork(input_nodes=3, hidden_nodes=6, output_nodes=1)


    def position(self):
        return [self.x, self.y]

    def update(self):
        self.velocity += self.gravity
        self.velocity *= .9
        self.y += int(self.velocity)
        self.f += 1
        self.alive_time += 1

        # self.nn.fitness = self.f + self.alive_time

        from FlappyBird import height
        if self.y + self.radius > height:
            self.y = height - self.radius
            self.velocity = 0
        if self.y - self.radius < 0:
            self.y = self.radius
            self.velocity = 0
        if self.target_point[0] - self.x - 5 == 0:
            self.score += 1

    def show(self):
        if self.show_bird:
            from FlappyBird import pygame, white, screen, red_blue, bird_image
            screen.blit(bird_image, [self.position()[0]-15, self.position()[1]-15])
            # pygame.draw.circle(screen, red_blue, self.position(), self.radius)
            # pygame.draw.line(screen, white, (self.x, self.y + self.height_difference), (self.x, self.y))
            # pygame.draw.line(screen, white,
            #                  (self.x, self.y),
            #                  (self.horizontal_distance + self.x, self.y))
            # screen.blit(
            #     pygame.font.Font('C://windows//fonts//arial.ttf', 20).render(
            #         "{}".format(self.height_difference), True, white),
            #     (self.x + 15, self.y - 100 if self.y - 100 > 0 else 0))
            # screen.blit(
            #     pygame.font.Font('C://windows//fonts//arial.ttf', 20).render(
            #         "{}".format(self.horizontal_distance), True, white),
            #     (self.x + 50, self.y - 30 if self.y - 30 > 0 else 0))

    def up(self):
        self.velocity += self.lift

    def hit_walls(self):
        from FlappyBird import height
        if self.y - self.radius == 0 or self.y + self.radius == height:
            return True
        return False

    def neural_network_make_decision(self, horizontal_distance, height_difference,velocity, simulated=True):
        if simulated:
            if self.f % self.random_no == 0:
                return True
            else:
                return False
        else:
            # print(horizontal_distance, height_difference,
            #       self.neural_network.predict([horizontal_distance, height_difference])[1])

        return self.neural_network.predict([horizontal_distance, height_difference, velocity])[1] > 0.5