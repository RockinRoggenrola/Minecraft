import pygame as pg
from matrices import *


class Object3D:
    def __init__(self, render):
        self.render = render
        self.vertices = np.array([(0, 0, 0, 1), (0, 1, 0, 1), (1, 1, 0, 1), (1, 0, 0, 1),
                                  (0, 0, 1, 1), (0, 1, 1, 1), (1, 1, 1, 1), (1, 0, 1, 1)]) # (x, y, z, w) index = vertex #
        self.faces = np.array([(0, 1, 2, 3), (4, 5, 6, 7), (0, 4, 5, 1), (2, 3, 7, 6), (1, 2, 6, 5), (0, 3, 7, 4)])

    def draw(self):
        self.screen_projection()
    def screen_projection(self):
        vertices = self.vertices @ self.render.camera.camera_matrix()
        vertices = vertices @ self.render.projection.projection_matrix
        vertices /= vertices[:,-1].reshape(-1, 1)
        vertices[(vertices > 2) | (vertices < -2)] = 0
        vertices = vertices @ self.render.projection.to_screen_matrix
        vertices = vertices[:, :2] # [x, y, z, w] -> [x, y]

        for face in self.faces:
            shape = vertices[face]
            if not np.any((shape == self.render.H_WIDTH) | (shape == self.render.H_HEIGHT)):
                pg.draw.polygon(self.render.screen, pg.Color('orange'), shape, 1)

        # for vertex in vertices:
        #     if not np.any((vertex == self.render.H_WIDTH) | (vertex == self.render.H_HEIGHT)):
        #         pg.draw.circle(self.render.screen, pg.Color('white'), vertex, 3)

    def translate(self, pos):
        self.vertices = self.vertices @ translate(pos) # @ is for matrix multiplacation

    def scale(self, scale_to):
        self.vertices = self.vertices @ scale(scale_to)

    def rotate_x(self, angle):
        self.vertices = self.vertices @ rotate_x(angle)
    
    def rotate_y(self, angle):
        self.vertices = self.vertices @ rotate_y(angle)

    def rotate_z(self, angle):
        self.vertices = self.vertices @ rotate_z(angle)

    
