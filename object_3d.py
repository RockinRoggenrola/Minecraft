import pygame as pg
from matrices import *


class Object3D:
    def __init__(self, vertices):
        self.vertices = [element.append(1) for element in vertices]
    
    def transform(self, matrix):
        self.vertices = self.vertices @ matrix
    
    
    
