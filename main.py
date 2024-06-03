import math
import pygame

pygame.init()
WIDTH = 1000
HEIGHT = 500
BLOCK_SIZE = 20
player_x = 0
player_y = 1.7
player_z = 0

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
sky = pygame.image.load('sky.jpg')
sky = pygame.transform.scale(sky, (WIDTH, HEIGHT))
grayblock = pygame.image.load('grayblock.jpg')
grayblock = pygame.transform.scale(grayblock, (BLOCK_SIZE, BLOCK_SIZE))

blocks = [[0 for i in range(100)] for i in range(100)]

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.MOUSEBUTTONUP:
            pos = pygame.mouse.get_pos()
            x = math.ceil(pos[0]/BLOCK_SIZE)-1
            y = math.ceil((HEIGHT-pos[1])/BLOCK_SIZE)-1
            blocks[x][y] = 1
    
    rectangles = []
    for i in range(len(blocks)):
        for j in range(len(blocks[i])):
            if blocks[i][j] == 1:
                block = blocks[i][j]
                blocksurf = grayblock.get_rect(topleft = (BLOCK_SIZE*(i), BLOCK_SIZE*(HEIGHT//BLOCK_SIZE-j-1)))
                screen.blit(grayblock, blocksurf)
                rectangles.append(blocksurf)

    pygame.display.update()
    clock.tick(60)
    screen.blit(sky, (0, 0))

from object_3d import *
from camera import *
from projection import *
import pygame as pg
import random