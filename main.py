import pygame
import math
import numpy
from setup import *
from Cube import Cube
from Camera import Camera

pygame.init()
screen = pygame.display.set_mode((width, height))
clock = pygame.time.Clock()

cube = Cube(2, 1, 4, (255, 0, 0))
player = Camera((0, 0, 1.7), numpy.array((1, 1, 1)), 0.1, 50, 45)

while True:
    clock.tick(fps)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            break

    RED = (255, 0, 0)
    for vertex in cube.vertices():
        projection_matrix = player.make_projection_matrix()
        twoD_coords = player.project_to_2d(vertex, projection_matrix)
        pygame_coords = player.convert_to_pygame(twoD_coords)
        pygame.draw.circle(screen, RED, pygame_coords, 3)


    pygame.display.update()