import pygame
from pygame.locals import *

from Bird import Bird
from Pipe import Pipe

black = (0, 0, 0)
white = (255, 255, 255)

height = 600
width = 400

pygame = pygame

pygame.init()
size = width, height
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Flappy bird")
clock = pygame.time.Clock()


def game():
    x = 100
    y = int(width / 2)
    bird = Bird(x, y)
    birds = [bird]  # , Bird(100, 100), Bird(100, 130), Bird(100, 100), Bird(100, 150)]
    pipes = []
    done = False
    pygame.time.set_timer(USEREVENT + 1, 750)
    while not done:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
            if event.type == USEREVENT + 1:
                pipes.append(Pipe())
                for bird in birds:
                    bird.score += 1
            if event.type == pygame.MOUSEBUTTONDOWN:
                for bird in birds:
                    bird.up()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    for bird in birds:
                        bird.up()
                if event.key == pygame.K_ESCAPE:
                    done = True

        screen.fill(black)

        mindist = 999
        minpipe = Pipe()
        for pipe in pipes:
            pipe.update()
            pipe.show()
            if pipe.offscreen():
                pipes.remove(pipe)
            for bird in birds:
                if pipe.hit(bird):
                    print("Score of this bird was", bird.score)
                    # birds.remove(bird)
                    pass
            if 0 < pipe.distance < mindist:
                minpipe = pipe

        min_dist = [minpipe.x + int(minpipe.w / 2), minpipe.top + int(minpipe.gap / 2)]
        pygame.draw.circle(screen, white, min_dist, 10)
        for bird in birds:
            bird.closest_pipe_distance = min_dist
            bird.update()
            bird.show()

        if len(birds) == 0:
            pass
            # done = True

        pygame.display.flip()
        clock.tick(50)


game()
pygame.quit()
