class Bird:
    def __init__(self, x, y, id=1):
        self.x = x
        self.y = y
        self.id = id
        self.gravity = 0.8
        self.velocity = 0
        self.lift = -25
        self.score = 0

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

    def show(self):
        from FlappyBird import pygame, screen, white
        pygame.draw.circle(screen, white, self.position(), 15)

    def up(self):
        self.velocity += self.lift

        # def hit(self, pipe):
        #     from FlappyBird import height
        #     if self.y < pipe.top or self.y > height - pipe.bottom:
        #         if pipe.x < self.x < pipe.x + pipe.w:
        #             pipe.has_hit = True
        #             return True
        #     pipe.has_hit = False
        #     return False
