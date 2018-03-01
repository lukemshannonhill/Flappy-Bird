from numpy import random


class Pipe:
    def __init__(self, pipe_level):
        from FlappyBird import height, width
        self.gap = 150
        self.top = random.randint(10, int(height / 2))
        self.bottom = height - self.top - self.gap
        self.x = width
        self.w = 50
        self.pipe_level = pipe_level
        self.speed = 5
        self.has_hit = False
        self.distance_from_bird_to_end_of_gap = (self.x + int(self.w / 1)) - 100

    def show(self):
        from FlappyBird import pygame, screen, height, green, red,white

        pygame.draw.rect(screen, green if not self.has_hit else red, [self.x, 0, self.w, self.top])
        pygame.draw.rect(screen, green if not self.has_hit else red,
                         [self.x, height - self.bottom, self.w, self.bottom])
        screen.blit(
            pygame.font.Font('C://windows//fonts//arial.ttf', 25).render(
                "{}".format(self.distance_from_bird_to_end_of_gap), True, green),
            (self.x, int(self.top + self.gap / 2)))

        screen.blit(
            pygame.font.Font('C://windows//fonts//arial.ttf', 30).render(
                "{}".format(self.pipe_level), True, red),
            (self.x, int(self.top - self.gap / 2)))

    def update(self):
        self.x -= self.speed
        self.distance_from_bird_to_end_of_gap = (self.x + int(self.w / 1)) - 100

    def offscreen(self):
        return self.x < -self.w

    def hit(self, bird):
        from FlappyBird import height
        if bird.y < self.top or bird.y > height - self.bottom:
            if self.x < bird.x < self.x + self.w:
                self.has_hit = True
                return True
        self.has_hit = False
        return False
