import numpy as np


class Bird:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.radius = 15
        self.id = id
        self.gravity = 0.8
        self.velocity = 0
        self.lift = -25
        self.score = 0
        self.horizontal_distance = 0  # Neural Network input 1
        self.height_difference = 0  # Neural Network input 2
        self.f = 0
        self.random_no = np.random.randint(30, 50)

    def position(self):
        return [self.x, self.y]

    def update(self):
        self.velocity += self.gravity
        self.velocity *= .9
        self.y += int(self.velocity)
        self.f += 1
        from FlappyBird import height
        if self.y + self.radius > height:
            self.y = height - self.radius
            self.velocity = 0
        if self.y - self.radius < 0:
            self.y = self.radius
            self.velocity = 0

            # self.up() if neuralnetwork.makeDecision(self.horizontal_distance,self.height_difference) else pass

    def show(self):
        from FlappyBird import pygame, white, screen, red_blue
        pygame.draw.circle(screen, red_blue, self.position(), self.radius)
        pygame.draw.line(screen, white, (self.x, self.y + self.height_difference), (self.x, self.y))
        pygame.draw.line(screen, white,
                         (self.x, self.y),
                         (self.horizontal_distance + self.x, self.y))
        screen.blit(
            pygame.font.Font('C://windows//fonts//arial.ttf', 20).render(
                "{}".format(self.height_difference), True, white),
            (self.x + 15, self.y - 100 if self.y - 100 > 0 else 0))
        screen.blit(
            pygame.font.Font('C://windows//fonts//arial.ttf', 20).render(
                "{}".format(self.horizontal_distance), True, white),
            (self.x + 50, self.y - 30 if self.y - 30 > 0 else 0))

    def up(self):
        self.velocity += self.lift

    def perform_action(self):
        pass

    def neuralnetwork_make_decision(self, horizontal_distance, height_difference):
        if self.f % self.random_no == 0:
            return True
        else:
            return False
