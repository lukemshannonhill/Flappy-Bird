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

fps = 60
pipe_interval = int(750 * 60 / fps)


def game():
    x = 100  # DON'T CHANGE THIS VALUE
    y = int(width / 2)
    bird = Bird(x, y)
    birds = [bird, Bird(100, 100), Bird(100, 130), Bird(100, 90), Bird(100, 150)]
    pipes = []
    done = False
    pygame.time.set_timer(USEREVENT + 1, pipe_interval)
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

        closest_pipe = [pipe for pipe in pipes if pipe.distance_from_bird_to_center_of_gap > 0]
        minx = 0
        if len(closest_pipe) > 0:
            minx = min(closest_pipe, key=lambda pipe_lambda: pipe_lambda.distance_from_bird_to_center_of_gap)

        for bird in birds:
            bird.horizontal_distance = minx.distance_from_bird_to_center_of_gap if minx else bird.x
            bird.update()
            bird.show()

        if len(birds) == 0:
            pass
            # done = True

        pygame.display.flip()
        clock.tick(fps)


game()
pygame.quit()
