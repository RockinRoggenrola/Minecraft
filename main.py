import pygame
import math
import numpy
from setup import *
from Cube import Cube
from Camera import Camera

pygame.init()

cube = Cube(2, 1, 4, (255, 0, 0))
player = Camera((1, 0, 1.7), numpy.array((1, 1, 1)), 0.1, 50, 45)

while True:
    clock.tick(fps)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            break

    keys = pygame.key.get_pressed()
    if keys[pygame.K_RIGHT]:
        player.move_right()
    if keys[pygame.K_LEFT]:
        player.move_left()
    if keys[pygame.K_UP]:
        player.move_up()
    if keys[pygame.K_DOWN]:
        player.move_down()


    screen.fill((0, 0, 0))
    player.render_cube(cube)
    pygame.display.update()