from object_3d import *
from camera import *
from projection import *
import pygame as pg

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
        self.objects = [[0 for x in range(self.world_length)] for y in range(self.world_width)] 
        self.create_3d_objects()

    def create_3d_objects(self):
        self.camera = Camera(self, [0, 0, 0]) # random starting camera location
        self.projection = Projection(self)
        for i in range(self.world_length):
            for j in range(self.world_width):
                self.objects[i][j] = Object3D(self)
                self.objects[i][j].translate([i, 0, j])
                self.objects[i][j].scale(0.5)

    def draw(self):
        self.screen.fill(pg.Color('paleturquoise1'))
        for i in range(self.world_length):
            for j in range(self.world_width):
                self.objects[i][j].draw()
    
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
    