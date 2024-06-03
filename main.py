from object_3d import *
from camera import *
from projection import *
import pygame as pg
import random

class CubeRender:
    def __init__(self):
        pg.init()
        self.RES = self.WIDTH, self.HEIGHT = 800, 600
        self.H_WIDTH, self.H_HEIGHT = self.WIDTH // 2, self.HEIGHT // 2
        self.FPS = 120
        self.screen = pg.display.set_mode(self.RES)
        self.clock= pg.time.Clock()
        self.world_length = 10 
        self.world_width = 10
        self.world_height = 10
        self.objects = [[[0 for x in range(self.world_length)] for y in range(self.world_width)] for z in range(self.world_height)]
        self.totally_random_heights = [1, 1, 1, 1, 1, 1, 1, 1, 2, 2, 2, 2, 3]
        self.create_3d_objects()

    def create_3d_objects(self):
        self.camera = Camera(self, [0, 0, 0]) # random starting camera location
        self.projection = Projection(self)
        for i in range(self.world_length):
            for j in range(self.world_width):
                self.rand_height = random.choice(self.totally_random_heights)
                for k in range(self.rand_height):
                    self.objects[i][j][k] = Object3D(self)
                    self.objects[i][j][k].translate([i, k-1, j])
                    self.objects[i][j][k].scale(0.1)

    def draw(self):
        self.screen.fill(pg.Color('paleturquoise1'))
        for i in range(self.world_length):
            for j in range(self.world_width):
                for k in range(self.world_height):
                    if self.objects[i][j][k] != 0:
                        self.objects[i][j][k].draw()
    
    def run(self):
        while True:
            self.draw()
            self.camera.control()
            [exit() for i in pg.event.get() if i.type == pg.QUIT]
            pg.display.set_caption(str(self.clock.get_fps()))
            pg.display.flip()
            self.clock.tick(self.FPS)

if __name__ == '__main__':
    game = CubeRender()
    game.run()
    