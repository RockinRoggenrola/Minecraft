import pygame as pg
import moderngl as mgl
import sys # system modules
from blocks import *

class Minecraft:
    def __init__(self):
        # initialize pygame modules
        pg.init()
        self.WIND_SIZE = (800, 450)

        # intialize OpenGL screen (context) for rendering
        # pg.OPENGL: makes a display that can render OpenGL
        # double buffering: two "buffers" (block of memory), one is used for drawing, and the 
        # other for displaying. After drawing is done, the drawing buffer is copied to video 
        # memory (the other buffer) and the buffers are swapped. Uses more memory than single buffering but is cleaner at graphics
        pg.display.set_mode(self.WIND_SIZE, flags = pg.OPENGL | pg.DOUBLEBUF)

        # detect the context we made and use it
        self.context = mgl.create_context()
        self.context.enable(mgl.DEPTH_TEST | mgl.CULL_FACE | mgl.BLEND)

        self.clock = pg.time.Clock()
        self.time = 0
        self.world = Block(self)

    def render(self):
        # clear framebuffer (a collection of buffers used as the rendering destination)
        self.context.clear(color=(225/255, 232/255, 227/255)) # colors are in rgb/255 form
        self.world.render()
        # swap buffers (update screen)
        pg.display.flip()
    
    def run(self):
        while True:
            for event in pg.event.get():
                if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                    self.world.clear()
                    pg.quit()
                    sys.exit()
                # if event.type == pg.MOUSEBUTTONDOWN:
                #     x, y = pg.mouse.get_pos()
                #     print(x, y)
            self.render()
            self.clock.tick(60)
            self.time = pg.time.get_ticks() * 0.001

if __name__ == '__main__':
    minecraft = Minecraft()
    minecraft.run()







