import pygame
from pygame.locals import *

from Bird import Bird
from Pipe import Pipe

black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)
green = (0, 255, 0)
blue = (0, 0, 255)
red_blue = (255, 0, 255)

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
    y = int(width / 2)
    bird = Bird(100, y)
    birds = [bird, Bird(100, 100), Bird(100, 130), Bird(100, 90), Bird(100, 150)]
    # birds = [bird]
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
            pipes = [pipe for pipe in pipes if not pipe.offscreen()]
            for bird in birds:
                if pipe.hit(bird):
                    print("Score of this bird was", bird.score)
                    birds.remove(bird)
                    pass

        pipes_to_right_of_bird = [pipe for pipe in pipes if pipe.distance_from_bird_to_end_of_gap > 0]
        closest_pipe_to_right_of_bird = 0
        if len(pipes_to_right_of_bird) > 0:
            closest_pipe_to_right_of_bird = min(pipes_to_right_of_bird,
                                                key=lambda pipe_lambda: pipe_lambda.distance_from_bird_to_end_of_gap)

        for bird in birds:
            bird.horizontal_distance = closest_pipe_to_right_of_bird.distance_from_bird_to_end_of_gap if isinstance(
                closest_pipe_to_right_of_bird, Pipe) else width
            bird.height_difference = (
                closest_pipe_to_right_of_bird.top + int(closest_pipe_to_right_of_bird.gap / 2) - bird.y) if isinstance(
                closest_pipe_to_right_of_bird, Pipe) else int(height / 2)
            bird.update()

            if bird.neuralnetwork_make_decision(bird.horizontal_distance, bird.height_difference):
                bird.up()
            else:
                pass

            bird.show()

        # draw target point
        pygame.draw.circle(screen, (0, 0, 255),
                           [100 + closest_pipe_to_right_of_bird.distance_from_bird_to_end_of_gap if isinstance(
                               closest_pipe_to_right_of_bird, Pipe) else width,
                            closest_pipe_to_right_of_bird.top + int(
                                closest_pipe_to_right_of_bird.gap / 2) if closest_pipe_to_right_of_bird else int(
                                height / 2)], 5)

        if len(birds) == 0:
            pass
            done = True

        pygame.display.flip()
        clock.tick(fps)


# while (1):
game()
pygame.quit()
