from numpy import random


class Pipe:
    def __init__(self):
        from FlappyBird import height, width
        self.gap = 150
        self.top = random.randint(10, int(height / 2))
        self.bottom = height - self.top - self.gap
        self.x = width
        self.w = 20
        self.speed = 5
        self.has_hit = False
        self.distance = -100 + self.x

    def show(self):
        from FlappyBird import pygame, screen, white, height

        pygame.draw.rect(screen, white if not self.has_hit else (255, 0, 0), [self.x, 0, self.w, self.top])
        pygame.draw.rect(screen, white if not self.has_hit else (255, 0, 0),
                         [self.x, height - self.bottom, self.w, self.bottom])
        screen.blit(
            pygame.font.Font('C://windows//fonts//arial.ttf', 25).render("{}".format(self.distance), True, (0, 255, 0)),
            (self.x, int(self.top + self.gap / 2)))

    def update(self):
        self.distance = -100 + self.x
        self.x -= self.speed

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
