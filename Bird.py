class Bird:
    def __init__(self, x, y, id=1):
        self.x = x
        self.y = y
        self.id = id
        self.gravity = 0.8
        self.velocity = 0
        self.lift = -25
        self.score = 0
        self.horizontal_distance = 0
        self.vertical_distance = 0

    def position(self):
        return [self.x, self.y]

    def update(self):
        self.velocity += self.gravity
        self.velocity *= .9
        self.y += int(self.velocity)

        from FlappyBird import height
        if self.y > height:
            self.y = height
            self.velocity = 0
        if self.y < 0:
            self.y = 0
            self.velocity = 0

        self.vertical_distance = self.y

    def show(self):
        from FlappyBird import pygame, screen, white
        pygame.draw.circle(screen, white, self.position(), 15)
        pygame.draw.line(screen, (0, 255, 0), (self.x, 0), (self.x, self.y))
        pygame.draw.line(screen, (0, 255, 0),
                         (self.x, self.y),
                         (self.horizontal_distance + 100, self.y))
        screen.blit(
            pygame.font.Font('C://windows//fonts//arial.ttf', 20).render(
                "{},{}".format(self.vertical_distance, self.horizontal_distance), True, (0, 255, 0)),
            (self.x + 50, self.y - 30))

    def up(self):
        self.velocity += self.lift

    def distance(self, p1, p2):
        import math
        return math.pow((math.pow(p1[0] - p2[0], 2) + math.pow(p1[1] - p2[1], 2)), 0.5)
