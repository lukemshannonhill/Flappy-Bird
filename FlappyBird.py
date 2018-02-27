import numpy as np
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

pygame.init()
pygame = pygame
size = width, height
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Flappy bird")
clock = pygame.time.Clock()

fps = 60
pipe_interval = int(750 * 60 / fps)


def game():
    birds = []
    for i in range(5):
        birds.append(Bird(100, np.random.randint(20, 500)))
    pipes = []
    done = False
    pygame.time.set_timer(USEREVENT + 1, pipe_interval)
    while not done:
        screen.fill(black)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
                pygame.quit()
                exit()
            if event.type == USEREVENT + 1:
                pipes.append(Pipe())
            if event.type == pygame.MOUSEBUTTONDOWN:
                # TODO: Thread this
                for bird in birds:
                    bird.up()
                    # until this
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    # TODO: Thread this
                    for bird in birds:
                        bird.up()
                        # until this
                if event.key == pygame.K_ESCAPE:
                    done = True
                    pygame.quit()
                    exit()

        # TODO: Thread this
        for pipe in pipes:
            pipe.update()
            # pipe.show()   draw functions should be in main loop
            pipes = [pipe for pipe in pipes if not pipe.offscreen()]
            for bird in birds:
                if pipe.hit(bird):
                    print("Score of this bird was", bird.score)
                    birds.remove(bird)
                    pass
        # until this

        # Drawing pipes
        for pipe in pipes:
            pipe.show()

        pipes_to_right_of_bird = [pipe for pipe in pipes if pipe.distance_from_bird_to_end_of_gap > 0]
        closest_pipe_to_right_of_bird = 0
        if len(pipes_to_right_of_bird) > 0:
            closest_pipe_to_right_of_bird = min(pipes_to_right_of_bird,
                                                key=lambda pipe_lambda: pipe_lambda.distance_from_bird_to_end_of_gap)

        # draw target point
        target_point = [100 + closest_pipe_to_right_of_bird.distance_from_bird_to_end_of_gap if isinstance(
            closest_pipe_to_right_of_bird, Pipe) else width,
                        closest_pipe_to_right_of_bird.top + int(
                            closest_pipe_to_right_of_bird.gap / 2) if closest_pipe_to_right_of_bird else int(
                            height / 2)]

        pygame.draw.circle(screen, blue, target_point, 5)
        pygame.draw.line(screen, blue, [0, target_point[1]], [width, target_point[1]])

        # TODO: Thread this
        for bird in birds:
            bird.update()
            bird.horizontal_distance = target_point[0] - bird.x
            bird.height_difference = target_point[1] - bird.y
            bird.target_point = target_point
            # Simulate neural network if True
            if False:
                if bird.neuralnetwork_make_decision(bird.horizontal_distance, bird.height_difference):
                    bird.up()
                else:
                    pass

            # bird.show()   draw the birds on main loop
        # until this

        # Draw birds
        for bird in birds:
            bird.show()

        if not len(birds):
            pass
            done = True

        pygame.display.flip()
        clock.tick(fps)


# while 1:
#     game()
game()
pygame.quit()
exit()
